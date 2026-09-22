---
title: "UserService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java"]
---

# UserService

Account lookup, email-only registration, token activation, username update, a password change that proves the current password, silent password-reset requests and token-based reset. Locale is passed explicitly for outgoing mail.

## Connections

Project types referenced: [[User]].

Referenced by: [[AuthenticatedUserDetailsService]], [[AuthenticationController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[ProfileController]], [[SecurityConfig]], [[UserServiceImpl]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;
import java.util.Optional;

public interface UserService {
    Optional<User> findById(long id);

    Optional<User> findByEmail(String email);

    User register(String email, Locale locale);

    Optional<User> verifyEmail(String token, String username, String rawPassword, Locale locale);

    User updateUsername(long id, String username);

    User changePassword(long id, String currentPassword, String newPassword, Locale locale);

    void requestPasswordReset(String email, Locale locale);

    Optional<User> resetPassword(String token, String newPassword, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
