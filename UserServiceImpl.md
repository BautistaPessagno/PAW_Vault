---
title: "UserServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java"]
---

# UserServiceImpl

Registers a normalized email as a disabled USER account without a password, or reuses an existing pending account. Generates 32 random bytes encoded as unpadded URL-safe Base64 and requests verification mail. Enabled duplicate accounts raise DuplicateUserException. Verification conditionally activates the account, hashes the chosen password, deletes its tokens and requests welcome mail in one transaction. Tokens do not expire in this implementation.

## Connections

Project types referenced: [[DuplicateUserException]], [[EmailService]], [[EmailVerificationToken]], [[EmailVerificationTokenDao]], [[PasswordHasher]], [[SupportedLocales]], [[User]], [[UserDao]], [[UserRole]], [[UserService]].

Referenced by: [[UserServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java, lines 1–125](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.EmailVerificationToken;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.EmailVerificationTokenDao;
import ar.edu.itba.paw.persistence.UserDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.util.Base64;
import java.util.Locale;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    private static final Logger LOGGER = LoggerFactory.getLogger(UserServiceImpl.class);

    // 32 bytes aleatorios: adivinar un enlace de verificacion no es viable por fuerza bruta.
    private static final int TOKEN_BYTES = 32;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private final UserDao userDao;
    private final EmailService emailService;
    private final PasswordHasher passwordHasher;
    private final EmailVerificationTokenDao verificationTokenDao;

    @Autowired
    public UserServiceImpl(final UserDao userDao, final EmailService emailService,
                           final PasswordHasher passwordHasher,
                           final EmailVerificationTokenDao verificationTokenDao) {
        this.userDao = userDao;
        this.emailService = emailService;
        this.passwordHasher = passwordHasher;
        this.verificationTokenDao = verificationTokenDao;
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
        LOGGER.info("Sent verification link userId={}", user.getId());
        emailService.sendVerificationEmail(user, token, locale);
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
        LOGGER.info("Verified user email userId={}", user.getId());
        emailService.sendWelcomeEmail(user, locale);
        return Optional.of(user);
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
