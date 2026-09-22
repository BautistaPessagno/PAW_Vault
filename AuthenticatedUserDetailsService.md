---
title: "AuthenticatedUserDetailsService"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java"]
---

# AuthenticatedUserDetailsService

Loads an account through UserService.findByEmail and returns AuthenticatedUser. Missing accounts and null password hashes produce the same Invalid credentials message; enabled is checked by Spring Security using the adapter.

## Connections

Project types referenced: [[AuthenticatedUser]], [[User]], [[UserService]].

Referenced by: [[SecurityConfig]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java>)

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.UserService;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

public final class AuthenticatedUserDetailsService implements UserDetailsService {

    private final UserService userService;

    public AuthenticatedUserDetailsService(final UserService userService) {
        this.userService = userService;
    }

    @Override
    public UserDetails loadUserByUsername(final String email) {
        final User user = userService.findByEmail(email).orElseThrow(
                () -> new UsernameNotFoundException("Invalid credentials"));
        if (user.getPasswordHash() == null) {
            throw new UsernameNotFoundException("Invalid credentials");
        }
        return new AuthenticatedUser(user);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
