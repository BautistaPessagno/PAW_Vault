---
title: "UserServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java"]
---

# UserServiceImpl

Cuentas: registro con Cuenta sin verificar, verificación, reenvío con espera de un minuto, cambio y recuperación de contraseña, nombre, avatar y datos de cobro. Genera los tokens, resuelve las carreras con actualizaciones condicionales y registra cada correo para después del commit. Ver [[Authentication flow]], [[Password recovery flow]] y [[Tokens and email links]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `TOKEN_BYTES`, `SECURE_RANDOM`, `RESET_TOKEN_TTL`, `RESEND_COOLDOWN`, `userDao`, `emailService`, `passwordHasher`, `verificationTokenDao`, `resetTokenDao`, `inquiryDao`, `imageService`.

Operaciones para localizar en la fuente: `findById`, `findPublicProfileById`, `findAccountAppearanceById`, `updateAvatar`, `lockById`, `findByEmail`, `register`, `verifyEmail`, `resendVerification`, `issueVerificationToken`, `updateUsername`, `changePassword`, `requestPasswordReset`, `resetPassword`, `updatePaymentInfo`, `generateToken`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[DuplicateUserException]], [[EmailRules]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[ImageService]], [[ImageUpload]], [[InquiryDao]], [[InvalidCurrentPasswordException]], [[InvalidPaymentInfoException]], [[PasswordHasher]], [[PasswordResetToken]], [[PasswordResetTokenDao]], [[PaymentInfo]], [[PaymentInfoRequiredException]], [[PaymentInfoRules]], [[PublicUserProfile]], [[SupportedLocales]], [[TransactionCallbacks]], [[UnchangedPasswordException]], [[User]], [[UserDao]], [[UserNotFoundException]], [[UserRole]], [[UserService]].

