---
title: "UserServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# UserServiceImplTest

Tests de `UserServiceImpl` en `services`: 44 casos declarados. Cubre: registro (nuevo, duplicado, pendiente, carrera), verificación, reenvío con espera, cambio y recuperación de contraseña y datos de cobro, con DAOs simulados. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `LOCALE`, `LANGUAGE`, `PENDING_USER_ID`, `PENDING_EMAIL`, `UNVERIFIED_USER_ID`, `NEW_EMAIL`, `TOKEN`, `RECENTLY_SENT_USER_ID`, `RECENT_TOKEN`, `FIXTURE_TOKENS`, `CHOSEN_USERNAME`, `RAW_PASSWORD`, `PASSWORD_HASH`, `NEW_RAW_PASSWORD`, `NEW_PASSWORD_HASH`, `AVATAR_USER_ID`, `PREVIOUS_AVATAR_ID`, `NEW_AVATAR_ID`, `PNG_CONTENT_TYPE`, `PNG_DATA`, `userDao`, `resetTokenDao`, `passwordHasher`, `inquiryDao`, `imageService`, `verificationTokenDao`, `emailService`, `userService`, `tokens`, `nextId`, `verificationUser`, `verificationToken`, `verificationLocale`, `welcomeUser`, `welcomeLocale`, `passwordChangedUser`, `passwordChangedLocale`, `passwordResetUser`, `passwordResetToken`, `passwordResetLocale`.

Operaciones para localizar en la fuente: `setUp`, `tearDown`, `currentUser`, `liveToken`, `pendingUser`, `verifiedPublisher`, `unverifiedUser`, `verifiedUser`, `commitTransaction`, `InMemoryVerificationTokenDao`, `create`, `findByToken`, `findLatestByUserId`, `deleteByUserId`, `countForUser`, `size`, `sendWelcomeEmail`, `sendVerificationEmail`, `sendPostInterestEmail`, `sendInquiryUpdateEmail`, `sendMessageEmail`, `sendPasswordChangedEmail`, `sendPasswordResetEmail`.

Casos declarados: 44.

