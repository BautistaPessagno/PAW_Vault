---
title: "TestConfiguration"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java"]
---

# TestConfiguration

Builds the persistence test Spring context. HSQLDB is an in-memory database named paw with PostgreSQL syntax mode. It initializes test schema.sql followed by populator.sql, scans persistence beans, and supplies a DataSourceTransactionManager. This does not load [[WebConfig]], production PostgreSQL or SMTP.

Production connections: .

## Test cases

This is shared test configuration, not a test class.

## Exact test source

[persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java, lines 1–47](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>)

```java
package ar.edu.itba.paw.persistence;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.jdbc.datasource.init.DataSourceInitializer;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;

@Configuration
@EnableTransactionManagement
@ComponentScan({ "ar.edu.itba.paw.persistence" })
public class TestConfiguration {

    @Bean
    public DataSource dataSource() {
        final SimpleDriverDataSource dataSource = new SimpleDriverDataSource();
        dataSource.setDriverClass(org.hsqldb.jdbc.JDBCDriver.class);
        dataSource.setUrl("jdbc:hsqldb:mem:paw;sql.syntax_pgs=true");
        dataSource.setUsername("sa");
        dataSource.setPassword("");
        return dataSource;
    }

    @Bean
    public DataSourceInitializer dataSourceInitializer(final DataSource dataSource) {
        final ResourceDatabasePopulator populator = new ResourceDatabasePopulator();
        populator.addScript(new ClassPathResource("schema.sql"));
        populator.addScript(new ClassPathResource("populator.sql"));

        final DataSourceInitializer initializer = new DataSourceInitializer();
        initializer.setDataSource(dataSource);
        initializer.setDatabasePopulator(populator);
        return initializer;
    }

    @Bean
    public PlatformTransactionManager transactionManager(final DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
