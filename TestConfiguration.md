---
title: "TestConfiguration"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java"]
---

# TestConfiguration

Contexto de los tests de persistencia: HSQLDB en memoria con sintaxis PostgreSQL, las mismas migraciones Flyway que producción y después los fixtures de `populator.sql`.

## Guía de lectura

Operaciones para localizar en la fuente: `dataSource`, `flyway`, `dataSourceInitializer`, `transactionManager`.

Casos declarados: 0.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AddressJdbcDaoTest]], [[AlbumJdbcDaoTest]], [[ArtistJdbcDaoTest]], [[CartItemJdbcDaoTest]], [[EmailVerificationTokenJdbcDaoTest]], [[ImageJdbcDaoTest]], [[InquiryJdbcDaoTest]], [[MessageJdbcDaoTest]], [[PasswordResetTokenJdbcDaoTest]], [[PostImageJdbcDaoTest]], [[PostJdbcDaoTest]], [[ReviewJdbcDaoTest]], [[UserJdbcDaoTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>), líneas 1–59.

```java
package ar.edu.itba.paw.persistence;

import org.flywaydb.core.Flyway;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
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

    // Las mismas migraciones que corre WebConfig en produccion, sobre la base vacia.
    @Bean(initMethod = "migrate")
    public Flyway flyway(final DataSource dataSource) {
        return Flyway.configure()
                .dataSource(dataSource)
                .locations("classpath:db/migration")
                .load();
    }

    // Los fixtures se cargan recien con el esquema migrado.
    @Bean
    @DependsOn("flyway")
    public DataSourceInitializer dataSourceInitializer(final DataSource dataSource) {
        final ResourceDatabasePopulator populator = new ResourceDatabasePopulator();
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
