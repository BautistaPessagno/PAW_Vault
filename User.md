---
title: "User"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/User.java"]
---

# User

Account row with display username, normalized email, nullable password hash, USER/ADMIN role, enabled flag and preferred locale. Registration creates a disabled account; email verification chooses credentials and enables it. [[AuthenticatedUser]] adapts this value for Spring Security.

## Connections

Project types referenced: [[UserRole]].

Referenced by: [[AuthenticatedUser]], [[AuthenticatedUserDetailsService]], [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserNotFoundException]], [[UserService]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/User.java, lines 1–51](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/User.java>)

```java
package ar.edu.itba.paw.models;

public class User {
    private final long id;
    private final String username;
    private final String email;
    private final String passwordHash;
    private final UserRole role;
    private final boolean enabled;
    private final String preferredLocale;

    public User(final long id, final String username, final String email,
                final String passwordHash, final UserRole role, final boolean enabled,
                final String preferredLocale) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
        this.role = role;
        this.enabled = enabled;
        this.preferredLocale = preferredLocale;
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

    public String getPasswordHash() {
        return passwordHash;
    }

    public UserRole getRole() {
        return role;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public String getPreferredLocale() {
        return preferredLocale;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
