---
title: "EmailVerificationTokenJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java"]
---

# EmailVerificationTokenJdbcDao

Stores the token string with a user foreign key, looks up by unique token, and deletes by user ID. No time-based expiration is implemented.

## Connections

Project types referenced: [[EmailVerificationToken]], [[EmailVerificationTokenDao]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java, lines 1–60](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailVerificationToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Repository
public class EmailVerificationTokenJdbcDao implements EmailVerificationTokenDao {

    private static final RowMapper<EmailVerificationToken> ROW_MAPPER = (resultSet, rowNum) ->
            new EmailVerificationToken(
                    resultSet.getLong("verification_id"),
                    resultSet.getLong("verification_user_id"),
                    resultSet.getString("verification_token")
            );

    private static final String SELECT = "SELECT id AS verification_id, user_id AS verification_user_id, "
            + "token AS verification_token FROM email_verification_tokens ";

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
    public EmailVerificationToken create(final long userId, final String token) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("token", token);
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new EmailVerificationToken(id.longValue(), userId, token);
    }

    @Override
    public Optional<EmailVerificationToken> findByToken(final String token) {
        return jdbcTemplate.query(SELECT + "WHERE token = ?", ROW_MAPPER, token)
                .stream()
                .findAny();
    }

    @Override
    public int deleteByUserId(final long userId) {
        return jdbcTemplate.update("DELETE FROM email_verification_tokens WHERE user_id = ?", userId);
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
