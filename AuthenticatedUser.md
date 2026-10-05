---
title: "AuthenticatedUser"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java"]
---

# AuthenticatedUser

El principal de la sesión: adapta la Cuenta a `UserDetails`. Authorities `ROLE_USER`, `ROLE_ADMIN` y `VERIFIED`; `isEnabled` siempre verdadero para que una Cuenta sin verificar pueda entrar; `equals` por id para que el registro de sesiones agrupe bien. Ver [[Authentication flow]].

## Guía de lectura

Datos y dependencias declaradas: `VERIFIED`, `ROLE_USER`, `ROLE_ADMIN`, `VERIFIED_AUTHORITY`, `id`, `username`, `email`, `passwordHash`, `authorities`.

Operaciones para localizar en la fuente: `authoritiesFor`, `idOf`, `getId`, `isAdmin`, `getDisplayName`, `getEmail`, `isVerified`, `getAuthorities`, `getPassword`, `getUsername`, `isAccountNonExpired`, `isAccountNonLocked`, `isCredentialsNonExpired`, `isEnabled`, `equals`, `hashCode`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[User]], [[UserRole]].

Referenciado por: [[AddressAccessHandler]], [[AuthenticatedUserDetailsService]], [[AuthenticationController]], [[AuthenticationSessions]], [[CartController]], [[CartCountAdvice]], [[InquiryAccessHandler]], [[InquiryController]], [[PostAccessHandler]], [[PostContactController]], [[PostController]], [[ProfileController]], [[PublishController]], [[SecurityConfig]], [[VerificationAccessDeniedHandler]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>), líneas 1–130.

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

public final class AuthenticatedUser implements UserDetails {

    // La authority que exigen las URLs de publicar, consultar y operar sobre una consulta.
    public static final String VERIFIED = "VERIFIED";

    private static final GrantedAuthority ROLE_USER = new SimpleGrantedAuthority("ROLE_USER");
    private static final GrantedAuthority ROLE_ADMIN = new SimpleGrantedAuthority("ROLE_ADMIN");
    private static final GrantedAuthority VERIFIED_AUTHORITY = new SimpleGrantedAuthority(VERIFIED);

    private final long id;
    private final String username;
    private final String email;
    private final String passwordHash;
    private final List<GrantedAuthority> authorities;

    public AuthenticatedUser(final User user) {
        this.id = user.getId();
        this.username = user.getUsername();
        this.email = user.getEmail();
        this.passwordHash = user.getPasswordHash();
        this.authorities = authoritiesFor(user);
    }

    // El administrador conserva lo que puede hacer una cuenta comun y le suma administracion.
    private static List<GrantedAuthority> authoritiesFor(final User user) {
        final List<GrantedAuthority> granted = new ArrayList<>();
        if (user.getRole() == UserRole.ADMIN) {
            granted.add(ROLE_ADMIN);
        }
        granted.add(ROLE_USER);
        if (user.isVerified()) {
            granted.add(VERIFIED_AUTHORITY);
        }
        return List.copyOf(granted);
    }

    // Para los access handlers de @PreAuthorize: el id de la Cuenta con sesion, si la hay.
    public static Optional<Long> idOf(final Authentication authentication) {
        if (authentication != null && authentication.getPrincipal() instanceof AuthenticatedUser user) {
            return Optional.of(user.getId());
        }
        return Optional.empty();
    }

    public long getId() {
        return id;
    }

    public boolean isAdmin() {
        return authorities.contains(ROLE_ADMIN);
    }

    // El nombre que la persona eligio al registrarse, para mostrar en la cabecera.
    public String getDisplayName() {
        return username;
    }

    // El correo con el que responder la consulta, para no volver a buscar al comprador en la base.
    public String getEmail() {
        return email;
    }

    public boolean isVerified() {
        return authorities.contains(VERIFIED_AUTHORITY);
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

    // Una cuenta sin verificar tambien inicia sesion: lo que no puede hacer lo decide la
    // authority VERIFIED en SecurityConfig, no el login.
    @Override
    public boolean isEnabled() {
        return true;
    }

    // El SessionRegistry agrupa las sesiones por principal: dos principals de la misma cuenta,
    // aunque uno se haya refrescado despues de verificar, tienen que ser el mismo.
    @Override
    public boolean equals(final Object other) {
        return this == other || (other instanceof AuthenticatedUser user && id == user.id);
    }

    @Override
    public int hashCode() {
        return Long.hashCode(id);
    }
}
```
