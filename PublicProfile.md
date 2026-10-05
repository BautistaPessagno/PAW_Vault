---
title: "PublicProfile"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java"]
---

# PublicProfile

El perfil público de una Cuenta: identidad, publicaciones a la venta paginadas y una [[ReviewPage]] con las reseñas del rol elegido. Ver [[Public profile flow]].

## Guía de lectura

Datos y dependencias declaradas: `user`, `postPage`, `reviewPage`.

Operaciones para localizar en la fuente: `getUser`, `getPostPage`, `getReviewPage`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostPage]], [[PublicUserProfile]], [[ReviewPage]].

Referenciado por: [[PublicProfileService]], [[PublicProfileServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java>), líneas 1–21.

```java
package ar.edu.itba.paw.models;

// El perfil publico de una Cuenta: sus publicaciones a la venta y la reputacion que le dejaron.
public final class PublicProfile {

    private final PublicUserProfile user;
    private final PostPage postPage;
    private final ReviewPage reviewPage;

    public PublicProfile(final PublicUserProfile user, final PostPage postPage, final ReviewPage reviewPage) {
        this.user = user;
        this.postPage = postPage;
        this.reviewPage = reviewPage;
    }

    public PublicUserProfile getUser() { return user; }

    public PostPage getPostPage() { return postPage; }

    public ReviewPage getReviewPage() { return reviewPage; }
}
```
