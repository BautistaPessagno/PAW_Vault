---
title: "Configuration and running"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "operations"]
sources: ["webapp/src/main/resources/database.properties.example", "webapp/src/main/resources/mail.properties.example", "README.md"]
---

# Configuration and running

The repository README names Java 21, Maven 3.x and PostgreSQL 16. The local helper script targets Homebrew PostgreSQL 18. This map records both rather than claiming the developer's installed database version was verified.

## Required local files

[[WebConfig]] declares required classpath `database.properties` and `mail.properties`. The committed `.example` files show the keys. Local values are ignored by Git and were not read for this map.

[webapp/src/main/resources/database.properties.example, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/database.properties.example>)

```properties
db.driver=org.postgresql.Driver
db.url=jdbc:postgresql://localhost:5432/paw
db.username=your_database_username
db.password=your_database_password
```

[webapp/src/main/resources/mail.properties.example, lines 1–10](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>)

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
```


Database driver is dynamically loaded and checked as a java.sql.Driver. The datasource is SimpleDriverDataSource, with no connection pool configuration. getRequiredProperty fails when a required key is unavailable; mail.port is parsed as Integer. The two @PropertySource declarations also require their files to exist, so the README's environment-only alternative is not fully supported as written without resolving that file-loading requirement.

## Commands, shown for reference

```bash
cd /Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b
cp webapp/src/main/resources/database.properties.example webapp/src/main/resources/database.properties
cp webapp/src/main/resources/mail.properties.example webapp/src/main/resources/mail.properties
# Fill the local files with the intended database and SMTP settings.
mvn clean install
mvn -pl webapp jetty:run
```

These commands were not executed while authoring the vault. Starting with an empty PostgreSQL database and adequate table-creation permissions runs the current schema initializer. It creates tables but not sample content. Historical SQL and the optional development seed are separate in [[Schema history and seeds]].

Submitting create/publish with a new email can send welcome mail. Submitting contact attempts synchronous delivery. Building the vault requires neither operation and no mail was sent.

The deployment target host, external database state and server readiness are not verified. TODO.md records a course deployment blocker, but that document is not a live status check.

[[Startup and dependency injection]] · [[Build and dependencies]] · [[Logging]] · [[Development tools]]
