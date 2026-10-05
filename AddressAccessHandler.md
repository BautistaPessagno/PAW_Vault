---
title: "AddressAccessHandler"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java"]
---

# AddressAccessHandler

Bean `addressAccess` de `@PreAuthorize`: solo el dueño edita o elimina una dirección. Una dirección inexistente pasa, para que el service responda 404.

## Guía de lectura

Datos y dependencias declaradas: `addressService`.

Operaciones para localizar en la fuente: `isOwner`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressService]], [[AuthenticatedUser]].

Referenciado por: [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java>), líneas 1–23.

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.services.AddressService;
import org.springframework.security.core.Authentication;

// Regla de @PreAuthorize para las direcciones: solo su duenia las edita o elimina. Una
// direccion inexistente pasa: el service responde 404 en vez de un 403 enganioso.
public final class AddressAccessHandler {

    private final AddressService addressService;

    public AddressAccessHandler(final AddressService addressService) {
        this.addressService = addressService;
    }

    public boolean isOwner(final Authentication authentication, final long addressId) {
        return AuthenticatedUser.idOf(authentication)
                .map(userId -> addressService.findById(addressId)
                        .map(address -> address.getUserId() == userId)
                        .orElse(true))
                .orElse(false);
    }
}
```
