---
title: "UserServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java"]
---

# UserServiceImpl

Registration creates or reuses a pending account and stores a 32-byte URL-safe token; verification activates it once. updateUsername trims and rewrites the name. changePassword checks the current password, rejects reuse and uses a compare-and-set update. requestPasswordReset ignores unknown or pending accounts, purges expired links and keeps one live one-hour link per account. resetPassword checks expiry, rejects reuse, claims the token and updates the hash. Mail and success logs run after commit.

## Connections

Project types referenced: [[DuplicateUserException]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[InvalidCurrentPasswordException]], [[PasswordHasher]], [[PasswordResetToken]], [[PasswordResetTokenDao]], [[SupportedLocales]], [[TransactionCallbacks]], [[UnchangedPasswordException]], [[User]], [[UserDao]], [[UserNotFoundException]], [[UserRole]], [[UserService]].

Referenced by: [[UserServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java, lines 1–242](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.PasswordResetToken;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.PasswordResetTokenDao;
import ar.edu.itba.paw.persistence.UserDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;
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

    private final UserDao userDao;
    private final EmailService emailService;
    private final PasswordHasher passwordHasher;
    private final EmailVerificationTokenDao verificationTokenDao;
    private final PasswordResetTokenDao resetTokenDao;

    @Autowired
    public UserServiceImpl(final UserDao userDao, final EmailService emailService,
                           final PasswordHasher passwordHasher,
                           final EmailVerificationTokenDao verificationTokenDao,
                           final PasswordResetTokenDao resetTokenDao) {
        this.userDao = userDao;
        this.emailService = emailService;
        this.passwordHasher = passwordHasher;
        this.verificationTokenDao = verificationTokenDao;
        this.resetTokenDao = resetTokenDao;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findById(final long id) {
        return userDao.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findByEmail(final String email) {
        return userDao.findByEmail(normalize(email));
    }

    /*
     * El registro no pide clave: crea la cuenta deshabilitada y manda un enlace con un token
     * aleatorio al correo. Recien quien lo reciba elige nombre de usuario y clave, asi que
     * nadie puede ocupar el correo de otra persona. Una cuenta pendiente puede volver a
     * registrarse para recibir un enlace nuevo.
     */
    @Override
    @Transactional
    public User register(final String email, final Locale locale) {
        final String normalizedEmail = normalize(email);
        final Optional<User> existing = userDao.findByEmail(normalizedEmail);
        final User user;
        if (existing.isPresent()) {
            if (existing.get().isEnabled()) {
                throw new DuplicateUserException();
            }
            user = existing.get();
        } else {
            try {
                user = userDao.create(normalizedEmail, normalizedEmail, null, UserRole.USER,
                        SupportedLocales.languageOf(locale));
            } catch (final DuplicateKeyException e) {
                // Otro registro simultaneo del mismo correo se adelanto.
                throw new DuplicateUserException();
            }
        }

        final String token = generateToken();
        verificationTokenDao.create(user.getId(), token);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Sent verification link userId={}", user.getId());
            emailService.sendVerificationEmail(user, token, locale);
        });
        return user;
    }

    @Override
    @Transactional
    public Optional<User> verifyEmail(final String token, final String username, final String rawPassword,
                                      final Locale locale) {
        if (token == null) {
            return Optional.empty();
        }
        final Optional<EmailVerificationToken> stored = verificationTokenDao.findByToken(token);
        if (stored.isEmpty()) {
            return Optional.empty();
        }
        final long userId = stored.get().getUserId();

        // activateIfPending solo actualiza si la cuenta sigue deshabilitada: si otro request
        // ya la activo devuelve false y este enlace no pisa las credenciales elegidas.
        if (!userDao.activateIfPending(userId, username.trim(), passwordHasher.hash(rawPassword))) {
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
     * cuentas existen. Una cuenta pendiente tampoco recibe enlace, porque todavia no tiene
     * clave que recuperar: su camino sigue siendo el correo de verificacion.
     */
    @Override
    @Transactional
    public void requestPasswordReset(final String email, final Locale locale) {
        final Optional<User> found = userDao.findByEmail(normalize(email));
        if (found.isEmpty() || !found.get().isEnabled()) {
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
        final User updated = userDao.updatePassword(userId, passwordHasher.hash(newPassword))
                .orElseThrow(UserNotFoundException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Reset password userId={}", userId);
            emailService.sendPasswordChangedEmail(updated, locale);
        });
        return Optional.of(updated);
    }

    private static String generateToken() {
        final byte[] bytes = new byte[TOKEN_BYTES];
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    private static String normalize(final String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
