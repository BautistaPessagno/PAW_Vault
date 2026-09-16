---
title: "TestConfiguration"
categories: ["Testing"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java"]
---

# TestConfiguration

Builds the persistence test Spring context. HSQLDB is an in-memory database named paw with PostgreSQL syntax mode. It initializes test schema.sql followed by populator.sql, scans persistence beans, and supplies a DataSourceTransactionManager. This does not load [[WebConfig]], production PostgreSQL or SMTP.

## Connections

Project types referenced: none.

Referenced by: [[AlbumJdbcDaoTest]], [[ArtistJdbcDaoTest]], [[EmailVerificationTokenJdbcDaoTest]], [[ImageJdbcDaoTest]], [[InquiryJdbcDaoTest]], [[PostJdbcDaoTest]], [[UserJdbcDaoTest]].

## Exact source

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
