---
title: "EmailVerificationToken"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java"]
---

# EmailVerificationToken

Persisted token ID, user ID and random URL-safe token string. No expiry timestamp is present. Successful activation deletes every token for that user through [[EmailVerificationTokenDao]].

## Connections

Project types referenced: none.

Referenced by: [[EmailVerificationTokenDao]], [[EmailVerificationTokenJdbcDao]], [[EmailVerificationTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java, lines 1–27](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java>)

```java
package ar.edu.itba.paw.models;

public final class EmailVerificationToken {

    private final long id;
    private final long userId;
    private final String token;

    public EmailVerificationToken(final long id, final long userId, final String token) {
        this.id = id;
        this.userId = userId;
        this.token = token;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getToken() {
        return token;
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
