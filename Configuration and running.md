---
title: "Configuration and running"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/resources/database.properties.example", "webapp/src/main/resources/mail.properties.example", "webapp/src/pampero/resources/database.properties.example", "webapp/src/pampero/resources/mail.properties.example", "README.md", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "tools/seed_local_data.sh"]
---

# Configuration and running

README lists Java 21, Maven 3.x and PostgreSQL 16. The local helper targets Homebrew PostgreSQL 18, while the new seed script defaults to a `paw-pg` Docker container; this refresh does not establish the installed or deployed database version.

WebConfig marks database.properties and mail.properties as optional classpath resources. Required values can come from those files or Environment property sources, and README lists the uppercase environment names such as DB_URL and APP_BASE_URL. Unavailable required properties still fail startup. It uses DriverManagerDataSource and no connection pool. Local credential files were not read or copied into this vault.

## Pampero packaging

The course server receives only `web/app.war` by SFTP and cannot inject Tomcat environment variables. The new Maven profile `pampero` in webapp/pom.xml therefore excludes the local database.properties and mail.properties from the WAR and packages two separate files from webapp/src/pampero/resources instead. Both files are Git-ignored and have committed `.example` templates; the mail example already sets app.base-url to the group's public URL with its context path. An antrun check in the validate phase fails the build when either file is missing. The resources plugin now overwrites copied files so switching between local and Pampero builds cannot leave stale properties in an incremental WAR.

## database.properties.example

[webapp/src/main/resources/database.properties.example, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/database.properties.example>)

```text
db.driver=org.postgresql.Driver
db.url=jdbc:postgresql://localhost:5432/paw
db.username=your_database_username
db.password=your_database_password
```

## mail.properties.example

[webapp/src/main/resources/mail.properties.example, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>)

```text
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

## Pampero database.properties.example

[webapp/src/pampero/resources/database.properties.example, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/pampero/resources/database.properties.example>)

```text
# Configuracion exclusiva del WAR que se sube a Pampero. Copiar a
# database.properties y completar con los datos de PostgreSQL de la catedra.
db.driver=org.postgresql.Driver
db.url=jdbc:postgresql://pampero-database-host:5432/paw
db.username=your_pampero_database_username
db.password=your_pampero_database_password
```

## Pampero mail.properties.example

[webapp/src/pampero/resources/mail.properties.example, lines 1–13](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/pampero/resources/mail.properties.example>)

```text
# Configuracion exclusiva del WAR que se sube a Pampero. Copiar a
# mail.properties y completar las credenciales SMTP de produccion.
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
app.base-url=http://pawserver.it.itba.edu.ar/paw-2026b-14
```

## Reference workflow

Build from the source repository root. `mvn clean install` builds, tests and installs the six sibling modules. `mvn -pl webapp jetty:run` uses installed siblings. `mvn clean package` produces webapp/target/app.war for local use, and `mvn clean package -Ppampero` produces the deployable WAR after the Pampero files exist. These commands were not executed by this documentation refresh.

Startup runs the canonical schema and its backfills, but does not load demo users or catalog data. tools/sql/demo-users.sql is an optional manual USER/ADMIN seed outside the packaged classpath. tools/seed_local_data.sh loads those users plus 200 artists and 24 illustrated demo publications; see [[Schema history and seeds]] for its validation steps and a likely incompatibility with the current search_phrase columns. Account creation sends verification mail, activation sends welcome mail, and password changes send a notice; publishing sends nothing.

No database changes, server startup, email or course deployment were performed. [[Verification record]] records the actual checks.

[[Startup and dependency injection]] · [[Build and dependencies]] · [[Logging]] · [[Development tools]]
