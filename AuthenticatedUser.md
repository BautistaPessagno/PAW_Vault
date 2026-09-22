---
title: "AuthenticatedUser"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java"]
---

# AuthenticatedUser

Immutable UserDetails adapter. getUsername returns the login email, getDisplayName returns the chosen name, and getId/getEmail supply trusted publication/contact identity. ADMIN receives both authorities; enabled mirrors the account. Expiry and account-lock flags otherwise return true. [[ProfileController]] builds a fresh instance after a username change to refresh the session principal.

## Connections

Project types referenced: [[User]], [[UserRole]].

Referenced by: [[AuthenticatedUserDetailsService]], [[InquiryController]], [[PostContactController]], [[ProfileController]], [[PublishController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java, lines 1–87](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>)

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

public final class AuthenticatedUser implements UserDetails {

    private static final GrantedAuthority ROLE_USER = new SimpleGrantedAuthority("ROLE_USER");
    private static final GrantedAuthority ROLE_ADMIN = new SimpleGrantedAuthority("ROLE_ADMIN");

    private final long id;
    private final String username;
    private final String email;
    private final String passwordHash;
    private final List<GrantedAuthority> authorities;
    private final boolean enabled;

    public AuthenticatedUser(final User user) {
        this.id = user.getId();
        this.username = user.getUsername();
        this.email = user.getEmail();
        this.passwordHash = user.getPasswordHash();
        this.authorities = authoritiesFor(user.getRole());
        this.enabled = user.isEnabled();
    }

    // El administrador conserva lo que puede hacer una cuenta comun y le suma administracion.
    private static List<GrantedAuthority> authoritiesFor(final UserRole role) {
        return role == UserRole.ADMIN ? List.of(ROLE_ADMIN, ROLE_USER) : List.of(ROLE_USER);
    }

    public long getId() {
        return id;
    }

    // El nombre que la persona eligio al verificar la cuenta, para mostrar en la cabecera.
    public String getDisplayName() {
        return username;
    }

    // El correo con el que responder la consulta, para no volver a buscar al comprador en la base.
    public String getEmail() {
        return email;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities;
    }

    @Override
    public String getPassword() {
        return passwordHash;
    }

    // Spring Security identifica la cuenta por el valor con el que se inicia sesion.
    @Override
    public String getUsername() {
        return email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return enabled;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
