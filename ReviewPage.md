---
title: "ReviewPage"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ReviewPage.java"]
---

# ReviewPage

Una página de reseñas del perfil público para un rol ([[ReviewSubjectRole]]): las reseñas, las estadísticas de ese rol, el número de página y si hay anterior o siguiente. Ver [[Public profile flow]].

## Guía de lectura

Datos y dependencias declaradas: `reviews`, `role`, `stats`, `pageNumber`, `hasPrevious`, `hasNext`.

Operaciones para localizar en la fuente: `getReviews`, `getRole`, `getStats`, `getPageNumber`, `isHasPrevious`, `isHasNext`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewStats]], [[ReviewSubjectRole]].

Referenciado por: [[PublicProfile]], [[ReviewService]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ReviewPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewPage.java>), líneas 1–29.

```java
package ar.edu.itba.paw.models;

import java.util.List;

public final class ReviewPage {
    private final List<Review> reviews;
    private final ReviewSubjectRole role;
    private final ReviewStats stats;
    private final int pageNumber;
    private final boolean hasPrevious;
    private final boolean hasNext;

    public ReviewPage(final List<Review> reviews, final ReviewSubjectRole role, final ReviewStats stats,
                      final int pageNumber, final int totalPages) {
        this.reviews = List.copyOf(reviews);
        this.role = role;
        this.stats = stats;
        this.pageNumber = pageNumber;
        this.hasPrevious = pageNumber > 1;
        this.hasNext = pageNumber < totalPages;
    }

    public List<Review> getReviews() { return reviews; }
    public ReviewSubjectRole getRole() { return role; }
    public ReviewStats getStats() { return stats; }
    public int getPageNumber() { return pageNumber; }
    public boolean isHasPrevious() { return hasPrevious; }
    public boolean isHasNext() { return hasNext; }
}
```
