---
title: "UserJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java"]
---

# UserJdbcDao

`USER_SELECT` aliases each column for one shared RowMapper. `findById` binds an ID; `findByEmail` binds a normalized email. `findOrCreate` normalizes then reads before inserting; `create` normalizes again and inserts username/email with SimpleJdbcInsert. Normalization is trim plus Locale.ROOT lowercase. An existing email preserves the prior username. The DAO does not handle uniqueness exceptions locally. [[UserServiceImpl]] uses the lower-level methods to control welcome mail.

## Connections

Project types referenced: [[User]], [[UserDao]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java, lines 1–75](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;

@Repository
public class UserJdbcDao implements UserDao {

    private static final RowMapper<User> ROW_MAPPER = (resultSet, rowNum) -> new User(
            resultSet.getLong("user_id"),
            resultSet.getString("user_username"),
            resultSet.getString("user_email")
    );

    private static final String USER_SELECT =
            "SELECT id AS user_id, username AS user_username, email AS user_email FROM users ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public UserJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("users")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Optional<User> findById(final long id) {
        return jdbcTemplate.query(USER_SELECT + "WHERE id = ?", ROW_MAPPER, id)
                .stream()
                .findAny();
    }

    @Override
    public Optional<User> findByEmail(final String email) {
        return jdbcTemplate.query(USER_SELECT + "WHERE email = ?", ROW_MAPPER, normalize(email))
                .stream()
                .findAny();
    }

    @Override
    public User findOrCreate(final String username, final String email) {
        final String normalizedEmail = normalize(email);
        return findByEmail(normalizedEmail)
                .orElseGet(() -> create(username, normalizedEmail));
    }

    @Override
    public User create(final String username, final String email) {
        final String normalizedEmail = normalize(email);
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("username", username);
        parameters.put("email", normalizedEmail);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new User(id.longValue(), username, normalizedEmail);
    }


    private static String normalize(final String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
