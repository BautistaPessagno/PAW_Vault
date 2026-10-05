---
title: "Inquiry"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Inquiry.java"]
---

# Inquiry

La Consulta tal como está guardada: id, post (nulo si la publicación fue eliminada), comprador y [[InquiryStatus]]. Ver [[Inquiry and sale flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `postId`, `buyerId`, `status`.

Operaciones para localizar en la fuente: `getId`, `getPostId`, `isPostDeleted`, `getBuyerId`, `getStatus`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquiryStatus]].

Referenciado por: [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Inquiry.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Inquiry.java>), líneas 1–39.

```java
package ar.edu.itba.paw.models;

/*
 * Una consulta tal como esta guardada. postId es null cuando la publicacion consultada fue
 * eliminada: la consulta sobrevive, pero ya no hay post sobre el que actuar.
 */
public final class Inquiry {
    private final long id;
    private final Long postId;
    private final long buyerId;
    private final InquiryStatus status;

    public Inquiry(final long id, final Long postId, final long buyerId, final InquiryStatus status) {
        this.id = id;
        this.postId = postId;
        this.buyerId = buyerId;
        this.status = status;
    }

    public long getId() {
        return id;
    }

    public Long getPostId() {
        return postId;
    }

    public boolean isPostDeleted() {
        return postId == null;
    }

    public long getBuyerId() {
        return buyerId;
    }

    public InquiryStatus getStatus() {
        return status;
    }
}
```
