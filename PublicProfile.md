---
title: "PublicProfile"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java"]
---

# PublicProfile

El perfil público de una Cuenta: identidad, publicaciones a la venta paginadas, estadísticas y reseñas recientes. Ver [[Public profile flow]].

## Guía de lectura

Datos y dependencias declaradas: `user`, `postPage`, `reviewStats`, `reviews`.

Operaciones para localizar en la fuente: `getUser`, `getPostPage`, `getReviewStats`, `getReviews`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostPage]], [[PublicUserProfile]], [[Review]], [[ReviewStats]].

Referenciado por: [[PublicProfileService]], [[PublicProfileServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java>), líneas 1–29.

```java
package ar.edu.itba.paw.models;

import java.util.List;

// El perfil publico de una Cuenta: sus publicaciones a la venta y la reputacion que le dejaron.
public final class PublicProfile {

    private final PublicUserProfile user;
    private final PostPage postPage;
    private final ReviewStats reviewStats;
    private final List<Review> reviews;

    public PublicProfile(final PublicUserProfile user, final PostPage postPage, final ReviewStats reviewStats,
                         final List<Review> reviews) {
        this.user = user;
        this.postPage = postPage;
        this.reviewStats = reviewStats;
        this.reviews = List.copyOf(reviews);
    }

    public PublicUserProfile getUser() { return user; }

    public PostPage getPostPage() { return postPage; }

    public ReviewStats getReviewStats() { return reviewStats; }

    // Las mas nuevas primero.
    public List<Review> getReviews() { return reviews; }
}
```
