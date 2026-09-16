---
title: "UserJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java"]
---

# UserJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[UserJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindByIdWhenUserExistsReturnsUser`
- `testFindByIdWhenUserDoesNotExistReturnsEmpty`
- `testFindByEmailWhenEmailIsUnnormalizedReturnsExistingUser`
- `testCreateWhenUserIsNewReturnsPersistedNormalizedUser`
- `testActivateIfPendingWhenUserIsPendingReturnsTrueAndEnabledUser`
- `testActivateIfPendingWhenUserIsAlreadyEnabledReturnsFalseAndPreservesCredentials`

## Connections

Project types referenced: [[TestConfiguration]], [[User]], [[UserDao]], [[UserRole]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java, lines 1–151](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
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
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class UserJdbcDaoTest {

    private static final String USERS_TABLE = "users";
    private static final long USER_ID = 1;
    private static final String USERNAME = "bpessagno";
    private static final String USER_EMAIL = "bpessagno@itba.edu.ar";
    private static final String PASSWORD_HASH = "$2a$12$FpiCwPCeBQTF3ihFUejq2Oz4HO.SYw2n4z1fgYoZ3bpZI67EDcIFm";

    @Autowired
    private UserDao userDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByIdWhenUserExistsReturnsUser() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userDao.findById(USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(USER_ID, result.get().getId());
        Assertions.assertEquals(USERNAME, result.get().getUsername());
        Assertions.assertEquals(USER_EMAIL, result.get().getEmail());
        Assertions.assertEquals(PASSWORD_HASH, result.get().getPasswordHash());
        Assertions.assertEquals(UserRole.USER, result.get().getRole());
        Assertions.assertTrue(result.get().isEnabled());
    }

    @Test
    public void testFindByIdWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<User> result = userDao.findById(missingId);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testFindByEmailWhenEmailIsUnnormalizedReturnsExistingUser() {
        // 1. Arrange
        final String unnormalizedEmail = "  BPESSAGNO@ITBA.EDU.AR  ";

        // 2. Exercise
        final Optional<User> result = userDao.findByEmail(unnormalizedEmail);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(USER_ID, result.get().getId());
        Assertions.assertEquals(USERNAME, result.get().getUsername());
        Assertions.assertEquals(USER_EMAIL, result.get().getEmail());
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testCreateWhenUserIsNewReturnsPersistedNormalizedUser() {
        // 1. Arrange
        final String username = "publisher";
        final String email = "  Publisher@Example.COM  ";
        final String normalizedEmail = "publisher@example.com";

        // 2. Exercise
        final User result = userDao.create(username, email, null, UserRole.USER, "fr");

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(username, result.getUsername());
        Assertions.assertEquals(normalizedEmail, result.getEmail());
        Assertions.assertNull(result.getPasswordHash());
        Assertions.assertEquals(UserRole.USER, result.getRole());
        Assertions.assertFalse(result.isEnabled());
        Assertions.assertEquals("fr", result.getPreferredLocale());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + result.getId() + " AND username = " + sqlString(username)
                        + " AND email = " + sqlString(normalizedEmail)
                        + " AND role = " + sqlString(UserRole.USER.name())
                        + " AND password_hash IS NULL AND enabled = FALSE AND preferred_locale = 'fr'"));
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testActivateIfPendingWhenUserIsPendingReturnsTrueAndEnabledUser() {
        // 1. Arrange
        final long legacyUserId = 3;
        final String username = "claimed-user";

        // 2. Exercise
        final boolean activated = userDao.activateIfPending(legacyUserId, username, PASSWORD_HASH);

        // 3. Assert
        Assertions.assertTrue(activated);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + legacyUserId + " AND username = " + sqlString(username)
                        + " AND password_hash = " + sqlString(PASSWORD_HASH) + " AND enabled = TRUE"));
    }

    @Test
    public void testActivateIfPendingWhenUserIsAlreadyEnabledReturnsFalseAndPreservesCredentials() {
        // 1. Arrange
        final String replacementUsername = "attacker";
        final String replacementHash = "$2a$12$replacement";

        // 2. Exercise
        final boolean activated = userDao.activateIfPending(USER_ID, replacementUsername, replacementHash);

        // 3. Assert
        Assertions.assertFalse(activated);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND username = " + sqlString(USERNAME)
                        + " AND password_hash = " + sqlString(PASSWORD_HASH) + " AND enabled = TRUE"));
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
