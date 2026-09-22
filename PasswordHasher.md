---
title: "PasswordHasher"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java"]
---

# PasswordHasher

Service contract with hash and matches, so services can create and verify password hashes without Spring Security types. [[SecurityConfig]] supplies an anonymous adapter over the BCrypt PasswordEncoder bean.

## Connections

Project types referenced: none.

Referenced by: [[SecurityConfig]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java>)

```java
package ar.edu.itba.paw.services;

public interface PasswordHasher {
    String hash(String rawPassword);

    boolean matches(String rawPassword, String passwordHash);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
