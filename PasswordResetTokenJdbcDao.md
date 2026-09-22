---
title: "PasswordResetTokenJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java"]
---

# PasswordResetTokenJdbcDao

Stores token rows through SimpleJdbcInsert and maps them with a static RowMapper. findByToken returns a row even when expired; deleteByToken reports whether this request claimed the link; deleteByUserId and deleteExpired(now) clean up. The unique user_id constraint makes a concurrent second insert for the same account fail with DuplicateKeyException.

## Connections

Project types referenced: [[PasswordResetToken]], [[PasswordResetTokenDao]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java, lines 1–85](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PasswordResetToken;
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
public class PasswordResetTokenJdbcDao implements PasswordResetTokenDao {

    private static final RowMapper<PasswordResetToken> ROW_MAPPER = (resultSet, rowNum) ->
            new PasswordResetToken(
                    resultSet.getLong("reset_id"),
                    resultSet.getLong("reset_user_id"),
                    resultSet.getString("reset_token"),
                    resultSet.getTimestamp("reset_expires_at").toLocalDateTime()
            );

    private static final String SELECT = "SELECT id AS reset_id, user_id AS reset_user_id, "
            + "token AS reset_token, expires_at AS reset_expires_at FROM password_reset_tokens ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public PasswordResetTokenJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("password_reset_tokens")
                .usingGeneratedKeyColumns("id");
    }

    /*
     * El vencimiento llega calculado desde el service: la ventana es una regla de
     * negocio, no del almacenamiento.
     */
    @Override
    public PasswordResetToken create(final long userId, final String token, final LocalDateTime expiresAt) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("token", token);
        parameters.put("expires_at", Timestamp.valueOf(expiresAt));
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new PasswordResetToken(id.longValue(), userId, token, expiresAt);
    }

    /*
     * Devuelve el token aunque este vencido: quien decide si todavia sirve es el service.
     */
    @Override
    public Optional<PasswordResetToken> findByToken(final String token) {
        return jdbcTemplate.query(SELECT + "WHERE token = ?", ROW_MAPPER, token)
                .stream()
                .findAny();
    }

    @Override
    public int deleteByToken(final String token) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE token = ?", token);
    }

    @Override
    public int deleteByUserId(final long userId) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE user_id = ?", userId);
    }

    /*
     * Igual que en create, el corte llega del service: el DAO solo borra lo que quedo atras.
     */
    @Override
    public int deleteExpired(final LocalDateTime now) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE expires_at < ?",
                Timestamp.valueOf(now));
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
