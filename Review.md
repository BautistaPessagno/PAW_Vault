---
title: "Review"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Review.java"]
---

# Review

Calificación de una parte a la otra en una venta confirmada: consulta, autor, destinatario, nombre del autor, puntaje, comentario, si está activa y fecha. Ver [[Reviews flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `inquiryId`, `authorId`, `subjectId`, `authorUsername`, `rating`, `body`, `active`, `createdAt`.

Operaciones para localizar en la fuente: `getId`, `getInquiryId`, `getAuthorId`, `getSubjectId`, `getAuthorUsername`, `getRating`, `getBody`, `isActive`, `getCreatedAt`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryDetail]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PublicProfile]], [[ReviewDao]], [[ReviewForm]], [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewService]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Review.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Review.java>), líneas 1–39.

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;

public final class Review {
    private final long id;
    private final long inquiryId;
    private final long authorId;
    private final long subjectId;
    private final String authorUsername;
    private final int rating;
    private final String body;
    private final boolean active;
    private final LocalDateTime createdAt;

    public Review(final long id, final long inquiryId, final long authorId, final long subjectId,
                  final String authorUsername, final int rating, final String body, final boolean active,
                  final LocalDateTime createdAt) {
        this.id = id;
        this.inquiryId = inquiryId;
        this.authorId = authorId;
        this.subjectId = subjectId;
        this.authorUsername = authorUsername;
        this.rating = rating;
        this.body = body;
        this.active = active;
        this.createdAt = createdAt;
    }

    public long getId() { return id; }
    public long getInquiryId() { return inquiryId; }
    public long getAuthorId() { return authorId; }
    public long getSubjectId() { return subjectId; }
    public String getAuthorUsername() { return authorUsername; }
    public int getRating() { return rating; }
    public String getBody() { return body; }
    public boolean isActive() { return active; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```
