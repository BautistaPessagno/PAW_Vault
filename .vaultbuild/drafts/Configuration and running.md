@title: Configuration and running
@categories: Operations
@files: webapp/src/main/resources/database.properties.example, webapp/src/main/resources/mail.properties.example, webapp/src/pampero/resources/database.properties.example, webapp/src/pampero/resources/mail.properties.example, webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java, docs/setup.md, tools/setup_local_postgres.sh, tools/seed_local_data.sh

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

{{file:webapp/src/main/resources/database.properties.example}}

### Ejemplo de correo (local)

{{file:webapp/src/main/resources/mail.properties.example}}

### Lectura del SMTP

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java:145-161}}

### Lectura de remitente y URL base

{{code:services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java:43-54}}
