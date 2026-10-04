---
title: "EmailVerificationTokenJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java"]
---

# EmailVerificationTokenJdbcDao

Tokens de verificación con Spring JDBC: inserta con su fecha, busca por token, trae el último de una Cuenta y borra por Cuenta.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `create`, `findByToken`, `findLatestByUserId`, `deleteByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[EmailVerificationToken]], [[EmailVerificationTokenDao]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>), líneas 1–74.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailVerificationToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Repository
public class EmailVerificationTokenJdbcDao implements EmailVerificationTokenDao {

    private static final RowMapper<EmailVerificationToken> ROW_MAPPER = (resultSet, rowNum) ->
            new EmailVerificationToken(
                    resultSet.getLong("verification_id"),
                    resultSet.getLong("verification_user_id"),
                    resultSet.getString("verification_token"),
                    resultSet.getTimestamp("verification_created_at").toLocalDateTime()
            );

    private static final String SELECT = "SELECT id AS verification_id, user_id AS verification_user_id, "
            + "token AS verification_token, created_at AS verification_created_at "
            + "FROM email_verification_tokens ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public EmailVerificationTokenJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("email_verification_tokens")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public EmailVerificationToken create(final long userId, final String token, final LocalDateTime createdAt) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("token", token);
        parameters.put("created_at", Timestamp.valueOf(createdAt));
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new EmailVerificationToken(id.longValue(), userId, token, createdAt);
    }

    @Override
    public Optional<EmailVerificationToken> findByToken(final String token) {
        return jdbcTemplate.query(SELECT + "WHERE token = ?", ROW_MAPPER, token)
                .stream()
                .findAny();
    }

    // Normalmente hay uno solo por cuenta, pero nada en el esquema impide que haya mas.
    @Override
    public Optional<EmailVerificationToken> findLatestByUserId(final long userId) {
        return jdbcTemplate.query(SELECT + "WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT 1",
                        ROW_MAPPER, userId)
                .stream()
                .findFirst();
    }

    @Override
    public int deleteByUserId(final long userId) {
        return jdbcTemplate.update("DELETE FROM email_verification_tokens WHERE user_id = ?", userId);
    }

}
```
