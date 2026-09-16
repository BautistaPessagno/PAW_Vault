---
title: "UserService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java"]
---

# UserService

Account lookup, email-only registration and token-based activation with chosen username/password. Locale is supplied explicitly for outgoing mail; no findOrCreate publisher API remains.

## Connections

Project types referenced: [[User]].

Referenced by: [[AuthenticatedUserDetailsService]], [[AuthenticationController]], [[PostServiceImpl]], [[PostServiceImplTest]], [[SecurityConfig]], [[UserServiceImpl]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>)

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
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