Referenciado por: [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 1–359.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailRules;
import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.PasswordResetToken;
import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.PaymentInfoRules;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PasswordResetTokenDao;
import ar.edu.itba.paw.persistence.UserDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Base64;
import java.util.Locale;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    private static final Logger LOGGER = LoggerFactory.getLogger(UserServiceImpl.class);

    // 32 bytes aleatorios: adivinar un enlace de verificacion no es viable por fuerza bruta.
    private static final int TOKEN_BYTES = 32;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    // A diferencia del de verificacion, el enlace de recuperacion abre una cuenta que ya
    // esta en uso: se limita la ventana en la que sirve si el correo queda expuesto.
    private static final Duration RESET_TOKEN_TTL = Duration.ofHours(1);

    // Tiempo minimo entre dos enlaces de verificacion pedidos con el boton de reenviar.
    private static final Duration RESEND_COOLDOWN = Duration.ofMinutes(1);

    private final UserDao userDao;
    private final EmailService emailService;
    private final PasswordHasher passwordHasher;
    private final EmailVerificationTokenDao verificationTokenDao;
    private final PasswordResetTokenDao resetTokenDao;
    private final InquiryDao inquiryDao;
    private final ImageService imageService;

    // InquiryDao y no InquiryService: InquiryService ya depende de UserService.
    @Autowired
    public UserServiceImpl(final UserDao userDao, final EmailService emailService,
                           final PasswordHasher passwordHasher,
                           final EmailVerificationTokenDao verificationTokenDao,
                           final PasswordResetTokenDao resetTokenDao, final InquiryDao inquiryDao,
                           final ImageService imageService) {
        this.userDao = userDao;
        this.emailService = emailService;
        this.passwordHasher = passwordHasher;
        this.verificationTokenDao = verificationTokenDao;
        this.resetTokenDao = resetTokenDao;
        this.inquiryDao = inquiryDao;
        this.imageService = imageService;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findById(final long id) {
        return userDao.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<PublicUserProfile> findPublicProfileById(final long id) {
        return userDao.findPublicProfileById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<PublicUserProfile> findAccountAppearanceById(final long id) {
        return userDao.findAccountAppearanceById(id);
    }

    @Override
    @Transactional
    public Optional<Long> updateAvatar(final long userId, final ImageUpload avatar) {
        // El lock serializa dos cambios de foto de la misma Cuenta: cada uno borra la que leyo.
        final Long previousId = userDao.findAccountAppearanceByIdForUpdate(userId)
                .orElseThrow(UserNotFoundException::new).getAvatarImageId();
        final Long newId = avatar == null ? null
                : imageService.create(avatar.getContentType(), avatar.getData()).getId();
        if (!userDao.updateAvatarImageId(userId, newId)) {
            throw new UserNotFoundException();
        }
        if (previousId != null) {
            imageService.delete(previousId);
        }
        LOGGER.info("Updated avatar userId={} removed={}", userId, newId == null);
        return Optional.ofNullable(newId);
    }

    // MANDATORY: fuera de una transaccion el lock no protegeria nada.
    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public User lockById(final long id) {
        return userDao.findByIdForUpdate(id).orElseThrow(UserNotFoundException::new);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findByEmail(final String email) {
        return userDao.findByEmail(EmailRules.normalize(email));
    }

    /*
     * La cuenta existe desde el registro, sin verificar, y ya puede iniciar sesion. Un correo
     * que ya tiene clave, verificado o no, no se puede volver a registrar: si no, quien llegara
     * segundo pisaria la clave de la cuenta ajena. La unica excepcion es la cuenta pendiente
     * del flujo anterior, que no tiene clave y se completa con este registro.
     */
    @Override
    @Transactional
    public User register(final String email, final String username, final String rawPassword,
                         final Locale locale) {
        final String normalizedEmail = EmailRules.normalize(email);
        final String trimmedUsername = username.trim();
        final Optional<User> existing = userDao.findByEmail(normalizedEmail);
        if (existing.isPresent() && existing.get().getPasswordHash() != null) {
            throw new DuplicateUserException();
        }

        final String passwordHash = passwordHasher.hash(rawPassword);
        final User user;
        if (existing.isPresent()) {
            final long pendingId = existing.get().getId();
            // completePending solo actualiza una cuenta sin clave: si otro registro la completo
            // entre la lectura y este update, devuelve false y este no pisa la clave elegida.
            if (!userDao.completePending(pendingId, trimmedUsername, passwordHash)) {
                throw new DuplicateUserException();
            }
            user = userDao.findById(pendingId).orElseThrow(IllegalStateException::new);
        } else {
            try {
                user = userDao.create(trimmedUsername, normalizedEmail, passwordHash, UserRole.USER,
                        SupportedLocales.languageOf(locale));
            } catch (final DuplicateKeyException e) {
                // Otro registro simultaneo del mismo correo se adelanto.
                throw new DuplicateUserException();
            }
        }

        LOGGER.info("Registered user userId={}", user.getId());
        issueVerificationToken(user, locale);
        return user;
    }

    @Override
    @Transactional
    public Optional<User> verifyEmail(final String token, final Locale locale) {
        if (token == null) {
            return Optional.empty();
        }
        final Optional<EmailVerificationToken> stored = verificationTokenDao.findByToken(token);
        if (stored.isEmpty()) {
            return Optional.empty();
        }
        final long userId = stored.get().getUserId();

        // markVerified solo actualiza si la cuenta sigue sin verificar: si otro request ya la
        // verifico devuelve false y la bienvenida no se manda dos veces.
        if (!userDao.markVerified(userId)) {
            return Optional.empty();
        }
        verificationTokenDao.deleteByUserId(userId);

        final User user = userDao.findById(userId).orElseThrow(IllegalStateException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Verified user email userId={}", user.getId());
            emailService.sendWelcomeEmail(user, locale);
        });
        return Optional.of(user);
    }

    /*
     * Cualquiera puede registrar un correo ajeno y pedir reenvios en bucle: si el ultimo enlace
     * se mando hace menos de RESEND_COOLDOWN no se manda otro. El anterior sigue sirviendo.
     * El lock sobre la cuenta impide que dos pedidos en paralelo pasen juntos el chequeo.
     */
    @Override
    @Transactional
    public boolean resendVerification(final long userId, final Locale locale) {
        final User user = lockById(userId);
        if (user.isVerified()) {
            return false;
        }
        final LocalDateTime cooldownStart = LocalDateTime.now().minus(RESEND_COOLDOWN);
        final boolean recentlySent = verificationTokenDao.findLatestByUserId(userId)
                .filter(latest -> latest.getCreatedAt().isAfter(cooldownStart))
                .isPresent();
        if (recentlySent) {
            LOGGER.info("Skipped verification resend inside the cooldown userId={}", userId);
            return false;
        }
        issueVerificationToken(user, locale);
        return true;
    }

    // Borra los enlaces anteriores antes de crear el nuevo: solo vale el ultimo que se mando.
    private void issueVerificationToken(final User user, final Locale locale) {
        verificationTokenDao.deleteByUserId(user.getId());
        final String token = generateToken();
        verificationTokenDao.create(user.getId(), token, LocalDateTime.now());
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Sent verification link userId={}", user.getId());
            emailService.sendVerificationEmail(user, token, locale);
        });
    }

    @Override
    @Transactional
    public User updateUsername(final long id, final String username) {
        final User user = userDao.updateUsername(id, username.trim()).orElseThrow(UserNotFoundException::new);
        LOGGER.info("Updated username userId={}", id);
        return user;
    }

    @Override
    @Transactional
    public User changePassword(final long id, final String currentPassword, final String newPassword,
                               final Locale locale) {
        final User user = userDao.findById(id).orElseThrow(UserNotFoundException::new);
        if (!passwordHasher.matches(currentPassword, user.getPasswordHash())) {
            throw new InvalidCurrentPasswordException();
        }
        if (passwordHasher.matches(newPassword, user.getPasswordHash())) {
            throw new UnchangedPasswordException();
        }
        // Si otra request cambio la clave entre la lectura y el update, la actual ingresada ya no es la vigente.
        final User updated = userDao.updatePasswordIfMatches(id, user.getPasswordHash(),
                passwordHasher.hash(newPassword)).orElseThrow(InvalidCurrentPasswordException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Changed password userId={}", id);
            emailService.sendPasswordChangedEmail(updated, locale);
        });
        return updated;
    }

    /*
     * No distingue un correo desconocido de uno registrado: en los dos casos termina sin
     * avisar nada, asi la pantalla puede dar siempre la misma respuesta y no delatar que
     * cuentas existen. Una cuenta pendiente del flujo anterior tampoco recibe enlace, porque
     * no tiene clave que recuperar: su camino es volver a registrarse. Una cuenta sin
     * verificar que ya tiene clave si lo recibe.
     */
    @Override
    @Transactional
    public void requestPasswordReset(final String email, final Locale locale) {
        final Optional<User> found = userDao.findByEmail(EmailRules.normalize(email));
        if (found.isEmpty() || found.get().getPasswordHash() == null) {
            LOGGER.info("Ignored password reset request for an unknown or pending account");
            return;
        }
        final User user = found.get();
        final LocalDateTime now = LocalDateTime.now();

        // Un enlace vencido no vuelve a servir y nadie mas lo saca de la tabla: el pedido
        // aprovecha para limpiar los que quedaron atras, sean de quien sean.
        resetTokenDao.deleteExpired(now);

        // Un solo enlace vivo por cuenta: pedir otro deja sin efecto al anterior. La
        // invariante la sostiene la unicidad de user_id, porque dos pedidos simultaneos
        // borran cero filas cada uno y llegarian los dos al insert.
        resetTokenDao.deleteByUserId(user.getId());
        final String token = generateToken();
        try {
            resetTokenDao.create(user.getId(), token, now.plus(RESET_TOKEN_TTL));
        } catch (final DuplicateKeyException e) {
            // Otro pedido simultaneo para la misma cuenta ya dejo vivo su enlace: con ese
            // correo alcanza, asi que este termina sin enviar nada.
            LOGGER.info("Skipped a concurrent password reset request userId={}", user.getId());
            return;
        }
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Sent password reset link userId={}", user.getId());
            emailService.sendPasswordResetEmail(user, token, locale);
        });
    }

    @Override
    @Transactional
    public Optional<User> resetPassword(final String token, final String newPassword, final Locale locale) {
        if (token == null) {
            return Optional.empty();
        }
        final Optional<PasswordResetToken> stored = resetTokenDao.findByToken(token);
        if (stored.isEmpty() || stored.get().getExpiresAt().isBefore(LocalDateTime.now())) {
            return Optional.empty();
        }
        final long userId = stored.get().getUserId();

        // Mismo criterio que changePassword. Se rechaza antes de reclamar el enlace para que
        // quien elija la clave que ya tenia pueda reintentar con el mismo correo.
        final User current = userDao.findById(userId).orElseThrow(UserNotFoundException::new);
        if (passwordHasher.matches(newPassword, current.getPasswordHash())) {
            throw new UnchangedPasswordException();
        }

        // Reclamar el enlace dentro de la transaccion antes de tocar la clave impide que dos
        // requests concurrentes que leyeron el mismo token lo usen para pisarse entre si.
        if (resetTokenDao.deleteByToken(token) != 1) {
            return Optional.empty();
        }
        // El enlace llego al correo, asi que demuestra lo mismo que el de verificacion.
        userDao.markVerified(userId);
        verificationTokenDao.deleteByUserId(userId);
        final User updated = userDao.updatePassword(userId, passwordHasher.hash(newPassword))
                .orElseThrow(UserNotFoundException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Reset password userId={}", userId);
            emailService.sendPasswordChangedEmail(updated, locale);
        });
        return Optional.of(updated);
    }

    @Override
    @Transactional
    public User updatePaymentInfo(final long id, final String cbu, final String alias) {
        final PaymentInfo paymentInfo = new PaymentInfo(PaymentInfoRules.normalizeCbu(cbu),
                PaymentInfoRules.normalizeAlias(alias));
        if ((paymentInfo.getCbu() != null && !PaymentInfoRules.isValidCbu(paymentInfo.getCbu()))
                || (paymentInfo.getAlias() != null && !PaymentInfoRules.isValidAlias(paymentInfo.getAlias()))) {
            throw new InvalidPaymentInfoException();
        }
        // Vaciar los datos bloquea la cuenta antes de buscar ventas abiertas: accept() lee el
        // CBU de esa misma fila bloqueada, asi que un Aceptar en paralelo espera a que esto
        // termine (y ve los datos vacios) o termina antes (y aca se ve su venta abierta).
        if (!paymentInfo.isPresent()) {
            lockById(id);
            if (inquiryDao.hasOpenSalesBySellerId(id)) {
                throw new PaymentInfoRequiredException();
            }
        }
        final User user = userDao.updatePaymentInfo(id, paymentInfo)
                .orElseThrow(UserNotFoundException::new);
        LOGGER.info("Updated payment info userId={}", id);
        return user;
    }

    private static String generateToken() {
        final byte[] bytes = new byte[TOKEN_BYTES];
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}
```
