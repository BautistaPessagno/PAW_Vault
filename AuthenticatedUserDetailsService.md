---
title: "AuthenticatedUserDetailsService"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java"]
---

# AuthenticatedUserDetailsService

Carga la Cuenta por correo para el login. Si no existe o no tiene contraseña, responde con el mismo error genérico.

## Guía de lectura

Datos y dependencias declaradas: `userService`.

Operaciones para localizar en la fuente: `loadUserByUsername`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[User]], [[UserService]].

Referenciado por: [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java>), líneas 1–26.

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
