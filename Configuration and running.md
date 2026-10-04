---
title: "Configuration and running"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/resources/database.properties.example", "webapp/src/main/resources/mail.properties.example", "webapp/src/pampero/resources/database.properties.example", "webapp/src/pampero/resources/mail.properties.example", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "docs/setup.md", "tools/setup_local_postgres.sh", "tools/seed_local_data.sh", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# Configuration and running

> [!summary] En una frase
> La aplicación necesita dos archivos de propiedades que no se versionan (base y correo); se leen al arrancar con `getRequiredProperty`, y hay un juego para desarrollo local y otro para el servidor de la cátedra.

Esta nota documenta **las keys y los ejemplos versionados**, nunca valores reales.

## Los archivos

| Archivo | Se versiona | Uso |
|---|---|---|
| `webapp/src/main/resources/database.properties.example` | Sí | Plantilla local |
| `webapp/src/main/resources/database.properties` | No | Conexión local |
| `webapp/src/main/resources/mail.properties.example` | Sí | Plantilla local |
| `webapp/src/main/resources/mail.properties` | No | SMTP local |
| `webapp/src/pampero/resources/*.properties.example` | Sí | Plantillas del servidor de la cátedra |
| `webapp/src/pampero/resources/*.properties` | No | Valores del servidor; entran al WAR con `-Ppampero` |

## Keys

| Key | Para qué | Quién la lee |
|---|---|---|
| `db.driver`, `db.url`, `db.username`, `db.password` | Conexión JDBC | Bean `dataSource` |
| `mail.host`, `mail.port`, `mail.username`, `mail.password` | Servidor SMTP | Bean `mailSender` |
| `mail.smtp.auth`, `mail.smtp.starttls.enable` | Autenticación y cifrado de la conexión SMTP | Bean `mailSender` |
| `mail.smtp.connection-timeout-ms`, `read-timeout-ms`, `write-timeout-ms` | Topes para que un SMTP lento no retenga un hilo | Bean `mailSender` |
| `app.mail.from` | Remitente | [[EmailServiceImpl]], con `@Value` |
| `app.base-url` | URL pública para armar los enlaces de los correos | [[EmailServiceImpl]], con `@Value` |

`app.base-url` tiene que ser absoluta: el correo se arma en un hilo `@Async`, donde no hay request del que deducir host ni context path. En el servidor de la cátedra la aplicación cuelga de `/paw-2026b-14`, así que la URL lo incluye ([[Mail delivery]], [[Tokens and email links]]).

Las keys `db.*` y `mail.*` se leen en [[WebConfig]] con `environment.getRequiredProperty(...)`: si falta una, la aplicación no arranca ([[Startup and dependency injection]]). `app.mail.from` y `app.base-url` se inyectan en el constructor de [[EmailServiceImpl]] con `@Value("${...}")`. El proyecto no declara un `PropertySourcesPlaceholderConfigurer`, así que esas dos no tienen la misma garantía de fallo al arrancar: ver [[Known gaps and document drift]].

## Levantar en local

La aplicación la levanta quien desarrolla; estos son los pasos de `docs/setup.md`.

```bash
# 1. PostgreSQL: rol y base (guía interactiva para macOS con Homebrew)
bash tools/setup_local_postgres.sh

# 2. Configuración local a partir de los ejemplos
cp webapp/src/main/resources/database.properties.example webapp/src/main/resources/database.properties
cp webapp/src/main/resources/mail.properties.example webapp/src/main/resources/mail.properties
# completar los dos archivos con los valores propios

# 3. Compilar e instalar los módulos
mvn clean install

# 4. Arrancar
cd webapp && mvn jetty:run
```

En el primer arranque Flyway crea las tablas. Los datos de demostración son opcionales: `bash tools/seed_local_data.sh` ([[Schema history and seeds]]).

## Desplegar en el servidor de la cátedra

```bash
cp webapp/src/pampero/resources/database.properties.example webapp/src/pampero/resources/database.properties
cp webapp/src/pampero/resources/mail.properties.example webapp/src/pampero/resources/mail.properties
# completar con los valores provistos para el servidor
mvn clean package -Ppampero
```

El resultado es `webapp/target/app.war`. Detalle del perfil en [[Build and dependencies]].

## Diferencias entre local y servidor

| Aspecto | Local | Servidor |
|---|---|---|
| Contenedor | Jetty (plugin Maven) | Tomcat |
| Context path | `/` | `/paw-2026b-14` |
| `app.base-url` | `http://localhost:8080` | URL pública del grupo |
| Logs | `./logs/` | `${catalina.base}/logs/`, publicados por la cátedra ([[Logging]]) |

