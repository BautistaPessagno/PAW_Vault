---
title: "UserDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java"]
---

# UserDao

Account lookup by ID/email, creation with role and preferred locale, and conditional activation. activateIfPending changes credentials only while enabled is false.

## Connections

Project types referenced: [[User]], [[UserRole]].

Referenced by: [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;

import java.util.Optional;

public interface UserDao {
    Optional<User> findById(long id);

    Optional<User> findByEmail(String email);

    User create(String username, String email, String passwordHash, UserRole role, String preferredLocale);

    boolean activateIfPending(long id, String username, String passwordHash);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
