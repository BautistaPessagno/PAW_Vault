---
title: "PasswordHasher"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java"]
---

# PasswordHasher

Single-method service contract for password hashing. [[SecurityConfig]] supplies PasswordEncoder::encode, keeping Spring Security types out of services.

## Connections

Project types referenced: none.

Referenced by: [[SecurityConfig]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java>)

```java
package ar.edu.itba.paw.services;

public interface PasswordHasher {
    String hash(String rawPassword);

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
