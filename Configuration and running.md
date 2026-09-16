---
title: "Configuration and running"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/resources/database.properties.example", "webapp/src/main/resources/mail.properties.example", "README.md", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Configuration and running

README lists Java 21, Maven 3.x and PostgreSQL 16. The local helper targets Homebrew PostgreSQL 18; this refresh does not establish the installed or deployed database version.

WebConfig marks database.properties and mail.properties as optional classpath resources. Required values can come from those files or Environment property sources; unavailable required properties still fail startup. It now uses DriverManagerDataSource and no connection pool. Local credential files were not read or copied into this vault.

The committed example files enumerate database, SMTP and application URL keys. app.base-url must include the deployed context path for verification/home mail links. README now includes this key and documents uppercase environment names such as DB_URL and APP_BASE_URL. Those settings were inspected as source, not exercised in a deployment.

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

## Reference workflow

Build from the source repository root. `mvn clean install` builds/tests and installs the six sibling modules. `mvn -pl webapp jetty:run` uses installed siblings. `mvn clean package` produces webapp/target/app.war. These commands were not executed by this documentation refresh.

Startup runs the canonical schema and targeted backfills, but does not load demo users or development albums. tools/sql/demo-users.sql is an optional manual USER/ADMIN seed outside the packaged classpath. Account creation normally sends verification mail, and activation requests welcome mail; publishing itself does neither.

No database changes, server startup, email or course deployment were performed. [[Schema history and seeds]] explains compatibility limits and [[Verification record]] records the actual checks.

[[Startup and dependency injection]] · [[Build and dependencies]] · [[Logging]]