- `testUpdateAvatarWhenUserHasPhotoReturnsNewPhotoAndDeletesPrevious`
- `testUpdateAvatarWhenAvatarIsNullReturnsEmptyAndDeletesPrevious`
- `testUpdateAvatarWhenImageIsInvalidReturnsInvalidImageExceptionAndKeepsPrevious`
- `testUpdateAvatarWhenUserDoesNotExistReturnsUserNotFoundException`
- `testRegisterWhenEmailIsNewReturnsUnverifiedUserWithNormalizedEmailAndChosenUsername`
- `testRegisterWhenAccountIsVerifiedThrowsDuplicateUserException`
- `testRegisterWhenAccountIsUnverifiedWithPasswordThrowsDuplicateUserException`
- `testRegisterWhenAccountIsPendingReturnsCompletedUnverifiedUser`
- `testRegisterWhenPendingAccountWasCompletedByAnotherRequestThrowsDuplicateUserException`
- `testRegisterWhenAnotherRequestInsertedTheSameEmailThrowsDuplicateUserException`
- `testVerifyEmailWhenTokenIsValidReturnsVerifiedUserAndConsumesTheLink`
- `testVerifyEmailWhenTokenIsUnknownReturnsEmpty`
- `testVerifyEmailWhenTokenIsMissingReturnsEmpty`
- `testVerifyEmailWhenAccountWasAlreadyVerifiedReturnsEmptyWithoutWelcomeEmail`
- `testResendVerificationWhenAccountIsVerifiedReturnsFalseWithoutIssuingLink`
- `testResendVerificationWhenLastLinkIsRecentReturnsFalseAndKeepsIt`
- `testResendVerificationWhenAccountIsUnverifiedReturnsTrueAfterReplacingThePreviousLink`
- `testUpdateUsernameWhenValueHasSurroundingSpacesReturnsTrimmedUpdatedUser`
- `testUpdateUsernameWhenUserDoesNotExistThrowsUserNotFoundException`
- `testUpdatePaymentInfoWhenCbuHasSpacesReturnsUserWithNormalizedCbu`
- `testUpdatePaymentInfoWhenCvuIsValidReturnsUpdatedUser`
- `testUpdatePaymentInfoWhenClearingWithOpenSaleReturnsPaymentInfoRequiredException`
- `testUpdatePaymentInfoWhenClearingWithoutOpenSalesReturnsUserWithoutPaymentInfo`
- `testUpdatePaymentInfoWhenCheckDigitIsWrongReturnsInvalidPaymentInfoException`
- `testUpdatePaymentInfoWhenCbuIsShortReturnsInvalidPaymentInfoException`
- `testUpdatePaymentInfoWhenCbuHasLettersReturnsInvalidPaymentInfoException`
- `testUpdatePaymentInfoWhenAliasHasSpacesInsideReturnsInvalidPaymentInfoException`
- `testChangePasswordWhenCurrentPasswordMatchesReturnsUserWithNewHashAndNotifiesAfterCommit`
- `testChangePasswordWhenCurrentPasswordDoesNotMatchThrowsInvalidCurrentPasswordException`
- `testChangePasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException`
- `testChangePasswordWhenUserDoesNotExistThrowsUserNotFoundException`
- `testChangePasswordWhenHashWasReplacedConcurrentlyThrowsInvalidCurrentPasswordException`
- `testRequestPasswordResetWhenAccountIsEnabledReturnsNormallyAfterStoringTokenAndSchedulingLink`
- `testRequestPasswordResetWhenAccountIsUnverifiedWithPasswordReturnsNormallyAfterSchedulingLink`
- `testRequestPasswordResetWhenEmailIsUnknownReturnsNormallyWithoutSendingLink`
- `testRequestPasswordResetWhenAccountIsPendingReturnsNormallyWithoutSendingLink`
- `testRequestPasswordResetWhenAnotherRequestStoredItsLinkFirstReturnsNormallyWithoutSendingLink`
- `testResetPasswordWhenTokenIsValidReturnsUserWithNewHashAndNotifiesAfterCommit`
- `testResetPasswordWhenAccountIsUnverifiedReturnsVerifiedUserAndConsumesVerificationLinks`
- `testResetPasswordWhenTokenIsExpiredReturnsEmptyAndLeavesPasswordUntouched`
- `testResetPasswordWhenTokenWasAlreadyConsumedReturnsEmpty`
- `testResetPasswordWhenTokenDoesNotExistReturnsEmpty`
- `testResetPasswordWhenNewPasswordEqualsCurrentThrowsUnchangedPasswordException`
- `testResetPasswordWhenTokenIsMissingReturnsEmpty`

## Conexiones

Referencias estáticas a tipos del proyecto: [[DuplicateUserException]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[ImageUpload]], [[InMemoryImageService]], [[InquiryDao]], [[InquiryUpdateNotification]], [[InvalidCurrentPasswordException]], [[InvalidImageException]], [[InvalidPaymentInfoException]], [[MessageNotification]], [[PasswordHasher]], [[PasswordResetToken]], [[PasswordResetTokenDao]], [[PaymentInfo]], [[PaymentInfoRequiredException]], [[PostInterestNotification]], [[PublicUserProfile]], [[UnchangedPasswordException]], [[User]], [[UserDao]], [[UserNotFoundException]], [[UserRole]], [[UserServiceImpl]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>), líneas 1–938.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.PasswordResetToken;
import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.InquiryDao;
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

