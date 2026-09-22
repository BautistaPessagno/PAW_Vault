---
title: "UserJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java"]
---

# UserJdbcDao

Normalizes email with trim and Locale.ROOT lowercasing, maps role, enabled and preferred_locale, and creates disabled accounts. Activation uses WHERE enabled = FALSE. updateUsername and updatePassword rewrite one row and reread it; updatePasswordIfMatches also requires the current hash, so a stale form cannot overwrite a password chosen later.

## Connections

Project types referenced: [[User]], [[UserDao]], [[UserRole]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java, lines 1–118](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
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
            resultSet.getString("user_email"),
            resultSet.getString("user_password_hash"),
            UserRole.valueOf(resultSet.getString("user_role")),
            resultSet.getBoolean("user_enabled"),
            resultSet.getString("user_preferred_locale")
    );

    private static final String USER_SELECT =
            "SELECT id AS user_id, username AS user_username, email AS user_email, " +
                    "password_hash AS user_password_hash, role AS user_role, enabled AS user_enabled, "
                    + "preferred_locale AS user_preferred_locale FROM users ";

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
    public User create(final String username, final String email, final String passwordHash, final UserRole role,
                       final String preferredLocale) {
        final String normalizedEmail = normalize(email);
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("username", username);
        parameters.put("email", normalizedEmail);
        parameters.put("password_hash", passwordHash);
        parameters.put("role", role.name());
        parameters.put("enabled", false);
        parameters.put("preferred_locale", preferredLocale);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new User(id.longValue(), username, normalizedEmail, passwordHash, role, false, preferredLocale);
    }

    @Override
    public boolean activateIfPending(final long id, final String username, final String passwordHash) {
        // El UPDATE condicional es lo que hace que la activacion sea de un solo uso:
        // la segunda vez la fila ya esta enabled y no actualiza ninguna.
        return jdbcTemplate.update("UPDATE users SET username = ?, password_hash = ?, enabled = TRUE "
                        + "WHERE id = ? AND enabled = FALSE", username, passwordHash, id) == 1;
    }

    @Override
    public Optional<User> updateUsername(final long id, final String username) {
        if (jdbcTemplate.update("UPDATE users SET username = ? WHERE id = ?", username, id) != 1) {
            return Optional.empty();
        }
        return findById(id);
    }

    @Override
    public Optional<User> updatePasswordIfMatches(final long id, final String expectedPasswordHash,
                                                  final String newPasswordHash) {
        // El WHERE sobre el hash vigente evita que un formulario desactualizado pise una clave elegida despues.
        if (jdbcTemplate.update("UPDATE users SET password_hash = ? WHERE id = ? AND password_hash = ?",
                newPasswordHash, id, expectedPasswordHash) != 1) {
            return Optional.empty();
        }
        return findById(id);
    }

    /*
     * Sin WHERE sobre el hash vigente: quien recupera la clave justamente no lo conoce.
     * Lo que autoriza el cambio es el token que llego al correo, y eso lo valida el service.
     */
    @Override
    public Optional<User> updatePassword(final long id, final String newPasswordHash) {
        if (jdbcTemplate.update("UPDATE users SET password_hash = ? WHERE id = ?", newPasswordHash, id) != 1) {
            return Optional.empty();
        }
        return findById(id);
    }

    private static String normalize(final String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
