---
title: "EmailVerificationTokenJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java"]
---

# EmailVerificationTokenJdbcDaoTest

Tests de `EmailVerificationTokenJdbcDao` en `persistence`: 6 casos declarados. Cubre: crear, buscar por token, último de una Cuenta y borrado de tokens de verificación. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `TABLE`, `PENDING_USER_ID`, `USER_WITHOUT_TOKEN_ID`, `EXISTING_TOKEN_ID`, `EXISTING_TOKEN`, `NEW_TOKEN`, `EXISTING_CREATED_AT`, `NEW_CREATED_AT`, `tokenDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `sqlString`.

Casos declarados: 6.

- `testFindByTokenWhenTokenExistsReturnsAllPersistedFields`
- `testFindLatestByUserIdWhenUserHasTokenReturnsIt`
- `testFindLatestByUserIdWhenUserHasNoTokenReturnsEmpty`
- `testFindByTokenWhenTokenDoesNotExistReturnsEmpty`
- `testCreateWhenTokenIsNewReturnsPersistedToken`
- `testDeleteByUserIdWhenUserHasTokensReturnsCountAndEmptyLookup`

## Conexiones

Referencias estáticas a tipos del proyecto: [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java>), líneas 1–131.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailVerificationToken;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.time.LocalDateTime;
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class EmailVerificationTokenJdbcDaoTest {

    private static final String TABLE = "email_verification_tokens";
    private static final long PENDING_USER_ID = 3;
    private static final long USER_WITHOUT_TOKEN_ID = 1;
    private static final long EXISTING_TOKEN_ID = 1;
    private static final String EXISTING_TOKEN = "pending-user-verification-token";
    private static final String NEW_TOKEN = "a-brand-new-verification-token";
    private static final LocalDateTime EXISTING_CREATED_AT = LocalDateTime.of(2026, 1, 1, 10, 0);
    private static final LocalDateTime NEW_CREATED_AT = LocalDateTime.of(2026, 9, 30, 18, 45, 12);

    @Autowired
    private EmailVerificationTokenDao tokenDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByTokenWhenTokenExistsReturnsAllPersistedFields() {
        // 1. Arrange

        // 2. Exercise
        final Optional<EmailVerificationToken> result = tokenDao.findByToken(EXISTING_TOKEN);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(EXISTING_TOKEN_ID, result.get().getId());
        Assertions.assertEquals(PENDING_USER_ID, result.get().getUserId());
        Assertions.assertEquals(EXISTING_TOKEN, result.get().getToken());
        Assertions.assertEquals(EXISTING_CREATED_AT, result.get().getCreatedAt());
    }

    @Test
    public void testFindLatestByUserIdWhenUserHasTokenReturnsIt() {
        // 1. Arrange

        // 2. Exercise
        final Optional<EmailVerificationToken> result = tokenDao.findLatestByUserId(PENDING_USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(EXISTING_TOKEN, result.get().getToken());
        Assertions.assertEquals(EXISTING_CREATED_AT, result.get().getCreatedAt());
    }

    @Test
    public void testFindLatestByUserIdWhenUserHasNoTokenReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<EmailVerificationToken> result = tokenDao.findLatestByUserId(USER_WITHOUT_TOKEN_ID);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testFindByTokenWhenTokenDoesNotExistReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<EmailVerificationToken> result = tokenDao.findByToken(NEW_TOKEN);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testCreateWhenTokenIsNewReturnsPersistedToken() {
        // 1. Arrange

        // 2. Exercise
        final EmailVerificationToken result = tokenDao.create(USER_WITHOUT_TOKEN_ID, NEW_TOKEN, NEW_CREATED_AT);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(USER_WITHOUT_TOKEN_ID, result.getUserId());
        Assertions.assertEquals(NEW_TOKEN, result.getToken());
        Assertions.assertEquals(NEW_CREATED_AT, result.getCreatedAt());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "id = " + result.getId() + " AND user_id = " + USER_WITHOUT_TOKEN_ID
                        + " AND token = " + sqlString(NEW_TOKEN)
                        + " AND created_at = TIMESTAMP '2026-09-30 18:45:12'"));
    }

    @Test
    public void testDeleteByUserIdWhenUserHasTokensReturnsCountAndEmptyLookup() {
        // 1. Arrange

        // 2. Exercise
        final int deleted = tokenDao.deleteByUserId(PENDING_USER_ID);

        // 3. Assert
        Assertions.assertEquals(1, deleted);
        Assertions.assertFalse(tokenDao.findByToken(EXISTING_TOKEN).isPresent());
    }

    private static String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```