import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class UserServiceImplTest {

    private static final Locale LOCALE = Locale.ENGLISH;
    private static final String LANGUAGE = "en";
    private static final long PENDING_USER_ID = 3;
    private static final String PENDING_EMAIL = "legacy@example.com";
    private static final long UNVERIFIED_USER_ID = 4;
    private static final String NEW_EMAIL = "publisher@example.com";
    private static final String TOKEN = "pending-user-verification-token";
    // Cuenta sin verificar que pidio su enlace recien, dentro del tiempo minimo entre reenvios.
    private static final long RECENTLY_SENT_USER_ID = 5;
    private static final String RECENT_TOKEN = "recently-sent-verification-token";
    // Enlaces con los que arranca cada test: el viejo de la Cuenta sin verificar y el reciente.
    private static final int FIXTURE_TOKENS = 2;
    private static final String CHOSEN_USERNAME = "mailbox-owner";
    private static final String RAW_PASSWORD = "ViniloDemo2026!";
    private static final String PASSWORD_HASH = "$2a$12$hash-of-the-chosen-password";
    private static final String NEW_RAW_PASSWORD = "OtroVinilo2026!";
    private static final String NEW_PASSWORD_HASH = "$2a$12$hash-of-the-new-password";
    // La foto con la que arranca la Cuenta de los tests de avatar y la que le asigna el servicio al reemplazarla.
    private static final long AVATAR_USER_ID = 1;
    private static final long PREVIOUS_AVATAR_ID = 3;
    private static final long NEW_AVATAR_ID = 4;
    private static final String PNG_CONTENT_TYPE = "image/png";
    private static final byte[] PNG_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};

    @Mock
    private UserDao userDao;

    @Mock
    private PasswordResetTokenDao resetTokenDao;

    @Mock
    private PasswordHasher passwordHasher;

    @Mock
    private InquiryDao inquiryDao;

    private InMemoryImageService imageService;

    private InMemoryVerificationTokenDao verificationTokenDao;

    private CapturingEmailService emailService;

    private UserServiceImpl userService;

    @BeforeEach
    public void setUp() {
        emailService = new CapturingEmailService();
        // Arranca con la foto anterior de la Cuenta de los tests de avatar: la proxima es NEW_AVATAR_ID.
        imageService = new InMemoryImageService(PREVIOUS_AVATAR_ID);
        imageService.create(PNG_CONTENT_TYPE, PNG_DATA);
        verificationTokenDao = new InMemoryVerificationTokenDao();
        userService = new UserServiceImpl(userDao, emailService, passwordHasher, verificationTokenDao,
                resetTokenDao, inquiryDao, imageService);
        TransactionSynchronizationManager.initSynchronization();
    }

    @AfterEach
    public void tearDown() {
        TransactionSynchronizationManager.clearSynchronization();
    }

    @Test
    public void testUpdateAvatarWhenUserHasPhotoReturnsNewPhotoAndDeletesPrevious() {
        // 1. Arrange
        final ImageUpload upload = new ImageUpload(PNG_CONTENT_TYPE, PNG_DATA);
        Mockito.when(userDao.findAccountAppearanceByIdForUpdate(AVATAR_USER_ID)).thenReturn(Optional.of(
                new PublicUserProfile(AVATAR_USER_ID, "buyer", PREVIOUS_AVATAR_ID)));
        Mockito.when(userDao.updateAvatarImageId(AVATAR_USER_ID, NEW_AVATAR_ID)).thenReturn(true);

        // 2. Exercise
        final Optional<Long> result = userService.updateAvatar(AVATAR_USER_ID, upload);

        // 3. Assert
        Assertions.assertEquals(Optional.of(NEW_AVATAR_ID), result);
        Assertions.assertFalse(imageService.contains(PREVIOUS_AVATAR_ID));
        Assertions.assertArrayEquals(PNG_DATA, imageService.dataOf(NEW_AVATAR_ID));
    }

    @Test
    public void testUpdateAvatarWhenAvatarIsNullReturnsEmptyAndDeletesPrevious() {
        // 1. Arrange
        Mockito.when(userDao.findAccountAppearanceByIdForUpdate(AVATAR_USER_ID)).thenReturn(Optional.of(
                new PublicUserProfile(AVATAR_USER_ID, "buyer", PREVIOUS_AVATAR_ID)));
        Mockito.when(userDao.updateAvatarImageId(AVATAR_USER_ID, null)).thenReturn(true);

        // 2. Exercise
        final Optional<Long> result = userService.updateAvatar(AVATAR_USER_ID, null);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
        Assertions.assertFalse(imageService.contains(PREVIOUS_AVATAR_ID));
    }

    @Test
    public void testUpdateAvatarWhenImageIsInvalidReturnsInvalidImageExceptionAndKeepsPrevious() {
        // 1. Arrange
        final ImageUpload fakePng = new ImageUpload(PNG_CONTENT_TYPE, "not a png".getBytes(StandardCharsets.US_ASCII));
        Mockito.when(userDao.findAccountAppearanceByIdForUpdate(AVATAR_USER_ID)).thenReturn(Optional.of(
                new PublicUserProfile(AVATAR_USER_ID, "buyer", PREVIOUS_AVATAR_ID)));

        // 2. Exercise
        final Executable update = () -> userService.updateAvatar(AVATAR_USER_ID, fakePng);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, update);
        Assertions.assertTrue(imageService.contains(PREVIOUS_AVATAR_ID));
    }

    @Test
    public void testUpdateAvatarWhenUserDoesNotExistReturnsUserNotFoundException() {
        // 1. Arrange
        Mockito.when(userDao.findAccountAppearanceByIdForUpdate(AVATAR_USER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable update = () -> userService.updateAvatar(AVATAR_USER_ID, null);

        // 3. Assert
        Assertions.assertThrows(UserNotFoundException.class, update);
    }

    @Test
    public void testRegisterWhenEmailIsNewReturnsUnverifiedUserWithNormalizedEmailAndChosenUsername() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.empty());
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        // El DAO devuelve lo que se le pidio guardar, asi que el usuario devuelto muestra
        // con que argumentos se creo la cuenta.
        Mockito.when(userDao.create(CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH, UserRole.USER, LANGUAGE))
                .thenReturn(new User(1, CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH, UserRole.USER, false, LANGUAGE));

        // 2. Exercise
        final User result = userService.register("  Publisher@Example.COM  ", "  " + CHOSEN_USERNAME + "  ",
                RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertEquals(NEW_EMAIL, result.getEmail());
        Assertions.assertEquals(CHOSEN_USERNAME, result.getUsername());
        Assertions.assertEquals(PASSWORD_HASH, result.getPasswordHash());
        Assertions.assertFalse(result.isVerified());
        Assertions.assertNull(emailService.verificationUser);
        commitTransaction();
        Assertions.assertSame(result, emailService.verificationUser);
        Assertions.assertEquals(LOCALE, emailService.verificationLocale);
        Assertions.assertEquals(result.getId(),
                verificationTokenDao.findByToken(emailService.verificationToken).orElseThrow().getUserId());
    }

    @Test
    public void testRegisterWhenAccountIsVerifiedThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(verifiedPublisher()));

        // 2. Exercise
        final Executable register = () -> userService.register(NEW_EMAIL, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
        Assertions.assertEquals(FIXTURE_TOKENS, verificationTokenDao.size());
    }

    /*
     * Una cuenta sin verificar ya tiene la clave que eligio quien se registro primero: si un
     * segundo registro pudiera pisarla, cualquiera se quedaria con la cuenta ajena.
     */
    @Test
    public void testRegisterWhenAccountIsUnverifiedWithPasswordThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(unverifiedUser()));

        // 2. Exercise
        final Executable register = () -> userService.register(NEW_EMAIL, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
        Assertions.assertEquals(FIXTURE_TOKENS, verificationTokenDao.size());
    }

    @Test
    public void testRegisterWhenAccountIsPendingReturnsCompletedUnverifiedUser() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(PENDING_EMAIL))
                .thenReturn(Optional.of(pendingUser(PENDING_USER_ID, "legacy", PENDING_EMAIL, LANGUAGE)));
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        Mockito.when(userDao.completePending(PENDING_USER_ID, CHOSEN_USERNAME, PASSWORD_HASH)).thenReturn(true);
        Mockito.when(userDao.findById(PENDING_USER_ID)).thenReturn(Optional.of(
                new User(PENDING_USER_ID, CHOSEN_USERNAME, PENDING_EMAIL, PASSWORD_HASH, UserRole.USER, false,
                        LANGUAGE)));

        // 2. Exercise
        final User result = userService.register(PENDING_EMAIL, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertEquals(PENDING_USER_ID, result.getId());
        Assertions.assertEquals(CHOSEN_USERNAME, result.getUsername());
        Assertions.assertEquals(PASSWORD_HASH, result.getPasswordHash());
        Assertions.assertFalse(result.isVerified());
        commitTransaction();
        Assertions.assertSame(result, emailService.verificationUser);
    }

    @Test
    public void testRegisterWhenPendingAccountWasCompletedByAnotherRequestThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(PENDING_EMAIL))
                .thenReturn(Optional.of(pendingUser(PENDING_USER_ID, "legacy", PENDING_EMAIL, LANGUAGE)));
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        Mockito.when(userDao.completePending(PENDING_USER_ID, CHOSEN_USERNAME, PASSWORD_HASH)).thenReturn(false);

        // 2. Exercise
        final Executable register = () -> userService.register(PENDING_EMAIL, CHOSEN_USERNAME, RAW_PASSWORD,
                LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
        Assertions.assertEquals(FIXTURE_TOKENS, verificationTokenDao.size());
    }

    @Test
    public void testRegisterWhenAnotherRequestInsertedTheSameEmailThrowsDuplicateUserException() {
        // 1. Arrange
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.empty());
        Mockito.when(passwordHasher.hash(RAW_PASSWORD)).thenReturn(PASSWORD_HASH);
        Mockito.when(userDao.create(CHOSEN_USERNAME, NEW_EMAIL, PASSWORD_HASH, UserRole.USER, LANGUAGE))
                .thenThrow(new DuplicateKeyException("users_email_key"));

        // 2. Exercise
        final Executable register = () -> userService.register(NEW_EMAIL, CHOSEN_USERNAME, RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicateUserException.class, register);
    }

    @Test
    public void testVerifyEmailWhenTokenIsValidReturnsVerifiedUserAndConsumesTheLink() {
        // 1. Arrange
        Mockito.when(userDao.markVerified(UNVERIFIED_USER_ID)).thenReturn(true);
        Mockito.when(userDao.findById(UNVERIFIED_USER_ID)).thenReturn(Optional.of(verifiedUser(UNVERIFIED_USER_ID)));

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(TOKEN, LOCALE);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertTrue(result.get().isVerified());
        Assertions.assertFalse(verificationTokenDao.findByToken(TOKEN).isPresent());
        Assertions.assertNull(emailService.welcomeUser);
        commitTransaction();
        Assertions.assertSame(result.get(), emailService.welcomeUser);
        Assertions.assertEquals(LOCALE, emailService.welcomeLocale);
    }

    @Test
    public void testVerifyEmailWhenTokenIsUnknownReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(TOKEN, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testVerifyEmailWhenTokenIsMissingReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(null, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testVerifyEmailWhenAccountWasAlreadyVerifiedReturnsEmptyWithoutWelcomeEmail() {
        // 1. Arrange
        Mockito.when(userDao.markVerified(UNVERIFIED_USER_ID)).thenReturn(false);

        // 2. Exercise
        final Optional<User> result = userService.verifyEmail(TOKEN, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
        commitTransaction();
        Assertions.assertNull(emailService.welcomeUser);
    }

    @Test
    public void testResendVerificationWhenAccountIsVerifiedReturnsFalseWithoutIssuingLink() {
        // 1. Arrange
        Mockito.when(userDao.findByIdForUpdate(1)).thenReturn(Optional.of(verifiedPublisher()));

        // 2. Exercise
        final boolean result = userService.resendVerification(1, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(FIXTURE_TOKENS, verificationTokenDao.size());
        commitTransaction();
        Assertions.assertNull(emailService.verificationUser);
    }

    @Test
    public void testResendVerificationWhenLastLinkIsRecentReturnsFalseAndKeepsIt() {
        // 1. Arrange
        Mockito.when(userDao.findByIdForUpdate(RECENTLY_SENT_USER_ID)).thenReturn(Optional.of(
                new User(RECENTLY_SENT_USER_ID, "recent", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, false, LANGUAGE)));

        // 2. Exercise
        final boolean result = userService.resendVerification(RECENTLY_SENT_USER_ID, LOCALE);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertTrue(verificationTokenDao.findByToken(RECENT_TOKEN).isPresent());
        Assertions.assertEquals(FIXTURE_TOKENS, verificationTokenDao.size());
        commitTransaction();
        Assertions.assertNull(emailService.verificationUser);
    }

    @Test
    public void testResendVerificationWhenAccountIsUnverifiedReturnsTrueAfterReplacingThePreviousLink() {
        // 1. Arrange
        final User user = unverifiedUser();
        Mockito.when(userDao.findByIdForUpdate(UNVERIFIED_USER_ID)).thenReturn(Optional.of(user));

        // 2. Exercise
        final boolean result = userService.resendVerification(UNVERIFIED_USER_ID, LOCALE);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertFalse(verificationTokenDao.findByToken(TOKEN).isPresent());
        Assertions.assertEquals(1, verificationTokenDao.countForUser(UNVERIFIED_USER_ID));
        commitTransaction();
        Assertions.assertSame(user, emailService.verificationUser);
        Assertions.assertEquals(LOCALE, emailService.verificationLocale);
        Assertions.assertTrue(verificationTokenDao.findByToken(emailService.verificationToken).isPresent());
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
    public void testUpdatePaymentInfoWhenCbuHasSpacesReturnsUserWithNormalizedCbu() {
        // 1. Arrange
        final User updated = new User(1, "user", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE,
                new PaymentInfo("2850590940090418135201", null));
        Mockito.when(userDao.updatePaymentInfo(1, new PaymentInfo("2850590940090418135201", null)))
                .thenReturn(Optional.of(updated));

        // 2. Exercise
        final User result = userService.updatePaymentInfo(1, " 2850 5909 4009 0418 1352 01 ", "   ");

        // 3. Assert
        Assertions.assertSame(updated, result);
    }

    @Test
    public void testUpdatePaymentInfoWhenCvuIsValidReturnsUpdatedUser() {
        // 1. Arrange
        final User updated = new User(1, "user", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE,
                new PaymentInfo("0000003110000000000014", "mi.alias"));
        Mockito.when(userDao.updatePaymentInfo(1, new PaymentInfo("0000003110000000000014", "mi.alias")))
                .thenReturn(Optional.of(updated));

        // 2. Exercise
        final User result = userService.updatePaymentInfo(1, "0000003110000000000014", "mi.alias");

        // 3. Assert
        Assertions.assertSame(updated, result);
    }

    @Test
    public void testUpdatePaymentInfoWhenClearingWithOpenSaleReturnsPaymentInfoRequiredException() {
        // 1. Arrange
        Mockito.when(userDao.findByIdForUpdate(1)).thenReturn(Optional.of(currentUser()));
        Mockito.when(inquiryDao.hasOpenSalesBySellerId(1)).thenReturn(true);

        // 2. Exercise
        final Executable update = () -> userService.updatePaymentInfo(1, "  ", null);

        // 3. Assert
        Assertions.assertThrows(PaymentInfoRequiredException.class, update);
    }

    @Test
    public void testUpdatePaymentInfoWhenClearingWithoutOpenSalesReturnsUserWithoutPaymentInfo() {
        // 1. Arrange
        final User updated = new User(1, "user", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE);
        Mockito.when(userDao.findByIdForUpdate(1)).thenReturn(Optional.of(currentUser()));
        Mockito.when(inquiryDao.hasOpenSalesBySellerId(1)).thenReturn(false);
        Mockito.when(userDao.updatePaymentInfo(1, PaymentInfo.NONE)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final User result = userService.updatePaymentInfo(1, "", " ");

        // 3. Assert
        Assertions.assertFalse(result.hasPaymentInfo());
    }

    @Test
    public void testUpdatePaymentInfoWhenCheckDigitIsWrongReturnsInvalidPaymentInfoException() {
        // 1. Arrange
        final String wrongCheckDigit = "2850590940090418135202";

        // 2. Exercise
        final Executable update = () -> userService.updatePaymentInfo(1, wrongCheckDigit, null);

        // 3. Assert
        Assertions.assertThrows(InvalidPaymentInfoException.class, update);
    }

    @Test
    public void testUpdatePaymentInfoWhenCbuIsShortReturnsInvalidPaymentInfoException() {
        // 1. Arrange
        final String shortCbu = "285059094009041813520";

        // 2. Exercise
        final Executable update = () -> userService.updatePaymentInfo(1, shortCbu, null);

        // 3. Assert
        Assertions.assertThrows(InvalidPaymentInfoException.class, update);
    }

    @Test
    public void testUpdatePaymentInfoWhenCbuHasLettersReturnsInvalidPaymentInfoException() {
        // 1. Arrange
        final String lettersCbu = "28505909400904181352AB";

        // 2. Exercise
        final Executable update = () -> userService.updatePaymentInfo(1, lettersCbu, null);

        // 3. Assert
        Assertions.assertThrows(InvalidPaymentInfoException.class, update);
    }

    @Test
    public void testUpdatePaymentInfoWhenAliasHasSpacesInsideReturnsInvalidPaymentInfoException() {
        // 1. Arrange
        final String invalidAlias = "mi alias";

        // 2. Exercise
        final Executable update = () -> userService.updatePaymentInfo(1, null, invalidAlias);

        // 3. Assert
        Assertions.assertThrows(InvalidPaymentInfoException.class, update);
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
        final User current = verifiedPublisher();
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
        final User current = verifiedPublisher();
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
        final User current = verifiedPublisher();
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
        final User user = verifiedPublisher();
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
    public void testRequestPasswordResetWhenAccountIsUnverifiedWithPasswordReturnsNormallyAfterSchedulingLink() {
        // 1. Arrange
        final User user = unverifiedUser();
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(user));

        // 2. Exercise
        userService.requestPasswordReset(NEW_EMAIL, LOCALE);

        // 3. Assert
        commitTransaction();
        Assertions.assertSame(user, emailService.passwordResetUser);
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
     * Una cuenta pendiente del flujo anterior no tiene clave que recuperar: su camino es
     * volver a registrarse, asi que el pedido termina sin enviar nada.
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
        Mockito.when(userDao.findByEmail(NEW_EMAIL)).thenReturn(Optional.of(verifiedPublisher()));
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

    /*
     * El enlace de recuperacion llego al correo, asi que demuestra lo mismo que el de
     * verificacion: la cuenta queda verificada y sus enlaces de verificacion dejan de servir.
     */
    @Test
    public void testResetPasswordWhenAccountIsUnverifiedReturnsVerifiedUserAndConsumesVerificationLinks() {
        // 1. Arrange
        final PasswordResetToken resetToken = new PasswordResetToken(1, UNVERIFIED_USER_ID, TOKEN,
                LocalDateTime.now().plusMinutes(30));
        final User updated = new User(UNVERIFIED_USER_ID, "unverified", NEW_EMAIL, NEW_PASSWORD_HASH, UserRole.USER,
                true, LANGUAGE);
        Mockito.when(resetTokenDao.findByToken(TOKEN)).thenReturn(Optional.of(resetToken));
        Mockito.when(userDao.findById(UNVERIFIED_USER_ID)).thenReturn(Optional.of(unverifiedUser()));
        Mockito.when(passwordHasher.matches(NEW_RAW_PASSWORD, PASSWORD_HASH)).thenReturn(false);
        Mockito.when(resetTokenDao.deleteByToken(TOKEN)).thenReturn(1);
        Mockito.when(passwordHasher.hash(NEW_RAW_PASSWORD)).thenReturn(NEW_PASSWORD_HASH);
        Mockito.when(userDao.updatePassword(UNVERIFIED_USER_ID, NEW_PASSWORD_HASH)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final Optional<User> result = userService.resetPassword(TOKEN, NEW_RAW_PASSWORD, LOCALE);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertTrue(result.get().isVerified());
        Assertions.assertEquals(NEW_PASSWORD_HASH, result.get().getPasswordHash());
        Assertions.assertEquals(0, verificationTokenDao.countForUser(UNVERIFIED_USER_ID));
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

    private static User verifiedPublisher() {
        return new User(1, "publisher", NEW_EMAIL, "$2a$12$another-hash", UserRole.USER, true, LANGUAGE);
    }

    private static User unverifiedUser() {
        return new User(UNVERIFIED_USER_ID, "unverified", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, false, LANGUAGE);
    }

    private static User verifiedUser(final long id) {
        return new User(id, "unverified", NEW_EMAIL, PASSWORD_HASH, UserRole.USER, true, LANGUAGE);
    }

    private static void commitTransaction() {
        for (final TransactionSynchronization synchronization : TransactionSynchronizationManager.getSynchronizations()) {
            synchronization.afterCommit();
        }
    }

    /*
     * Guarda los tokens en memoria para que los tests comprueben que enlaces quedan vivos
     * despues de la operacion, en lugar de verificar que se llamo al DAO. Arranca con el
     * enlace vivo de la Cuenta sin verificar, como populator.sql en persistence, mandado hace
     * rato, y con uno recien mandado a otra cuenta.
     */
    private static final class InMemoryVerificationTokenDao implements EmailVerificationTokenDao {
        private final Map<String, EmailVerificationToken> tokens = new HashMap<>();
        private long nextId = 1;

        private InMemoryVerificationTokenDao() {
            create(UNVERIFIED_USER_ID, TOKEN, LocalDateTime.of(2026, 1, 1, 10, 0));
            create(RECENTLY_SENT_USER_ID, RECENT_TOKEN, LocalDateTime.now());
        }

        @Override
        public EmailVerificationToken create(final long userId, final String token, final LocalDateTime createdAt) {
            final EmailVerificationToken created = new EmailVerificationToken(nextId++, userId, token, createdAt);
            tokens.put(token, created);
            return created;
        }

        @Override
        public Optional<EmailVerificationToken> findByToken(final String token) {
            return Optional.ofNullable(tokens.get(token));
        }

        @Override
        public Optional<EmailVerificationToken> findLatestByUserId(final long userId) {
            return tokens.values().stream()
                    .filter(stored -> stored.getUserId() == userId)
                    .max(Comparator.comparing(EmailVerificationToken::getCreatedAt));
        }

        @Override
        public int deleteByUserId(final long userId) {
            final int before = tokens.size();
            tokens.values().removeIf(stored -> stored.getUserId() == userId);
            return before - tokens.size();
        }

        private long countForUser(final long userId) {
            return tokens.values().stream().filter(stored -> stored.getUserId() == userId).count();
        }

        private int size() {
            return tokens.size();
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
        public void sendInquiryUpdateEmail(final InquiryUpdateNotification notification,
                                           final Locale locale) { }

        @Override
        public void sendMessageEmail(final MessageNotification notification, final Locale locale) { }

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
