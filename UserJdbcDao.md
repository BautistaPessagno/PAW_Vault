---
title: "UserJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java"]
---

# UserJdbcDao

Cuentas con Spring JDBC. Normaliza el correo al buscar y al crear. Los `UPDATE` condicionales (`WHERE password_hash IS NULL`, `WHERE verified = FALSE`, `WHERE password_hash = ?`) hacen que el pedido que pierde una carrera no pise al que ganó. `FOR UPDATE` para los bloqueos de fila.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `PUBLIC_PROFILE_MAPPER`, `USER_SELECT`, `PUBLIC_PROFILE_SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `findById`, `findPublicProfileById`, `findAccountAppearanceById`, `findAccountAppearanceByIdForUpdate`, `updateAvatarImageId`, `findByIdForUpdate`, `findByEmail`, `create`, `completePending`, `markVerified`, `updateUsername`, `updatePasswordIfMatches`, `updatePassword`, `updatePaymentInfo`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[EmailRules]], [[PaymentInfo]], [[PublicUserProfile]], [[User]], [[UserDao]], [[UserRole]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>), líneas 1–170.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailRules;
import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.UserRole;
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
public class UserJdbcDao implements UserDao {

    private static final RowMapper<User> ROW_MAPPER = (resultSet, rowNum) -> new User(
            resultSet.getLong("user_id"),
            resultSet.getString("user_username"),
            resultSet.getString("user_email"),
            resultSet.getString("user_password_hash"),
            UserRole.valueOf(resultSet.getString("user_role")),
            resultSet.getBoolean("user_verified"),
            resultSet.getString("user_preferred_locale"),
            new PaymentInfo(resultSet.getString("user_cbu"), resultSet.getString("user_alias"))
    );

    private static final RowMapper<PublicUserProfile> PUBLIC_PROFILE_MAPPER = (resultSet, rowNum) -> {
        final Number avatarImageId = (Number) resultSet.getObject("avatar_image_id");
        return new PublicUserProfile(resultSet.getLong("id"), resultSet.getString("username"),
                avatarImageId == null ? null : avatarImageId.longValue());
    };

    private static final String USER_SELECT =
            "SELECT id AS user_id, username AS user_username, email AS user_email, " +
                    "password_hash AS user_password_hash, role AS user_role, verified AS user_verified, "
                    + "preferred_locale AS user_preferred_locale, cbu AS user_cbu, alias AS user_alias FROM users ";

    private static final String PUBLIC_PROFILE_SELECT = "SELECT id, username, avatar_image_id FROM users ";

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
    public Optional<PublicUserProfile> findPublicProfileById(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ? AND verified = TRUE",
                        PUBLIC_PROFILE_MAPPER, id)
                .stream().findAny();
    }

    @Override
    public Optional<PublicUserProfile> findAccountAppearanceById(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ?",
                PUBLIC_PROFILE_MAPPER, id).stream().findAny();
    }

    @Override
    public Optional<PublicUserProfile> findAccountAppearanceByIdForUpdate(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ? FOR UPDATE",
                PUBLIC_PROFILE_MAPPER, id).stream().findAny();
    }

    @Override
    public boolean updateAvatarImageId(final long id, final Long imageId) {
        return jdbcTemplate.update("UPDATE users SET avatar_image_id = ? WHERE id = ?", imageId, id) == 1;
    }

    @Override
    public Optional<User> findByIdForUpdate(final long id) {
        return jdbcTemplate.query(USER_SELECT + "WHERE id = ? FOR UPDATE", ROW_MAPPER, id)
                .stream()
                .findAny();
    }

    @Override
    public Optional<User> findByEmail(final String email) {
        return jdbcTemplate.query(USER_SELECT + "WHERE email = ?", ROW_MAPPER, EmailRules.normalize(email))
                .stream()
                .findAny();
    }

    @Override
    public User create(final String username, final String email, final String passwordHash, final UserRole role,
                       final String preferredLocale) {
        final String normalizedEmail = EmailRules.normalize(email);
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("username", username);
        parameters.put("email", normalizedEmail);
        parameters.put("password_hash", passwordHash);
        parameters.put("role", role.name());
        parameters.put("verified", false);
        parameters.put("preferred_locale", preferredLocale);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new User(id.longValue(), username, normalizedEmail, passwordHash, role, false, preferredLocale);
    }

    @Override
    public boolean completePending(final long id, final String username, final String passwordHash) {
        // El UPDATE condicional hace que solo el primer registro complete la cuenta pendiente:
        // despues la fila ya tiene clave y un segundo registro no la pisa.
        return jdbcTemplate.update("UPDATE users SET username = ?, password_hash = ? "
                        + "WHERE id = ? AND password_hash IS NULL", username, passwordHash, id) == 1;
    }

    @Override
    public boolean markVerified(final long id) {
        return jdbcTemplate.update("UPDATE users SET verified = TRUE WHERE id = ? AND verified = FALSE", id) == 1;
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

    @Override
    public Optional<User> updatePaymentInfo(final long id, final PaymentInfo paymentInfo) {
        if (jdbcTemplate.update("UPDATE users SET cbu = ?, alias = ? WHERE id = ?",
                paymentInfo.getCbu(), paymentInfo.getAlias(), id) != 1) {
            return Optional.empty();
        }
        return findById(id);
    }
}
```
