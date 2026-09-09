---
title: "Build and dependencies"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "operations"]
sources: ["pom.xml", "models/pom.xml", "persistence/pom.xml", "persistence-contracts/pom.xml", "services/pom.xml", "services-contracts/pom.xml", "webapp/pom.xml", "models/.mvn/jvm.config", "models/.mvn/maven.config", "persistence-contracts/.mvn/jvm.config", "persistence-contracts/.mvn/maven.config", "persistence/.mvn/jvm.config", "persistence/.mvn/maven.config", "services-contracts/.mvn/jvm.config", "services-contracts/.mvn/maven.config", "services/.mvn/jvm.config", "services/.mvn/maven.config", "webapp/.mvn/jvm.config", "webapp/.mvn/maven.config"]
---

# Build and dependencies

The root POM aggregates six modules under ar.edu.itba.paw:paw2026b:1.0-SNAPSHOT. Its dependencyManagement fixes external library versions. Child POMs still explicitly declare sibling versions and runtime scopes; the stronger centralization claim in docs/setup.md is not what these files implement.

`models`, both contracts modules, persistence and services are JARs. webapp is a WAR with finalName webapp. The compiler source/target is 21. The servlet API is provided by the container. Hibernate Validator implements Bean Validation here; its presence does not imply Hibernate ORM or JPA.

## Pinned versions in this snapshot

| Property | Value |
|---|---|
| `project.build.sourceEncoding` | `UTF-8` |
| `maven.compiler.source` | `21` |
| `maven.compiler.target` | `21` |
| `org.springframework.version` | `5.3.33` |
| `servlet-api.version` | `2.5` |
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

## Direct dependencies by module

Compile is the default when no scope is declared. For external dependencies without a child scope, consult the parent managed scope. Runtime implementations are packaged but excluded from the consumer compile classpath.

### models

| Dependency | Declared scope |
|---|---|

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/pom.xml>)

### persistence

| Dependency | Declared scope |
|---|---|
| `spring-context` | default / inherited |
| `spring-jdbc` | default / inherited |
| `postgresql` | default / inherited |
| `persistence-contracts` | default / inherited |
| `spring-test` | default / inherited |
| `junit-jupiter` | default / inherited |
| `hsqldb` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/pom.xml>)

### persistence-contracts

| Dependency | Declared scope |
|---|---|
| `models` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/pom.xml>)

### services

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

### services-contracts

| Dependency | Declared scope |
|---|---|
| `models` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/pom.xml>)

### webapp

| Dependency | Declared scope |
|---|---|
| `spring-webmvc` | default / inherited |
| `spring-jdbc` | default / inherited |
| `postgresql` | default / inherited |
| `validation-api` | default / inherited |
| `hibernate-validator` | default / inherited |
| `services` | runtime |
| `persistence` | runtime |
| `services-contracts` | default / inherited |
| `servlet-api` | default / inherited |
| `jstl` | default / inherited |
| `slf4j-api` | default / inherited |
| `logback-classic` | default / inherited |
| `spring-context-support` | default / inherited |
| `javax.mail` | default / inherited |
| `thymeleaf-spring5` | default / inherited |

[Exact POM](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/pom.xml>)

## Build lifecycle

Run Maven from the source repository root. `mvn clean install` builds the reactor, runs tests and installs sibling SNAPSHOTs. This matters before `mvn -pl webapp jetty:run`, which runs only webapp and resolves siblings from installed artifacts. `mvn clean package` produces `webapp/target/webapp.war` without installing it.

The inherited Jetty plugin is 9.4.58.v20250814 with scanIntervalSeconds=10, port=8080 and useTestScope=true in its configuration. Child pluginManagement pins compiler 3.13.0 and Surefire 3.3.0, among others. WAR plugin 3.4.0 excludes logback-test.xml from the packaged WAR. The `.mvn/jvm.config` and `.mvn/maven.config` files in each module are empty in this snapshot.

No Maven wrapper, Flyway dependency, Spring Boot starter, Spring Security dependency, JPA persistence unit or frontend package manager is defined. [[Configuration and running]] describes runtime configuration; [[Testing and evidence]] records what was actually checked.
