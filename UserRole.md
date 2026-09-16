---
title: "UserRole"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/UserRole.java"]
---

# UserRole

Account roles USER and ADMIN. [[AuthenticatedUser]] gives an administrator both ROLE_ADMIN and ROLE_USER authorities.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticatedUser]], [[EmailServiceImplTest]], [[PostServiceImplTest]], [[User]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/UserRole.java, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/UserRole.java>)

```java
package ar.edu.itba.paw.models;

public enum UserRole {
    USER,
    ADMIN
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
