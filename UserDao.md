---
title: "UserDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java"]
---

# UserDao

The users persistence contract. `findById` and `findByEmail` return Optional; `create` always inserts; `findOrCreate` reuses an email without updating the username. [[UserJdbcDao]] implements all four. [[UserServiceImpl]] implements its own find-or-create orchestration with `findByEmail` and `create` so only new users receive welcome mail.

## Connections

Project types referenced: [[User]].

Referenced by: [[UserJdbcDao]], [[UserServiceImpl]].

Tests: [[UserJdbcDaoTest]], [[UserServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java, lines 1–15](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.User;

import java.util.Optional;

public interface UserDao {
    Optional<User> findById(long id);

    Optional<User> findByEmail(String email);

    User findOrCreate(String username, String email);

    User create(String username, String email);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
