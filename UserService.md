---
title: "UserService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java"]
---

# UserService

Publisher lookup and findOrCreate contract. The public create method was removed with the inherited UI. [[UserServiceImpl]] creates a user privately when a normalized email is new. User rows remain part of publishing; there is still no authentication.

## Connections

Project types referenced: [[User]].

Referenced by: [[PostServiceImpl]], [[PostServiceImplTest]], [[UserServiceImpl]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;
import java.util.Optional;

public interface UserService {
    Optional<User> findById(long id);

    User findOrCreate(String username, String email, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
