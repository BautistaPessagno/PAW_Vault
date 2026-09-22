---
title: "PasswordResetTokenJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDaoTest.java"]
---

# PasswordResetTokenJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[PasswordResetTokenJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindByTokenWhenTokenExistsReturnsAllPersistedFields`
- `testFindByTokenWhenTokenIsExpiredReturnsTokenWithPastExpiration`
- `testFindByTokenWhenTokenDoesNotExistReturnsEmpty`
- `testCreateWhenTokenIsNewReturnsPersistedToken`
- `testCreateWhenUserAlreadyHasATokenThrowsDuplicateKeyExceptionWithoutPersistingIt`
- `testDeleteExpiredWhenThereAreExpiredTokensReturnsCountAndKeepsTheLiveOnes`
- `testDeleteByUserIdWhenUserHasTokensReturnsCountAndEmptyLookup`
- `testDeleteByTokenWhenTokenExistsReturnsOneAndRemovesIt`
- `testDeleteByUserIdWhenUserHasNoTokensReturnsZeroAndLeavesOtherTokensUntouched`

## Connections

Project types referenced: [[PasswordResetToken]], [[PasswordResetTokenDao]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDaoTest.java, lines 1–189](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PasswordResetToken;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
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
public class PasswordResetTokenJdbcDaoTest {

    private static final String TABLE = "password_reset_tokens";
    private static final long TOKEN_OWNER_ID = 1;
    private static final long EXPIRED_TOKEN_OWNER_ID = 2;
    private static final long USER_WITHOUT_TOKEN_ID = 3;
    private static final long LIVE_TOKEN_ID = 1;
    private static final String LIVE_TOKEN = "live-password-reset-token";
    private static final String EXPIRED_TOKEN = "expired-password-reset-token";
    private static final String NEW_TOKEN = "a-brand-new-password-reset-token";
    private static final LocalDateTime LIVE_EXPIRES_AT = LocalDateTime.of(2999, 1, 1, 0, 0);
    private static final LocalDateTime EXPIRED_EXPIRES_AT = LocalDateTime.of(2020, 1, 1, 0, 0);

    @Autowired
    private PasswordResetTokenDao tokenDao;

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
        final Optional<PasswordResetToken> result = tokenDao.findByToken(LIVE_TOKEN);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(LIVE_TOKEN_ID, result.get().getId());
        Assertions.assertEquals(TOKEN_OWNER_ID, result.get().getUserId());
        Assertions.assertEquals(LIVE_TOKEN, result.get().getToken());
        Assertions.assertEquals(LIVE_EXPIRES_AT, result.get().getExpiresAt());
    }

    /*
     * Un token vencido sigue siendo una fila como cualquier otra: descartarlo es decision
     * del service, asi que el DAO tiene que devolverlo con su fecha para que pueda hacerlo.
     */
    @Test
    public void testFindByTokenWhenTokenIsExpiredReturnsTokenWithPastExpiration() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PasswordResetToken> result = tokenDao.findByToken(EXPIRED_TOKEN);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(EXPIRED_TOKEN_OWNER_ID, result.get().getUserId());
        Assertions.assertEquals(EXPIRED_EXPIRES_AT, result.get().getExpiresAt());
    }

    @Test
    public void testFindByTokenWhenTokenDoesNotExistReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PasswordResetToken> result = tokenDao.findByToken(NEW_TOKEN);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testCreateWhenTokenIsNewReturnsPersistedToken() {
        // 1. Arrange
        final LocalDateTime expiresAt = LocalDateTime.of(2030, 6, 15, 10, 30);

        // 2. Exercise
        final PasswordResetToken result = tokenDao.create(USER_WITHOUT_TOKEN_ID, NEW_TOKEN, expiresAt);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(USER_WITHOUT_TOKEN_ID, result.getUserId());
        Assertions.assertEquals(NEW_TOKEN, result.getToken());
        Assertions.assertEquals(expiresAt, result.getExpiresAt());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "id = " + result.getId() + " AND user_id = " + USER_WITHOUT_TOKEN_ID
                        + " AND token = " + sqlString(NEW_TOKEN)
                        + " AND expires_at = TIMESTAMP '2030-06-15 10:30:00'"));
    }

    /*
     * La unicidad de user_id es la que garantiza un solo enlace vivo por cuenta: sin ella
     * dos pedidos simultaneos para el mismo correo dejarian dos tokens utilizables.
     */
    @Test
    public void testCreateWhenUserAlreadyHasATokenThrowsDuplicateKeyExceptionWithoutPersistingIt() {
        // 1. Arrange
        final LocalDateTime expiresAt = LocalDateTime.of(2030, 6, 15, 10, 30);

        // 2. Exercise
        final Executable create = () -> tokenDao.create(TOKEN_OWNER_ID, NEW_TOKEN, expiresAt);

        // 3. Assert
        Assertions.assertThrows(DuplicateKeyException.class, create);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(NEW_TOKEN)));
    }

    @Test
    public void testDeleteExpiredWhenThereAreExpiredTokensReturnsCountAndKeepsTheLiveOnes() {
        // 1. Arrange

        // 2. Exercise
        final int deleted = tokenDao.deleteExpired(LocalDateTime.of(2026, 1, 1, 0, 0));

        // 3. Assert
        Assertions.assertEquals(1, deleted);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(EXPIRED_TOKEN)));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(LIVE_TOKEN)));
    }

    @Test
    public void testDeleteByUserIdWhenUserHasTokensReturnsCountAndEmptyLookup() {
        // 1. Arrange

        // 2. Exercise
        final int deleted = tokenDao.deleteByUserId(TOKEN_OWNER_ID);

        // 3. Assert
        Assertions.assertEquals(1, deleted);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(LIVE_TOKEN)));
    }

    @Test
    public void testDeleteByTokenWhenTokenExistsReturnsOneAndRemovesIt() {
        // 1. Arrange

        // 2. Exercise
        final int deleted = tokenDao.deleteByToken(LIVE_TOKEN);

        // 3. Assert
        Assertions.assertEquals(1, deleted);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(LIVE_TOKEN)));
    }

    @Test
    public void testDeleteByUserIdWhenUserHasNoTokensReturnsZeroAndLeavesOtherTokensUntouched() {
        // 1. Arrange

        // 2. Exercise
        final int deleted = tokenDao.deleteByUserId(USER_WITHOUT_TOKEN_ID);

        // 3. Assert
        Assertions.assertEquals(0, deleted);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "token = " + sqlString(LIVE_TOKEN)));
    }

    private static String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
