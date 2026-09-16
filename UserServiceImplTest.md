---
title: "UserServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# UserServiceImplTest

Service tests with mocks or a capturing mail sender. Direct construction does not activate transaction or async proxies. Source evidence for [[UserServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testRegisterWhenEmailIsNewReturnsPendingUserWithNormalizedEmail`
- `testRegisterWhenAccountIsPendingReturnsExistingUserWithoutCreatingAnother`
- `testRegisterWhenAccountIsAlreadyEnabledThrowsDuplicateUserException`
- `testRegisterWhenAnotherRequestInsertedTheSameEmailThrowsDuplicateUserException`
- `testVerifyEmailWhenTokenIsValidReturnsActivatedUserWithChosenCredentials`
- `testVerifyEmailWhenTokenIsUnknownReturnsEmpty`
- `testVerifyEmailWhenAccountWasAlreadyActivatedReturnsEmpty`
- `testVerifyEmailWhenTokenIsMissingReturnsEmpty`

## Connections

Project types referenced: [[DuplicateUserException]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[PasswordHasher]], [[User]], [[UserDao]], [[UserRole]], [[UserServiceImpl]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java, lines 1–188](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.UserDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DuplicateKeyException;

import java.util.Locale;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class UserServiceImplTest {

    private static final Locale LOCALE = Locale.ENGLISH;
    private static final String LANGUAGE = "en";
    private static final long PENDING_USER_ID = 3;
    private static final String PENDING_EMAIL = "legacy@example.com";
    private static final String NEW_EMAIL = "publisher@example.com";
    private static final String TOKEN = "pending-user-verification-token";
    private static final String CHOSEN_USERNAME = "mailbox-owner";
    private static final String RAW_PASSWORD = "ViniloDemo2026!";
    private static final String PASSWORD_HASH = "$2a$12$hash-of-the-chosen-password";

    @Mock
    private UserDao userDao;

    @Mock
    private EmailVerificationTokenDao verificationTokenDao;

    @Mock
    private EmailService emailService;

    @Mock
    private PasswordHasher passwordHasher;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    public void testRegisterWhenEmailIsNewReturnsPendingUserWithNormalizedEmail() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.empty());
        // El DAO devuelve lo que se le pidio guardar, asi que el usuario devuelto muestra
        // con que argumentos se creo la cuenta.
        Mockito.when(userDao.create(NEW_EMAIL, NEW_EMAIL, null, UserRole.USER, LANGUAGE))
                .thenReturn(pendingUser(1, NEW_EMAIL, NEW_EMAIL, LANGUAGE));

        // 2. Exercise
        final User result = userService.register("  Publisher@Example.COM  ", LOCALE);

        // 3. Assert
        Assertions.assertEquals(NEW_EMAIL, result.getEmail());
        Assertions.assertEquals(NEW_EMAIL, result.getUsername());
        Assertions.assertNull(result.getPasswordHash());
        Assertions.assertFalse(result.isEnabled());
        Assertions.assertEquals(LANGUAGE, result.getPreferredLocale());
    }

    @Test
    public void testRegisterWhenAccountIsPendingReturnsExistingUserWithoutCreatingAnother() {
        // 1. Arrange
        final User pending = pendingUser(PENDING_USER_ID, "legacy", PENDING_EMAIL, LANGUAGE);
        Mockito.when(userDao.findByEmail(PENDING_EMAIL)).thenReturn(Optional.of(pending));

        // 2. Exercise
        final User result = userService.register(PENDING_EMAIL, LOCALE);

        // 3. Assert
        Assertions.assertEquals(PENDING_USER_ID, result.getId());
        Assertions.assertEquals("legacy", result.getUsername());
        Assertions.assertNull(result.getPasswordHash());
        Assertions.assertFalse(result.isEnabled());
    }

    @Test
    public void testRegisterWhenAccountIsAlreadyEnabledThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(enabledUser()));

        // 2. Exercise
        final Executable register = () -> userService.register(NEW_EMAIL, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
    }

    @Test
    public void testRegisterWhenAnotherRequestInsertedTheSameEmailThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.empty());
        Mockito.when(userDao.create(NEW_EMAIL, NEW_EMAIL, null, UserRole.USER, LANGUAGE))
                .thenThrow(new DuplicateKeyException("users_email_key"));

        // 2. Exercise
        final Executable register = () -> userService.register(NEW_EMAIL, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
    }

    @Test
    public void testVerifyEmailWhenTokenIsValidReturnsActivatedUserWithChosenCredentials() {
        // 1. Arrange
        Mockito.when(verificationTokenDao.findByToken(TOKEN))
                .thenReturn(Optional.of(new EmailVerificationToken(1, PENDING_USER_ID, TOKEN)));
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        // Solo activa si le llegan exactamente el usuario recortado y el hash elegido.
        Mockito.when(userDao.activateIfPending(PENDING_USER_ID, CHOSEN_USERNAME, PASSWORD_HASH))
                .thenReturn(true);
        Mockito.when(userDao.findById(PENDING_USER_ID))
                .thenReturn(Optional.of(activatedUser(CHOSEN_USERNAME, PASSWORD_HASH)));

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(
                TOKEN, "  " + CHOSEN_USERNAME + "  ", RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(CHOSEN_USERNAME, result.get().getUsername());
        Assertions.assertEquals(PASSWORD_HASH, result.get().getPasswordHash());
        Assertions.assertTrue(result.get().isEnabled());
    }

    @Test
    public void testVerifyEmailWhenTokenIsUnknownReturnsEmpty() {
        // 1. Arrange
        Mockito.when(verificationTokenDao.findByToken(TOKEN)).thenReturn(Optional.empty());

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(
                TOKEN, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testVerifyEmailWhenAccountWasAlreadyActivatedReturnsEmpty() {
        // 1. Arrange
        Mockito.when(verificationTokenDao.findByToken(TOKEN))
                .thenReturn(Optional.of(new EmailVerificationToken(1, PENDING_USER_ID, TOKEN)));
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        Mockito.when(userDao.activateIfPending(PENDING_USER_ID, CHOSEN_USERNAME, PASSWORD_HASH))
                .thenReturn(false);

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(
                TOKEN, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testVerifyEmailWhenTokenIsMissingReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(
                null, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    private static User pendingUser(final long id, final String username, final String email,
                                    final String preferredLocale) {
        return new User(id, username, email, null, UserRole.USER, false, preferredLocale);
    }

    private static User enabledUser() {
        return new User(1, "publisher", NEW_EMAIL, "$2a$12$another-hash", UserRole.USER, true, LANGUAGE);
    }

    private static User activatedUser(final String username, final String passwordHash) {
        return new User(PENDING_USER_ID, username, PENDING_EMAIL, passwordHash, UserRole.USER, true, LANGUAGE);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