Por el context path, toda URL de una JSP se arma con `<c:url>` y toda redirección de un controller con el prefijo `redirect:`, que Spring resuelve relativo al contexto.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Propiedades fuera de Git, con `.example` | No versionar credenciales | `CLAUDE.md` del repo, `.gitignore` |
| `getRequiredProperty` para base y SMTP | Fallar al arrancar, no en el primer uso | `CLAUDE.md` del repo |
| Tres timeouts de SMTP | Un servidor de correo caído no puede colgar hilos | `docs/setup.md`, comentarios de [[WebConfig]] |
| `app.base-url` explícita | En el hilo asíncrono no hay request | Comentario en `mail.properties.example` |
| `.worktreeinclude` | Copiar las propiedades ignoradas a un worktree nuevo | Comentario del archivo |

## Preguntas de defensa

**¿Dónde están las credenciales?**
En archivos de propiedades que no se versionan. El repositorio tiene solo ejemplos con las keys.

**¿Cómo sabe el correo qué URL poner en un enlace?**
Por la propiedad `app.base-url`, porque el envío corre fuera del request.

**¿Qué cambia entre local y producción?**
Los dos archivos de propiedades, elegidos por el perfil Maven, y el context path.

## Evidencia de código

### Ejemplo de base (local)

Fuente exacta en `8929aea`: [webapp/src/main/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/database.properties.example>), líneas 1–4.

```properties
db.driver=org.postgresql.Driver
db.url=jdbc:postgresql://localhost:5432/paw
db.username=your_database_username
db.password=your_database_password
```

### Ejemplo de correo (local)

Fuente exacta en `8929aea`: [webapp/src/main/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>), líneas 1–16.

```properties
mail.host=smtp.gmail.com
mail.port=587
mail.username=your_smtp_username
mail.password=your_smtp_password
mail.smtp.auth=true
mail.smtp.starttls.enable=true
mail.smtp.connection-timeout-ms=5000
mail.smtp.read-timeout-ms=10000
mail.smtp.write-timeout-ms=10000
app.mail.from=your_smtp_username

# URL publica de la aplicacion, usada para los links de los mails.
# Tiene que ser absoluta: el envio corre en un hilo @Async, donde no hay request
# del que deducirla. En el server de la catedra la app cuelga de un context path.
# Produccion: http://pawserver.it.itba.edu.ar/paw-2026b-14
app.base-url=http://localhost:8080
```

### Lectura del SMTP

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 145–161.

```java
  @Bean
  public JavaMailSender mailSender(final Environment environment) {
    final JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
    mailSender.setHost(environment.getRequiredProperty("mail.host"));
    mailSender.setPort(environment.getRequiredProperty("mail.port", Integer.class));
    mailSender.setUsername(environment.getRequiredProperty("mail.username"));
    mailSender.setPassword(environment.getRequiredProperty("mail.password"));

    final Properties properties = mailSender.getJavaMailProperties();
    properties.put("mail.transport.protocol", SMTP_PROTOCOL);
    properties.put("mail.smtp.auth", environment.getRequiredProperty("mail.smtp.auth"));
    properties.put("mail.smtp.starttls.enable", environment.getRequiredProperty("mail.smtp.starttls.enable"));
    properties.put("mail.smtp.connectiontimeout", environment.getRequiredProperty("mail.smtp.connection-timeout-ms"));
    properties.put("mail.smtp.timeout", environment.getRequiredProperty("mail.smtp.read-timeout-ms"));
    properties.put("mail.smtp.writetimeout", environment.getRequiredProperty("mail.smtp.write-timeout-ms"));
    return mailSender;
  }
```

### Lectura de remitente y URL base

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>), líneas 43–54.

```java
    @Autowired
    public EmailServiceImpl(final JavaMailSender mailSender, final SpringTemplateEngine templateEngine,
                            final MessageSource messageSource,
                            @Value("${app.mail.from}") final String from,
                            @Value("${app.base-url}") final String baseUrl) {
        this.mailSender = mailSender;
        this.templateEngine = templateEngine;
        this.messageSource = messageSource;
        this.from = from;
        // Sin la barra final, asi concatenar un path que empieza con "/" no la duplica.
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
    }
```

## Archivos para seguir el flujo

- [webapp/src/main/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/database.properties.example>)
- [webapp/src/main/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>)
- [webapp/src/pampero/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/database.properties.example>)
- [webapp/src/pampero/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/mail.properties.example>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) · [[WebConfig]]
- [docs/setup.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/setup.md>)
- [tools/setup_local_postgres.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/setup_local_postgres.sh>)
- [tools/seed_local_data.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/seed_local_data.sh>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
