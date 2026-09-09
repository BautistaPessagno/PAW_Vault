---
title: "UserServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java"]
---

# UserServiceImpl

`findById` is read-only transactional. `create` normalizes email, inserts through [[UserDao]], invokes asynchronous welcome mail, then returns the [[User]]. `findOrCreate` normalizes email and lazily calls create only when lookup is empty, preserving the existing username. Its internal `create` call is a self-call, so it uses the already active findOrCreate transaction rather than a second proxy interception. Welcome delivery is launched before database commit and is not rolled back with a failed publication. See [[Transactions and concurrency]].

## Connections

Project types referenced: [[EmailService]], [[User]], [[UserDao]], [[UserService]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: [[UserServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java, lines 1–50](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.UserDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {


    private final UserDao userDao;
    private final EmailService emailService;

    @Autowired
    public UserServiceImpl(final UserDao userDao, final EmailService emailService) {
        this.userDao = userDao;
        this.emailService = emailService;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findById(final long id) {
        return userDao.findById(id);
    }

    @Override
    @Transactional
    public User create(final String username, final String email, final Locale locale) {
        final User user = userDao.create(username, normalize(email));
        emailService.sendWelcomeEmail(user, locale);
        return user;
    }

    @Override
    @Transactional
    public User findOrCreate(final String username, final String email, final Locale locale) {
        final String normalizedEmail = normalize(email);
        return userDao.findByEmail(normalizedEmail)
                .orElseGet(() -> create(username, normalizedEmail, locale));
    }

    private static String normalize(final String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
