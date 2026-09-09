---
title: "UserJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java"]
---

# UserJdbcDaoTest

Runs the real JDBC DAO through a Spring HSQLDB context with transaction rollback. Fixture rows come from test populator.sql. Assertions inspect mapped objects and persisted row counts. This checks the test schema and DAO behavior, not production startup, PostgreSQL concurrency, JSPs or HTTP status.

Production connections: [[User]], [[UserDao]].

## Test cases

- `testFindByIdWhenUserExistsReturnsUser`
- `testFindByIdWhenUserDoesNotExistReturnsEmpty`
- `testFindOrCreateWhenUserExistsReturnsExistingUserUnchanged`
- `testFindOrCreateWhenUserIsNewReturnsPersistedNormalizedUser`

## Exact test source

[persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java, lines 1–108](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;
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
    public void testFindOrCreateWhenUserExistsReturnsExistingUserUnchanged() {
        // 1. Arrange
        final String differentUsername = "otherUsername";
        final String unnormalizedEmail = "  BPESSAGNO@ITBA.EDU.AR  ";

        // 2. Exercise
        final User result = userDao.findOrCreate(differentUsername, unnormalizedEmail);

        // 3. Assert
        Assertions.assertEquals(USER_ID, result.getId());
        Assertions.assertEquals(USERNAME, result.getUsername());
        Assertions.assertEquals(USER_EMAIL, result.getEmail());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenUserIsNewReturnsPersistedNormalizedUser() {
        // 1. Arrange
        final String username = "publisher";
        final String email = "  Publisher@Example.COM  ";
        final String normalizedEmail = "publisher@example.com";

        // 2. Exercise
        final User result = userDao.findOrCreate(username, email);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(username, result.getUsername());
        Assertions.assertEquals(normalizedEmail, result.getEmail());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + result.getId() + " AND username = " + sqlString(username)
                        + " AND email = " + sqlString(normalizedEmail)));
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
