---
title: "UserService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java"]
---

# UserService

Exposes lookup by ID, explicit user creation, and publisher reuse-or-creation. Creation methods take a Locale because a new user triggers [[EmailService]] welcome mail. [[HelloWorldController]] uses create and findById; [[PostServiceImpl]] uses findOrCreate. No authentication is part of this contract.

## Connections

Project types referenced: [[User]].

Referenced by: [[HelloWorldController]], [[PostServiceImpl]], [[UserServiceImpl]].

Tests: [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;
import java.util.Optional;

public interface UserService {
    Optional<User> findById(long id);

    User create(String username, String email, Locale locale);

    User findOrCreate(String username, String email, Locale locale);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
