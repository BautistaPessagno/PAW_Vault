---
title: "UserServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java"]
---

# UserServiceImpl

findById is read-only transactional. findOrCreate normalizes email and reuses an existing User without changing its username. If missing, a private create helper inserts the user and requests welcome mail with the caller Locale. The helper runs inside findOrCreate’s transaction; there is no longer a public create API or standalone create transaction. Welcome mail is not tied to database commit.

## Connections

Project types referenced: [[EmailService]], [[User]], [[UserDao]], [[UserService]].

Referenced by: [[UserServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java, lines 1–48](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>)

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

    private User create(final String username, final String email, final Locale locale) {
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

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
