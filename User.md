---
title: "User"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/User.java"]
---

# User

Account row with display username, normalized email, nullable password hash, USER/ADMIN role, enabled flag and preferred locale. Registration creates a disabled account; email verification chooses credentials and enables it. The username can later be edited from the profile, and the hash replaced by a password change or recovery. [[AuthenticatedUser]] adapts this value for Spring Security.

## Connections

Project types referenced: [[UserRole]].

Referenced by: [[AuthenticatedUser]], [[AuthenticatedUserDetailsService]], [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[ProfileController]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserNotFoundException]], [[UserService]], [[UserServiceImpl]], [[UserServiceImplTest]].

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
