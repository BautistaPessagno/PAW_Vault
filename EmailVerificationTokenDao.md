---
title: "EmailVerificationTokenDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java"]
---

# EmailVerificationTokenDao

Create and find unique tokens, and delete all tokens for an activated user. Re-registering a pending account can create additional tokens; this contract has no expiry or replacement operation.

## Connections

Project types referenced: [[EmailVerificationToken]].

Referenced by: [[EmailVerificationTokenJdbcDao]], [[EmailVerificationTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java, lines 1–15](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailVerificationToken;

import java.util.Optional;

public interface EmailVerificationTokenDao {

    EmailVerificationToken create(long userId, String token);

    Optional<EmailVerificationToken> findByToken(String token);

    int deleteByUserId(long userId);

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
