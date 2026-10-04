---
title: "PostAccessHandler"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java"]
---

# PostAccessHandler

Bean `postAccess` de `@PreAuthorize`: quien edita o elimina es el publicante. El administrador entra por rol en la misma expresión.

## Guía de lectura

Datos y dependencias declaradas: `postService`.

Operaciones para localizar en la fuente: `isPublisher`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[PostService]].

Referenciado por: [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java>), líneas 1–23.

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.services.PostService;
import org.springframework.security.core.Authentication;

// Regla de @PreAuthorize para editar y eliminar una publicacion; el administrador entra por su rol
// en la misma expresion. Un post inexistente pasa: el service responde 404 en vez de un 403 enganioso.
public final class PostAccessHandler {

    private final PostService postService;

    public PostAccessHandler(final PostService postService) {
        this.postService = postService;
    }

    public boolean isPublisher(final Authentication authentication, final long postId) {
        return AuthenticatedUser.idOf(authentication)
                .map(userId -> postService.findPublisherId(postId)
                        .map(userId::equals)
                        .orElse(true))
                .orElse(false);
    }
}
```
