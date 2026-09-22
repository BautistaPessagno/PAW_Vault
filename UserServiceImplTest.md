---
title: "UserServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# UserServiceImplTest

Service tests with mocks and a capturing mail service. The fixture initializes TransactionSynchronizationManager by hand and runs registered after-commit callbacks explicitly; direct construction still does not activate real transaction or async proxies. Source evidence for [[UserServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testRegisterWhenEmailIsNewReturnsPendingUserWithNormalizedEmail`
- `testRegisterWhenAccountIsPendingReturnsExistingUserWithoutCreatingAnother`
- `testRegisterWhenAccountIsAlreadyEnabledThrowsDuplicateUserException`
- `testRegisterWhenAnotherRequestInsertedTheSameEmailThrowsDuplicateUserException`
- `testVerifyEmailWhenTokenIsValidReturnsActivatedUserWithChosenCredentials`
- `testVerifyEmailWhenTokenIsUnknownReturnsEmpty`
- `testVerifyEmailWhenAccountWasAlreadyActivatedReturnsEmpty`
- `testVerifyEmailWhenTokenIsMissingReturnsEmpty`
- `testUpdateUsernameWhenValueHasSurroundingSpacesReturnsTrimmedUpdatedUser`
- `testUpdateUsernameWhenUserDoesNotExistThrowsUserNotFoundException`
- `testChangePasswordWhenCurrentPasswordMatchesReturnsUserWithNewHashAndNotifiesAfterCommit`
- `testChangePasswordWhenCurrentPasswordDoesNotMatchThrowsInvalidCurrentPasswordException`
- `testChangePasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException`
- `testChangePasswordWhenUserDoesNotExistThrowsUserNotFoundException`
- `testChangePasswordWhenHashWasReplacedConcurrentlyThrowsInvalidCurrentPasswordException`
- `testRequestPasswordResetWhenAccountIsEnabledReturnsNormallyAfterStoringTokenAndSchedulingLink`
- `testRequestPasswordResetWhenEmailIsUnknownReturnsNormallyWithoutSendingLink`
- `testRequestPasswordResetWhenAccountIsPendingReturnsNormallyWithoutSendingLink`
- `testRequestPasswordResetWhenAnotherRequestStoredItsLinkFirstReturnsNormallyWithoutSendingLink`
- `testResetPasswordWhenTokenIsValidReturnsUserWithNewHashAndNotifiesAfterCommit`
- `testResetPasswordWhenTokenIsExpiredReturnsEmptyAndLeavesPasswordUntouched`
- `testResetPasswordWhenTokenWasAlreadyConsumedReturnsEmpty`
- `testResetPasswordWhenTokenDoesNotExistReturnsEmpty`
- `testResetPasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException`
- `testResetPasswordWhenTokenIsMissingReturnsEmpty`

## Connections

Project types referenced: [[DuplicateUserException]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[InquiryAcceptedNotification]], [[InvalidCurrentPasswordException]], [[PasswordHasher]], [[PasswordResetToken]], [[PasswordResetTokenDao]], [[PostInterestNotification]], [[UnchangedPasswordException]], [[User]], [[UserDao]], [[UserNotFoundException]], [[UserRole]], [[UserServiceImpl]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java, lines 1–563](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.PasswordResetToken;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.PasswordResetTokenDao;
import ar.edu.itba.paw.persistence.UserDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.time.LocalDateTime;
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
    private static final String NEW_RAW_PASSWORD = "OtroVinilo2026!";
    private static final String NEW_PASSWORD_HASH = "$2a$12$hash-of-the-new-password";

    @Mock
    private UserDao userDao;

    @Mock
    private EmailVerificationTokenDao verificationTokenDao;

    @Mock
    private PasswordResetTokenDao resetTokenDao;

    @Mock
    private PasswordHasher passwordHasher;

    private CapturingEmailService emailService;

    private UserServiceImpl userService;

    @BeforeEach
    public void setUp() {
        emailService = new CapturingEmailService();
        userService = new UserServiceImpl(userDao, emailService, passwordHasher, verificationTokenDao,
                resetTokenDao);
        TransactionSynchronizationManager.initSynchronization();
    }

    @AfterEach
    public void tearDown() {
        TransactionSynchronizationManager.clearSynchronization();
    }

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
        Assertions.assertNull(emailService.verificationUser);
        commitTransaction();
        Assertions.assertSame(result, emailService.verificationUser);
        Assertions.assertEquals(LOCALE, emailService.verificationLocale);
        Assertions.assertNotNull(emailService.verificationToken);
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
        Assertions.assertNull(emailService.welcomeUser);
        commitTransaction();
        Assertions.assertSame(result.get(), emailService.welcomeUser);
        Assertions.assertEquals(LOCALE, emailService.welcomeLocale);
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

    @Test
    public void testUpdateUsernameWhenValueHasSurroundingSpacesReturnsTrimmedUpdatedUser() {
        // 1. Arrange
        final User updated = new User(1, CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH,
                UserRole.USER, true, LANGUAGE);
        Mockito.when(userDao.updateUsername(1, CHOSEN_USERNAME)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final User result = userService.updateUsername(1, "   " + CHOSEN_USERNAME + "   ");

        // 3. Assert
        Assertions.assertSame(updated, result);
        Assertions.assertEquals(CHOSEN_USERNAME, result.getUsername());
    }

    @Test
    public void testUpdateUsernameWhenUserDoesNotExistThrowsUserNotFoundException() {
        // 1. Arrange
        final long missingId = 999;
        Mockito.when(userDao.updateUsername(missingId, CHOSEN_USERNAME)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable update = () -> userService.updateUsername(missingId, CHOSEN_USERNAME);

        // 3. Assert
        Assertions.assertThrows(UserNotFoundException.class, update);
    }

    @Test
    public void testChangePasswordWhenCurrentPasswordMatchesReturnsUserWithNewHashAndNotifiesAfterCommit() {
        // 1. Arrange
        final User current = new User(1, CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE);
        final User updated = new User(1, CHOSEN_USERNAME, NEW_EMAIL, NEW_PASSWORD_HASH, UserRole.USER, true, LANGUAGE);
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(current));
        Mockito.when(passwordHasher.matches(RAW_PASSWORD, PASSWORD_HASH)).thenReturn(true);
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, PASSWORD_HASH)).thenReturn(false);
        Mockito.when(passwordHasher.hash(NEW_RAW_PASSWORD)).thenReturn(NEW_PASSWORD_HASH);
        Mockito.when(userDao.updatePasswordIfMatches(1, PASSWORD_HASH, NEW_PASSWORD_HASH)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final User result = userService.changePassword(1, RAW_PASSWORD, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertSame(updated, result);
        Assertions.assertEquals(NEW_PASSWORD_HASH, result.getPasswordHash());
        Assertions.assertNull(emailService.passwordChangedUser);
        commitTransaction();
        Assertions.assertSame(updated, emailService.passwordChangedUser);
        Assertions.assertEquals(LOCALE, emailService.passwordChangedLocale);
    }

    @Test
    public void testChangePasswordWhenCurrentPasswordDoesNotMatchThrowsInvalidCurrentPasswordException() {
        // 1. Arrange
        final User current = enabledUser();
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(current));
        Mockito.when(passwordHasher.matches("wrong-password", current.getPasswordHash())).thenReturn(false);

        // 2. Exercise
        final Executable change = () -> userService.changePassword(1, "wrong-password", NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(InvalidCurrentPasswordException.class, change);
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testChangePasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException() {
        // 1. Arrange
        final User current = enabledUser();
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(current));
        Mockito.when(passwordHasher.matches(RAW_PASSWORD, current.getPasswordHash())).thenReturn(true);

        // 2. Exercise
        final Executable change = () -> userService.changePassword(1, RAW_PASSWORD, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(UnchangedPasswordException.class, change);
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testChangePasswordWhenUserDoesNotExistThrowsUserNotFoundException() {
        // 1. Arrange
        final long missingId = 999;
        Mockito.when(userDao.findById(missingId)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable change = () -> userService.changePassword(missingId, RAW_PASSWORD, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(UserNotFoundException.class, change);
    }

    @Test
    public void testChangePasswordWhenHashWasReplacedConcurrentlyThrowsInvalidCurrentPasswordException() {
        // 1. Arrange
        final User current = enabledUser();
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(current));
        Mockito.when(passwordHasher.matches(RAW_PASSWORD, current.getPasswordHash())).thenReturn(true);
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, current.getPasswordHash())).thenReturn(false);
        Mockito.when(passwordHasher.hash(NEW_RAW_PASSWORD)).thenReturn(NEW_PASSWORD_HASH);
        Mockito.when(userDao.updatePasswordIfMatches(1, current.getPasswordHash(), NEW_PASSWORD_HASH)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable change = () -> userService.changePassword(1, RAW_PASSWORD, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(InvalidCurrentPasswordException.class, change);
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testRequestPasswordResetWhenAccountIsEnabledReturnsNormallyAfterStoringTokenAndSchedulingLink() {
        // 1. Arrange
        final User user = enabledUser();
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(user));

        // 2. Exercise
        userService.requestPasswordReset("  Publisher@Example.COM  ", LOCALE);

        // 3. Assert
        Assertions.assertNull(emailService.passwordResetUser);
        commitTransaction();
        Assertions.assertSame(user, emailService.passwordResetUser);
        Assertions.assertEquals(LOCALE, emailService.passwordResetLocale);
        Assertions.assertNotNull(emailService.passwordResetToken);
    }

    @Test
    public void testRequestPasswordResetWhenEmailIsUnknownReturnsNormallyWithoutSendingLink() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.empty());

        // 2. Exercise
        userService.requestPasswordReset(NEW_EMAIL, LOCALE);

        // 3. Assert
        commitTransaction();
        Assertions.assertNull(emailService.passwordResetUser);
    }

    /*
     * Una cuenta pendiente todavia no tiene clave que recuperar: su camino sigue siendo el
     * correo de verificacion, asi que el pedido termina sin enviar nada.
     */
    @Test
    public void testRequestPasswordResetWhenAccountIsPendingReturnsNormallyWithoutSendingLink() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(PENDING_EMAIL))
                .thenReturn(Optional.of(pendingUser(PENDING_USER_ID, PENDING_EMAIL, PENDING_EMAIL, LANGUAGE)));

        // 2. Exercise
        userService.requestPasswordReset(PENDING_EMAIL, LOCALE);

        // 3. Assert
        commitTransaction();
        Assertions.assertNull(emailService.passwordResetUser);
    }

    /*
     * Dos pedidos simultaneos para el mismo correo borran cero filas cada uno y los dos
     * llegan al insert: el segundo choca con la unicidad de user_id y termina sin enviar
     * nada, porque el enlace que quedo vivo es el del primero.
     */
    @Test
    public void testRequestPasswordResetWhenAnotherRequestStoredItsLinkFirstReturnsNormallyWithoutSendingLink() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(enabledUser()));
        Mockito.when(resetTokenDao.create(Mockito.anyLong(), Mockito.anyString(), Mockito.any()))
                .thenThrow(new DuplicateKeyException("password_reset_tokens_user_id_key"));

        // 2. Exercise
        userService.requestPasswordReset(NEW_EMAIL, LOCALE);

        // 3. Assert
        commitTransaction();
        Assertions.assertNull(emailService.passwordResetUser);
    }

    @Test
    public void testResetPasswordWhenTokenIsValidReturnsUserWithNewHashAndNotifiesAfterCommit() {
        // 1. Arrange
        final User updated = new User(1, CHOSEN_USERNAME, NEW_EMAIL, NEW_PASSWORD_HASH,
                UserRole.USER, true, LANGUAGE);
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.of(liveToken()));
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(currentUser()));
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, PASSWORD_HASH)).thenReturn(false);
        Mockito.when(resetTokenDao.deleteByToken(TOKEN)).thenReturn(1);
        Mockito.when(passwordHasher.hash(NEW_RAW_PASSWORD)).thenReturn(NEW_PASSWORD_HASH);
        Mockito.when(userDao.updatePassword(1, NEW_PASSWORD_HASH)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(NEW_PASSWORD_HASH, result.get().getPasswordHash());
        commitTransaction();
        Assertions.assertSame(updated, emailService.passwordChangedUser);
        Assertions.assertEquals(LOCALE, emailService.passwordChangedLocale);
    }

    @Test
    public void testResetPasswordWhenTokenIsExpiredReturnsEmptyAndLeavesPasswordUntouched() {
        // 1. Arrange
        final PasswordResetToken expired = new PasswordResetToken(1, 1, TOKEN,
                LocalDateTime.now().minusMinutes(1));
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.of(expired));

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testResetPasswordWhenTokenWasAlreadyConsumedReturnsEmpty() {
        // 1. Arrange
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.of(liveToken()));
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(currentUser()));
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, PASSWORD_HASH)).thenReturn(false);
        Mockito.when(resetTokenDao.deleteByToken(TOKEN)).thenReturn(0);

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testResetPasswordWhenTokenDoesNotExistReturnsEmpty() {
        // 1. Arrange
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.empty());

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    /*
     * Mismo criterio que changePassword. El rechazo llega antes de reclamar el enlace, asi
     * que el correo sigue sirviendo para elegir otra clave.
     */
    @Test
    public void testResetPasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException() {
        // 1. Arrange
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.of(liveToken()));
        Mockito.when(userDao.findById(1)).thenReturn(Optional.of(currentUser()));
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, PASSWORD_HASH)).thenReturn(true);

        // 2. Exercise
        final Executable reset = () -> userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(UnchangedPasswordException.class, reset);
        commitTransaction();
        Assertions.assertNull(emailService.passwordChangedUser);
    }

    @Test
    public void testResetPasswordWhenTokenIsMissingReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(null, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    private static User currentUser() {
        return new User(1, CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE);
    }

    private static PasswordResetToken liveToken() {
        return new PasswordResetToken(1, 1, TOKEN, LocalDateTime.now().plusMinutes(30));
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

    private static void commitTransaction() {
        for (final TransactionSynchronization synchronization : TransactionSynchronizationManager.getSynchronizations()) {
            synchronization.afterCommit();
        }
    }

    private static final class CapturingEmailService implements EmailService {
        private User verificationUser;
        private String verificationToken;
        private Locale verificationLocale;
        private User welcomeUser;
        private Locale welcomeLocale;
        private User passwordChangedUser;
        private Locale passwordChangedLocale;
        private User passwordResetUser;
        private String passwordResetToken;
        private Locale passwordResetLocale;

        @Override
        public void sendWelcomeEmail(final User user, final Locale locale) {
            welcomeUser = user;
            welcomeLocale = locale;
        }

        @Override
        public void sendVerificationEmail(final User user, final String token, final Locale locale) {
            verificationUser = user;
            verificationToken = token;
            verificationLocale = locale;
        }

        @Override
        public void sendPostInterestEmail(final PostInterestNotification notification, final Locale locale) { }

        @Override
        public void sendInquiryAcceptedEmail(final InquiryAcceptedNotification notification,
                                             final Locale locale) { }

        @Override
        public void sendPasswordChangedEmail(final User user, final Locale locale) {
            passwordChangedUser = user;
            passwordChangedLocale = locale;
        }

        @Override
        public void sendPasswordResetEmail(final User user, final String token, final Locale locale) {
            passwordResetUser = user;
            passwordResetToken = token;
            passwordResetLocale = locale;
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
