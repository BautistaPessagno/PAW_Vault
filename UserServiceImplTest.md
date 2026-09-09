---
title: "UserServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# UserServiceImplTest

Two Mockito tests cover retaining an existing user unchanged and returning a new normalized user. The old public-create tests were removed. These tests do not assert welcome delivery or activate transactional/async proxies.

## Test methods

- `testFindOrCreateWhenUserExistsReturnsExistingUserUnchanged`
- `testFindOrCreateWhenUserIsNewReturnsCreatedNormalizedUser`

These are source assertions, not a fresh passing test run.

## Connections

Project types referenced: [[EmailService]], [[User]], [[UserDao]], [[UserServiceImpl]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java, lines 1–64](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.UserDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Locale;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class UserServiceImplTest {

    @Mock
    private UserDao userDao;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private UserServiceImpl userService;

    @Test
    public void testFindOrCreateWhenUserExistsReturnsExistingUserUnchanged() {
        // 1. Arrange
        final String username = "newUsername";
        final String email = "  Publisher@Example.COM  ";
        final String normalizedEmail = "publisher@example.com";
        final User expected = new User(1, "firstUsername", normalizedEmail);
        Mockito.when(userDao.findByEmail(normalizedEmail)).thenReturn(Optional.of(expected));

        // 2. Exercise
        final User result = userService.findOrCreate(username, email, Locale.ENGLISH);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(expected.getUsername(), result.getUsername());
        Assertions.assertEquals(normalizedEmail, result.getEmail());
    }

    @Test
    public void testFindOrCreateWhenUserIsNewReturnsCreatedNormalizedUser() {
        // 1. Arrange
        final String username = "publisher";
        final String email = "  Publisher@Example.COM  ";
        final String normalizedEmail = "publisher@example.com";
        final User expected = new User(1, username, normalizedEmail);
        Mockito.when(userDao.findByEmail(normalizedEmail)).thenReturn(Optional.empty());
        Mockito.when(userDao.create(username, normalizedEmail)).thenReturn(expected);

        // 2. Exercise
        final User result = userService.findOrCreate(username, email, Locale.ENGLISH);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(username, result.getUsername());
        Assertions.assertEquals(normalizedEmail, result.getEmail());
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
