---
title: "User"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/User.java"]
---

# User

Stores an ID, username and email. Publishing reuses this row by normalized email through [[UserServiceImpl]]. There is no password, role or login state. The business publicante is represented by a User row in this implementation, even though the older glossary distinguishes a publisher from an account. Reusing an email keeps the original username.

## Connections

Project types referenced: none.

Referenced by: [[EmailService]], [[EmailServiceImpl]], [[HelloWorldController]], [[PostServiceImpl]], [[UserDao]], [[UserJdbcDao]], [[UserService]], [[UserServiceImpl]].

Tests: [[EmailServiceImplTest]], [[PostServiceImplTest]], [[UserJdbcDaoTest]], [[UserServiceImplTest]]. See [[Testing and evidence]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `username` | `String` |
| `email` | `String` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/User.java, lines 1–25](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/User.java>)

```java
package ar.edu.itba.paw.models;

public class User {
    private final long id;
    private final String username;
    private final String email;

    public User(final long id, final String username, final String email) {
        this.id = id;
        this.username = username;
        this.email = email;
    }

    public long getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
