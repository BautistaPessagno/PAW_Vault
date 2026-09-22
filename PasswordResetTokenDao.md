---
title: "PasswordResetTokenDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java"]
---

# PasswordResetTokenDao

Create, find, delete by token, delete by user and purge expired password-recovery tokens. Expiry instants and the current time come from the service; the DAO does not judge whether a token is still valid.

## Connections

Project types referenced: [[PasswordResetToken]].

Referenced by: [[PasswordResetTokenJdbcDao]], [[PasswordResetTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java, lines 1–20](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PasswordResetToken;

import java.time.LocalDateTime;
import java.util.Optional;

public interface PasswordResetTokenDao {

    PasswordResetToken create(long userId, String token, LocalDateTime expiresAt);

    Optional<PasswordResetToken> findByToken(String token);

    int deleteByToken(String token);

    int deleteByUserId(long userId);

    int deleteExpired(LocalDateTime now);

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
