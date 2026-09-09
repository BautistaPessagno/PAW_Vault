---
title: "Logging"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "operations"]
sources: ["webapp/src/main/resources/logback.xml", "webapp/src/main/resources/logback-test.xml"]
---

# Logging

SLF4J/Logback writes application records under `${catalina.base:-.}/logs`. The current application pattern is paw-2026b-14-webapp.%d{yyyy-MM-dd}.log; warnings use paw-2026b-14-webapp-warnings.%d{yyyy-MM-dd}.log. Both retain seven daily periods.

The rolling appenders omit an explicit file element, so the active file uses the dated pattern as well. The source comments tie this naming to the course server log path; no remote log or deployment was checked.

ar.edu.itba logs INFO to APP_FILE with additivity=false. Root WARN goes to WARNINGS_FILE, so application ERROR records are not automatically copied into that root appender. [[EmailServiceImpl]] logs userId/postId and passes the full exception on failure. [[ImageServiceImpl]] logs rejected type/size and stored image ID, type and byte count. The source does not establish what external mail exception text may contain.

logback-test.xml remains in webapp main resources and is excluded from the packaged WAR. It configures application DEBUG and root WARN to console; other development classpaths may select it.

## Production configuration

[webapp/src/main/resources/logback.xml, lines 1–45](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/logback.xml>)

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

## Test configuration

[webapp/src/main/resources/logback-test.xml, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>)

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

[[Mail delivery]] · [[Configuration and running]]
