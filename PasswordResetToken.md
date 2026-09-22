---
title: "PasswordResetToken"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java"]
---

# PasswordResetToken

Immutable password-recovery token: ID, user ID, random URL-safe token and expiresAt. Unlike [[EmailVerificationToken]] it carries an expiry. [[UserServiceImpl]] sets a one-hour window and decides validity, because [[PasswordResetTokenJdbcDao]] also returns expired rows.

## Connections

Project types referenced: none.

Referenced by: [[PasswordResetTokenDao]], [[PasswordResetTokenJdbcDao]], [[PasswordResetTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java>)

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;

public final class PasswordResetToken {

    private final long id;
    private final long userId;
    private final String token;
    private final LocalDateTime expiresAt;

    public PasswordResetToken(final long id, final long userId, final String token,
                              final LocalDateTime expiresAt) {
        this.id = id;
        this.userId = userId;
        this.token = token;
        this.expiresAt = expiresAt;
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

    public LocalDateTime getExpiresAt() {
        return expiresAt;
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
