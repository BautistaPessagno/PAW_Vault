---
title: "EmailVerificationTokenJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java"]
---

# EmailVerificationTokenJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[EmailVerificationTokenJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindByTokenWhenTokenExistsReturnsAllPersistedFields`
- `testFindByTokenWhenTokenDoesNotExistReturnsEmpty`
- `testCreateWhenTokenIsNewReturnsPersistedToken`
- `testDeleteByUserIdWhenUserHasTokensReturnsCountAndEmptyLookup`

## Connections

Project types referenced: [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java, lines 1–101](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java>)

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
        final EmailVerificationToken result = tokenDao.create(USER_WITHOUT_TOKEN_ID, NEW_TOKEN);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(USER_WITHOUT_TOKEN_ID, result.getUserId());
        Assertions.assertEquals(NEW_TOKEN, result.getToken());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, TABLE,
                "id = " + result.getId() + " AND user_id = " + USER_WITHOUT_TOKEN_ID
                        + " AND token = " + sqlString(NEW_TOKEN)));
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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
