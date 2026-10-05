---
title: "Review"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Review.java"]
---

# Review

Calificación de una parte a la otra en una venta confirmada: consulta, autor, destinatario, nombre y foto del autor, puntaje, comentario, si está activa y fecha. Ver [[Reviews flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `inquiryId`, `authorId`, `subjectId`, `authorUsername`, `authorAvatarImageId`, `rating`, `body`, `active`, `createdAt`.

Operaciones para localizar en la fuente: `getId`, `getInquiryId`, `getAuthorId`, `getSubjectId`, `getAuthorUsername`, `getAuthorAvatarImageId`, `getRating`, `getBody`, `isActive`, `getCreatedAt`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryDetail]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[ReviewDao]], [[ReviewForm]], [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewPage]], [[ReviewService]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Review.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Review.java>), líneas 1–42.

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;

public final class Review {
    private final long id;
    private final long inquiryId;
    private final long authorId;
    private final long subjectId;
    private final String authorUsername;
    private final Long authorAvatarImageId;
    private final int rating;
    private final String body;
    private final boolean active;
    private final LocalDateTime createdAt;

    public Review(final long id, final long inquiryId, final long authorId, final long subjectId,
                  final String authorUsername, final Long authorAvatarImageId, final int rating,
                  final String body, final boolean active, final LocalDateTime createdAt) {
        this.id = id;
        this.inquiryId = inquiryId;
        this.authorId = authorId;
        this.subjectId = subjectId;
        this.authorUsername = authorUsername;
        this.authorAvatarImageId = authorAvatarImageId;
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
    public Long getAuthorAvatarImageId() { return authorAvatarImageId; }
    public int getRating() { return rating; }
    public String getBody() { return body; }
    public boolean isActive() { return active; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```
