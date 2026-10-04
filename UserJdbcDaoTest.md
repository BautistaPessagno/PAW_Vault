---
title: "UserJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java"]
---

# UserJdbcDaoTest

Tests de `UserJdbcDao` en `persistence`: 27 casos declarados. Cubre: altas, búsquedas por correo normalizado y las actualizaciones condicionales de la Cuenta (`completePending`, `markVerified`, cambio de clave). No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `USERS_TABLE`, `USER_ID`, `USERNAME`, `USER_EMAIL`, `PASSWORD_HASH`, `PENDING_USER_ID`, `UNVERIFIED_USER_ID`, `UNVERIFIED_PASSWORD_HASH`, `userDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `sqlString`.

Casos declarados: 27.

- `testFindPublicProfileByIdWhenUserIsEnabledReturnsPublicFields`
- `testFindPublicProfileByIdWhenUserIsPendingReturnsEmpty`
- `testFindAccountAppearanceByIdWhenUserIsPendingReturnsAvatarFieldsForOwnProfile`
- `testFindAccountAppearanceByIdForUpdateWhenUserHasAvatarReturnsAvatarId`
- `testFindAccountAppearanceByIdForUpdateWhenUserDoesNotExistReturnsEmpty`
- `testUpdateAvatarImageIdWhenUserExistsReturnsTrueAndPersistsImage`
- `testUpdateAvatarImageIdWhenImageIsNullReturnsTrueAndRemovesAvatar`
- `testUpdateAvatarImageIdWhenUserDoesNotExistReturnsFalse`
- `testFindByIdWhenUserExistsReturnsUser`
- `testFindByIdWhenUserDoesNotExistReturnsEmpty`
- `testFindByIdForUpdateWhenUserExistsReturnsUser`
- `testFindByIdForUpdateWhenUserDoesNotExistReturnsEmpty`
- `testFindByEmailWhenEmailIsUnnormalizedReturnsExistingUser`
- `testCreateWhenUserIsNewReturnsPersistedUnverifiedNormalizedUser`
- `testCompletePendingWhenUserHasNoPasswordReturnsTrueAndKeepsItUnverified`
- `testCompletePendingWhenUserAlreadyHasPasswordReturnsFalseAndPreservesCredentials`
- `testMarkVerifiedWhenUserIsUnverifiedReturnsTrueAndPersistsIt`
- `testMarkVerifiedWhenUserIsAlreadyVerifiedReturnsFalse`
- `testUpdateUsernameWhenUserExistsReturnsUpdatedUserAndPreservesAccountData`
- `testUpdateUsernameWhenUserDoesNotExistReturnsEmptyAndPreservesUsers`
- `testUpdatePasswordIfMatchesWhenExpectedHashIsCurrentReturnsUserWithNewHashAndPersistsIt`
- `testUpdatePasswordIfMatchesWhenExpectedHashIsStaleReturnsEmptyAndPreservesHash`
- `testUpdatePasswordWhenUserExistsReturnsUserWithNewHash`
- `testUpdatePasswordWhenUserDoesNotExistReturnsEmpty`
- `testFindByIdWhenUserHasPaymentInfoReturnsCbuAndAlias`
- `testUpdatePaymentInfoWhenUserExistsReturnsUserWithNewPaymentInfo`
- `testUpdatePaymentInfoWhenUserDoesNotExistReturnsEmpty`

## Conexiones

Referencias estáticas a tipos del proyecto: [[PaymentInfo]], [[PublicUserProfile]], [[TestConfiguration]], [[User]], [[UserDao]], [[UserRole]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java>), líneas 1–441.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.models.PublicUserProfile;
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
    private static final long PENDING_USER_ID = 3;
    private static final long UNVERIFIED_USER_ID = 7;
    private static final String UNVERIFIED_PASSWORD_HASH = "$2a$12$hash-of-an-unverified-account";

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
    public void testFindPublicProfileByIdWhenUserIsEnabledReturnsPublicFields() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PublicUserProfile> result = userDao.findPublicProfileById(USER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(USER_ID, result.get().getId());
        Assertions.assertEquals(USERNAME, result.get().getUsername());
        Assertions.assertNull(result.get().getAvatarImageId());
    }

    @Test
    public void testFindPublicProfileByIdWhenUserIsPendingReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PublicUserProfile> result = userDao.findPublicProfileById(3);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindAccountAppearanceByIdWhenUserIsPendingReturnsAvatarFieldsForOwnProfile() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PublicUserProfile> result = userDao.findAccountAppearanceById(3);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals("legacy", result.get().getUsername());
        Assertions.assertNull(result.get().getAvatarImageId());
    }

    @Test
    public void testFindAccountAppearanceByIdForUpdateWhenUserHasAvatarReturnsAvatarId() {
        // 1. Arrange
        final long userWithAvatarId = 6;
        final long avatarImageId = 6;

        // 2. Exercise
        final Optional<PublicUserProfile> result = userDao.findAccountAppearanceByIdForUpdate(userWithAvatarId);

        // 3. Assert
        Assertions.assertEquals(avatarImageId, result.orElseThrow().getAvatarImageId());
    }

    @Test
    public void testFindAccountAppearanceByIdForUpdateWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<PublicUserProfile> result = userDao.findAccountAppearanceByIdForUpdate(missingId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testUpdateAvatarImageIdWhenUserExistsReturnsTrueAndPersistsImage() {
        // 1. Arrange
        final long unreferencedImageId = 3;

        // 2. Exercise
        final boolean updated = userDao.updateAvatarImageId(USER_ID, unreferencedImageId);

        // 3. Assert
        Assertions.assertTrue(updated);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND avatar_image_id = " + unreferencedImageId));
    }

    @Test
    public void testUpdateAvatarImageIdWhenImageIsNullReturnsTrueAndRemovesAvatar() {
        // 1. Arrange
        final long userWithAvatarId = 6;

        // 2. Exercise
        final boolean removed = userDao.updateAvatarImageId(userWithAvatarId, null);

        // 3. Assert
        Assertions.assertTrue(removed);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + userWithAvatarId + " AND avatar_image_id IS NULL"));
    }

    @Test
    public void testUpdateAvatarImageIdWhenUserDoesNotExistReturnsFalse() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final boolean updated = userDao.updateAvatarImageId(missingId, null);

        // 3. Assert
        Assertions.assertFalse(updated);
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
        Assertions.assertTrue(result.get().isVerified());
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
    public void testFindByIdForUpdateWhenUserExistsReturnsUser() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userDao.findByIdForUpdate(USER_ID);

        // 3. Assert
        Assertions.assertEquals(USERNAME, result.get().getUsername());
    }

    @Test
    public void testFindByIdForUpdateWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<User> result = userDao.findByIdForUpdate(missingId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
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
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testCreateWhenUserIsNewReturnsPersistedUnverifiedNormalizedUser() {
        // 1. Arrange
        final String username = "publisher";
        final String email = "  Publisher@Example.COM  ";
        final String normalizedEmail = "publisher@example.com";

        // 2. Exercise
        final User result = userDao.create(username, email, PASSWORD_HASH, UserRole.USER, "fr");

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(username, result.getUsername());
        Assertions.assertEquals(normalizedEmail, result.getEmail());
        Assertions.assertEquals(PASSWORD_HASH, result.getPasswordHash());
        Assertions.assertEquals(UserRole.USER, result.getRole());
        Assertions.assertFalse(result.isVerified());
        Assertions.assertEquals("fr", result.getPreferredLocale());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + result.getId() + " AND username = " + sqlString(username)
                        + " AND email = " + sqlString(normalizedEmail)
                        + " AND role = " + sqlString(UserRole.USER.name())
                        + " AND password_hash = " + sqlString(PASSWORD_HASH)
                        + " AND verified = FALSE AND preferred_locale = 'fr'"));
        Assertions.assertEquals(8, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testCompletePendingWhenUserHasNoPasswordReturnsTrueAndKeepsItUnverified() {
        // 1. Arrange
        final String username = "claimed-user";

        // 2. Exercise
        final boolean completed = userDao.completePending(PENDING_USER_ID, username, PASSWORD_HASH);

        // 3. Assert
        Assertions.assertTrue(completed);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + PENDING_USER_ID + " AND username = " + sqlString(username)
                        + " AND password_hash = " + sqlString(PASSWORD_HASH) + " AND verified = FALSE"));
    }

    @Test
    public void testCompletePendingWhenUserAlreadyHasPasswordReturnsFalseAndPreservesCredentials() {
        // 1. Arrange
        final String replacementHash = "$2a$12$replacement";

        // 2. Exercise
        final boolean completed = userDao.completePending(UNVERIFIED_USER_ID, "attacker", replacementHash);

        // 3. Assert
        Assertions.assertFalse(completed);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + UNVERIFIED_USER_ID + " AND username = 'unverified'"
                        + " AND password_hash = " + sqlString(UNVERIFIED_PASSWORD_HASH)));
    }

    @Test
    public void testMarkVerifiedWhenUserIsUnverifiedReturnsTrueAndPersistsIt() {
        // 1. Arrange

        // 2. Exercise
        final boolean verified = userDao.markVerified(UNVERIFIED_USER_ID);

        // 3. Assert
        Assertions.assertTrue(verified);
        Assertions.assertTrue(userDao.findById(UNVERIFIED_USER_ID).orElseThrow().isVerified());
    }

    @Test
    public void testMarkVerifiedWhenUserIsAlreadyVerifiedReturnsFalse() {
        // 1. Arrange

        // 2. Exercise
        final boolean verified = userDao.markVerified(USER_ID);

        // 3. Assert
        Assertions.assertFalse(verified);
        Assertions.assertTrue(userDao.findById(USER_ID).orElseThrow().isVerified());
    }

    @Test
    public void testUpdateUsernameWhenUserExistsReturnsUpdatedUserAndPreservesAccountData() {
        // 1. Arrange
        final String updatedUsername = "nuevo nombre";

        // 2. Exercise
        final Optional<User> result = userDao.updateUsername(USER_ID, updatedUsername);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(updatedUsername, result.get().getUsername());
        Assertions.assertEquals(USER_EMAIL, result.get().getEmail());
        Assertions.assertEquals(PASSWORD_HASH, result.get().getPasswordHash());
        Assertions.assertEquals(UserRole.USER, result.get().getRole());
        Assertions.assertTrue(result.get().isVerified());
        Assertions.assertEquals("es", result.get().getPreferredLocale());
    }

    @Test
    public void testUpdateUsernameWhenUserDoesNotExistReturnsEmptyAndPreservesUsers() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<User> result = userDao.updateUsername(missingId, "nadie");

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
    }

    @Test
    public void testUpdatePasswordIfMatchesWhenExpectedHashIsCurrentReturnsUserWithNewHashAndPersistsIt() {
        // 1. Arrange
        final String newHash = "$2a$12$replacement";

        // 2. Exercise
        final Optional<User> result = userDao.updatePasswordIfMatches(USER_ID, PASSWORD_HASH, newHash);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(newHash, result.get().getPasswordHash());
        Assertions.assertEquals(USERNAME, result.get().getUsername());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND username = " + sqlString(USERNAME)
                        + " AND email = " + sqlString(USER_EMAIL)
                        + " AND password_hash = " + sqlString(newHash)
                        + " AND role = 'USER' AND verified = TRUE AND preferred_locale = 'es'"));
    }

    @Test
    public void testUpdatePasswordIfMatchesWhenExpectedHashIsStaleReturnsEmptyAndPreservesHash() {
        // 1. Arrange
        final String staleHash = "$2a$12$stale";

        // 2. Exercise
        final Optional<User> result = userDao.updatePasswordIfMatches(USER_ID, staleHash, "$2a$12$replacement");

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND password_hash = " + sqlString(PASSWORD_HASH)));
    }

    @Test
    public void testUpdatePasswordWhenUserExistsReturnsUserWithNewHash() {
        // 1. Arrange
        final String newHash = "$2a$12$hash-chosen-while-recovering";

        // 2. Exercise
        final Optional<User> result = userDao.updatePassword(USER_ID, newHash);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(newHash, result.get().getPasswordHash());
        Assertions.assertEquals(USERNAME, result.get().getUsername());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND username = " + sqlString(USERNAME)
                        + " AND email = " + sqlString(USER_EMAIL)
                        + " AND password_hash = " + sqlString(newHash)
                        + " AND role = 'USER' AND verified = TRUE AND preferred_locale = 'es'"));
    }

    @Test
    public void testUpdatePasswordWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingUserId = 999;

        // 2. Exercise
        final Optional<User> result = userDao.updatePassword(missingUserId, "$2a$12$replacement");

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = " + USER_ID + " AND password_hash = " + sqlString(PASSWORD_HASH)));
    }

    @Test
    public void testFindByIdWhenUserHasPaymentInfoReturnsCbuAndAlias() {
        // 1. Arrange
        final long userId = 1;

        // 2. Exercise
        final Optional<User> result = userDao.findById(userId);

        // 3. Assert
        Assertions.assertEquals("2850590940090418135201", result.get().getPaymentInfo().getCbu());
        Assertions.assertEquals("bruno.vinilos", result.get().getPaymentInfo().getAlias());
    }

    @Test
    public void testUpdatePaymentInfoWhenUserExistsReturnsUserWithNewPaymentInfo() {
        // 1. Arrange
        final long userId = 2;

        // 2. Exercise
        final Optional<User> result = userDao.updatePaymentInfo(userId, new PaymentInfo(null, "tomi.discos"));

        // 3. Assert
        Assertions.assertEquals("tomi.discos", result.get().getPaymentInfo().getAlias());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, USERS_TABLE,
                "id = 2 AND alias = 'tomi.discos' AND cbu IS NULL"));
    }

    @Test
    public void testUpdatePaymentInfoWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingUserId = 999;

        // 2. Exercise
        final Optional<User> result = userDao.updatePaymentInfo(missingUserId, new PaymentInfo(null, "tomi.discos"));

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```
