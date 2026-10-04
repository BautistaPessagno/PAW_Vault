---
title: "Logging"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/resources/logback.xml", "webapp/src/main/resources/logback-test.xml", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "webapp/pom.xml"]
---

# Logging

> [!summary] En una frase
> El código loguea contra la fachada SLF4J y Logback escribe dos archivos diarios: uno con lo que hace la aplicación (INFO) y otro con las advertencias de todo lo demás (WARN), con el nombre exacto que la cátedra publica.

## Herramientas

| Herramienta | Para qué |
|---|---|
| SLF4J (`slf4j-api`) | Fachada: el código no depende de la implementación |
| Logback (`logback-classic`) | Implementación y configuración por XML |
| `RollingFileAppender` + `TimeBasedRollingPolicy` | Un archivo por día, siete días de historia |

## Configuración

| Logger | Nivel | Destino |
|---|---|---|
| `ar.edu.itba` (el código del proyecto) | INFO | `paw-2026b-14-webapp.<fecha>.log` |
| Raíz (Spring, drivers, contenedor) | WARN | `paw-2026b-14-webapp-warnings.<fecha>.log` |

- `additivity="false"` en el logger del proyecto: sus mensajes no se repiten en el archivo de advertencias.
- El directorio es `${catalina.base}/logs`; fuera de Tomcat cae a `./logs`.
- El patrón incluye fecha, hilo, nivel, logger abreviado y mensaje. El nombre del hilo permite distinguir los envíos de correo (`mail-1`, `mail-2`, ...).

`logback-test.xml` configura consola y nivel DEBUG para el proyecto. Logback lo prefiere sobre `logback.xml` cuando está en el classpath, así que es el que rige al correr con `mvn jetty:run`. El WAR **no** lo incluye: `maven-war-plugin` lo excluye con `packagingExcludes`, de modo que en el servidor rige `logback.xml`.

## Qué se loguea

Hay `LOGGER` en ocho services ([[UserServiceImpl]], [[InquiryServiceImpl]], [[PostServiceImpl]], [[CartServiceImpl]], [[AddressServiceImpl]], [[ReviewServiceImpl]], [[ImageServiceImpl]], [[EmailServiceImpl]]), en [[WebConfig]] (rechazo del pool de correo) y en [[MultipartExceptionHandlerFilter]]. Ningún controller ni DAO loguea.

| Nivel | Cantidad | Uso |
|---|---|---|
| INFO | 39 | Una operación de negocio que terminó: registro, verificación, publicación, consulta, cambio de estado, correo enviado |
| WARN | 9 | Algo esperable que no salió: intento rechazado, pool saturado, archivo demasiado grande |
| ERROR | 7 | Fallas de infraestructura, sobre todo de SMTP, con la excepción |

Convenciones que se repiten:

- `private static final Logger LOGGER = LoggerFactory.getLogger(Clase.class)`.
- Mensajes parametrizados (`"... userId={}"`), nunca concatenación: el texto no se arma si el nivel está apagado.
- Se loguean **ids**, no datos personales: ni correos, ni tokens, ni contraseñas.
- Los logs de éxito se emiten **después del commit** ([[TransactionCallbacks]]): si la transacción se revierte, no queda un log que afirme algo que no pasó.
- Las lecturas no se loguean.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Nombre de archivo fijo con fecha | La cátedra publica los logs en una URL con ese nombre exacto | Comentario en `logback.xml` |
| Sin `<file>` en los appenders | Con la política por tiempo, omitirlo hace que el archivo del día ya lleve la fecha; con `<file>`, el de hoy quedaría sin fecha y no se podría abrir desde la URL hasta rotar | Comentario en `logback.xml` |
| Dos archivos | Separar la actividad propia del ruido de los frameworks | Estructura de `logback.xml`; inferencia |
| Loguear en services, no en controllers | La operación de negocio vive en el service | `CLAUDE.md` del repo |
| No loguear tokens ni correos | Los logs son públicos para la cátedra | Inferencia sobre los mensajes |
| Excluir `logback-test.xml` del WAR | Consola en desarrollo, archivos en el servidor | `webapp/pom.xml` |

## Límites conocidos

- La separación entre desarrollo y servidor depende de la exclusión del WAR: `logback-test.xml` vive en `src/main/resources`, y si se quitara `packagingExcludes` el servidor loguearía a consola en vez de a los archivos que publica la cátedra.
- No hay ninguna llamada `LOGGER.debug`: el nivel DEBUG de desarrollo hoy no agrega mensajes propios.
- No hay id de correlación por request.

## Preguntas de defensa

**¿Qué usan para loguear?**
SLF4J como interfaz y Logback como implementación.

**¿Dónde quedan los logs?**
En `logs/` del contenedor, un archivo por día para la aplicación y otro para advertencias, con el nombre que la cátedra expone.

**¿Qué loguean y qué no?**
Operaciones de negocio completadas y fallas, con ids. No datos personales ni secretos, y no lecturas.

**¿Por qué algunos logs se emiten después del commit?**
Para que el log no afirme una operación que después se revirtió.

## Evidencia de código

### Configuración de producción

Fuente exacta en `8929aea`: [webapp/src/main/resources/logback.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback.xml>), líneas 1–45.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <!--
    La catedra publica los logs en
    http://pawserver.it.itba.edu.ar/logs/paw-2026b-14-webapp.<FECHA>.log
    asi que el nombre del archivo tiene que ser exactamente ese.

    Los appenders no declaran <file>: con TimeBasedRollingPolicy, omitirlo hace que
    el archivo activo se llame igual que el patron, o sea que el log del dia en curso
    ya lleva la fecha en el nombre. Si se declarara <file>, el log de hoy quedaria sin
    fecha y no se podria abrir desde la URL de la catedra hasta que rotara.

    catalina.base lo define Tomcat; el default es solo para correr fuera del contenedor.
  -->
  <property name="LOG_DIR" value="${catalina.base:-.}/logs"/>
  <property name="LOG_PATTERN" value="%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"/>

  <appender name="APP_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${LOG_DIR}/paw-2026b-14-webapp.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder>
      <pattern>${LOG_PATTERN}</pattern>
    </encoder>
  </appender>

  <appender name="WARNINGS_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${LOG_DIR}/paw-2026b-14-webapp-warnings.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder>
      <pattern>${LOG_PATTERN}</pattern>
    </encoder>
  </appender>

  <logger name="ar.edu.itba" level="INFO" additivity="false">
    <appender-ref ref="APP_FILE"/>
  </logger>

  <root level="WARN">
    <appender-ref ref="WARNINGS_FILE"/>
  </root>
</configuration>
```

### Configuración de consola

Fuente exacta en `8929aea`: [webapp/src/main/resources/logback-test.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>), líneas 1–16.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>

  <logger name="ar.edu.itba" level="DEBUG" additivity="false">
    <appender-ref ref="CONSOLE"/>
  </logger>

  <root level="WARN">
    <appender-ref ref="CONSOLE"/>
  </root>
</configuration>
```

### Exclusión del WAR

Fuente exacta en `8929aea`: [webapp/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/pom.xml>), líneas 153–159.

```xml
        <plugin>
          <artifactId>maven-war-plugin</artifactId>
          <version>3.4.0</version>
          <configuration>
            <packagingExcludes>**/logback-test.xml</packagingExcludes>
          </configuration>
        </plugin>
```

## Archivos para seguir el flujo

- [webapp/src/main/resources/logback.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback.xml>)
- [webapp/src/main/resources/logback-test.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>)
- [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) · [[UserServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>) · [[InquiryServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) · [[EmailServiceImpl]]

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
