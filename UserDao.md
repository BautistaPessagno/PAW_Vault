---
title: "UserDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java"]
---

# UserDao

Account lookup by ID or email, creation with role and preferred locale, conditional activation, username update, compare-and-set password change (updatePasswordIfMatches) and an unconditional password update for token-authorized recovery. Update methods return the reloaded User, or empty when no row matched.

## Connections

Project types referenced: [[User]], [[UserRole]].

Referenced by: [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java, lines 1–22](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>)

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

    Optional<User> updateUsername(long id, String username);

    Optional<User> updatePasswordIfMatches(long id, String expectedPasswordHash, String newPasswordHash);

    Optional<User> updatePassword(long id, String newPasswordHash);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
