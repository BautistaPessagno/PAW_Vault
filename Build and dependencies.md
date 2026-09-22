---
title: "Build and dependencies"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/pom.xml", "persistence-contracts/pom.xml", "persistence/pom.xml", "pom.xml", "services-contracts/pom.xml", "services/pom.xml", "webapp/pom.xml", "models/.mvn/jvm.config", "models/.mvn/maven.config", "persistence-contracts/.mvn/jvm.config", "persistence-contracts/.mvn/maven.config", "persistence/.mvn/jvm.config", "persistence/.mvn/maven.config", "services-contracts/.mvn/jvm.config", "services-contracts/.mvn/maven.config", "services/.mvn/jvm.config", "services/.mvn/maven.config", "webapp/.mvn/jvm.config", "webapp/.mvn/maven.config"]
---

# Build and dependencies

The root POM aggregates six modules under ar.edu.itba.paw:paw2026b:1.0-SNAPSHOT. Java source/target is 21. Spring Framework versions now come from spring-framework-bom. Spring Security web/config/taglibs are explicitly managed and consumed in webapp. The servlet API is javax.servlet-api 4.0.1 with provided scope.

The five non-web modules are JARs; webapp produces app.war. Sibling dependencies still declare versions/scopes in child POMs. Runtime dependencies package implementations without exposing them to the consumer compiler. Hibernate Validator is Bean Validation, not an ORM.

## Pinned properties

| Property | Value |
|---|---|
| `project.build.sourceEncoding` | `UTF-8` |
| `maven.compiler.source` | `21` |
| `maven.compiler.target` | `21` |
| `org.springframework.version` | `5.3.33` |
| `org.springframework.security.version` | `5.8.16` |
| `servlet-api.version` | `4.0.1` |
| `jstl.version` | `1.2` |
| `postgresql.version` | `42.2.5` |
| `javax.validation-api.version` | `2.0.1.Final` |
| `org.hibernate.validator` | `6.2.4.Final` |
| `junit-jupiter.version` | `5.10.2` |
| `mockito.version` | `5.12.0` |
| `hsqldb.version` | `2.7.3` |
| `slf4j.version` | `1.7.36` |
| `logback.version` | `1.2.13` |
| `javax.mail.version` | `1.6.2` |
| `thymeleaf.version` | `3.0.15.RELEASE` |
| `commons-fileupload.version` | `1.5` |
| `maven-antrun-plugin.version` | `3.1.0` |

## models

| Dependency | Declared scope |
|---|---|


[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/pom.xml>)

## persistence-contracts

| Dependency | Declared scope |
|---|---|
| `models` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/pom.xml>)

## persistence

| Dependency | Declared scope |
|---|---|
| `spring-context` | default / inherited |
| `spring-jdbc` | default / inherited |
| `postgresql` | default / inherited |
| `persistence-contracts` | default / inherited |
| `spring-test` | test |
| `junit-jupiter` | default / inherited |
| `hsqldb` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/pom.xml>)

## services-contracts

| Dependency | Declared scope |
|---|---|
| `models` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/pom.xml>)

## services

| Dependency | Declared scope |
|---|---|
| `spring-context` | default / inherited |
| `spring-tx` | default / inherited |
| `services-contracts` | default / inherited |
| `persistence-contracts` | default / inherited |
| `persistence` | runtime |
| `slf4j-api` | default / inherited |
| `spring-context-support` | default / inherited |
| `javax.mail` | default / inherited |
| `thymeleaf-spring5` | default / inherited |
| `junit-jupiter` | default / inherited |
| `mockito-core` | default / inherited |
| `mockito-junit-jupiter` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/pom.xml>)

## webapp

| Dependency | Declared scope |
|---|---|
| `spring-webmvc` | default / inherited |
| `spring-jdbc` | default / inherited |
| `spring-security-web` | default / inherited |
| `spring-security-config` | default / inherited |
| `spring-security-taglibs` | default / inherited |
| `postgresql` | default / inherited |
| `validation-api` | default / inherited |
| `hibernate-validator` | default / inherited |
| `services` | runtime |
| `persistence` | runtime |
| `services-contracts` | default / inherited |
| `javax.servlet-api` | default / inherited |
| `jstl` | default / inherited |
| `slf4j-api` | default / inherited |
| `logback-classic` | default / inherited |
| `spring-context-support` | default / inherited |
| `javax.mail` | default / inherited |
| `thymeleaf-spring5` | default / inherited |
| `commons-fileupload` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/pom.xml>)

## Build lifecycle

The only POM changes since `40328f0` are build-side: the root POM manages maven-antrun-plugin 3.1.0, and webapp/pom.xml adds the `pampero` profile plus `overwrite=true` for the resources plugin. Module dependencies and scopes are unchanged.

`mvn clean install` builds/tests the reactor and installs sibling SNAPSHOTs. `mvn clean package` produces webapp/target/app.war. Jetty remains 9.4.58.v20250814 with scan interval 10, port 8080 and useTestScope=true in the parent configuration. Child pluginManagement pins compiler 3.13.0 and Surefire 3.3.0; WAR plugin 3.4.0 excludes logback-test.xml.

The per-module .mvn/jvm.config and maven.config files are empty. No Maven wrapper, Spring Boot starter, Flyway dependency, JPA persistence unit or frontend package manager is defined. No Maven command ran for this refresh.

## Pampero profile

`mvn clean package -Ppampero` swaps the resource set of the webapp module: src/main/resources is copied without database.properties and mail.properties, and src/pampero/resources contributes only those two files. In the validate phase an antrun target checks that both Pampero files exist and fails with a message naming the missing one. The result is still webapp/target/app.war. See [[Configuration and running]].

[[Architecture]] · [[Configuration and running]] · [[Testing and evidence]]
