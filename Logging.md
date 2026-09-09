---
title: "Logging"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "operations"]
sources: ["webapp/src/main/resources/logback.xml", "webapp/src/main/resources/logback-test.xml"]
---

# Logging

The application uses SLF4J and Logback. Production logback.xml defines an application rolling file and a separate root-warning rolling file, both retaining seven daily archives. LOG_DIR defaults to logs.

The ar.edu.itba logger has INFO level and additivity=false, sending its records to APP_FILE. Root WARN records go to WARNINGS_FILE. Because the application logger is non-additive, its ERROR mail records are not automatically duplicated into the root warnings file.

The application code's concrete business logging is in [[EmailServiceImpl]]: welcome logs userId, contact logs postId, failures add the exception class name. It does not log mail bodies, names or recipient addresses in these calls. There are no publish-success log statements in PostServiceImpl.

logback-test.xml writes to console with application DEBUG and root WARN. It is located in webapp main resources despite its name; the WAR packaging configuration excludes it. Its presence on other development classpaths can affect configuration selection, so do not infer deployed logging from a local console alone.

## logback.xml

[webapp/src/main/resources/logback.xml, lines 1–35](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/resources/logback.xml>)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property name="LOG_DIR" value="${LOG_DIR:-logs}"/>
  <property name="LOG_PATTERN" value="%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"/>

  <appender name="APP_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${LOG_DIR}/paw-2026b-14.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${LOG_DIR}/paw-2026b-14.%d{yyyy-MM-dd}.log</fileNamePattern>
      <maxHistory>7</maxHistory>
    </rollingPolicy>
    <encoder>
      <pattern>${LOG_PATTERN}</pattern>
    </encoder>
  </appender>

  <appender name="WARNINGS_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>${LOG_DIR}/paw-2026b-14-warnings.log</file>
    <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
      <fileNamePattern>${LOG_DIR}/paw-2026b-14-warnings.%d{yyyy-MM-dd}.log</fileNamePattern>
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

## logback-test.xml

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
