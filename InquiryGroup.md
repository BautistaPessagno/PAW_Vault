---
title: "InquiryGroup"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java"]
---

# InquiryGroup

Una publicación y las consultas que la tocaron: la unidad por la que agrupan y paginan las dos bandejas. Es una proyección de lectura, no una tabla.

## Guía de lectura

Datos y dependencias declaradas: `postId`, `albumId`, `title`, `artistName`, `sellerUsername`, `coverImageId`, `postStatus`, `inquiries`.

Operaciones para localizar en la fuente: `getPostId`, `getAlbumId`, `isPostDeleted`, `getTitle`, `getArtistName`, `getSellerUsername`, `getCoverImageId`, `getPostStatus`, `getInquiries`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquirySummary]], [[PostStatus]].

Referenciado por: [[InquiryPage]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java>), líneas 1–44.

```java
package ar.edu.itba.paw.models;

import java.util.List;

/*
 * Una publicacion y las consultas que la tocaron, que la bandeja agrupa por publicacion
 * de los dos lados: las que recibio el vendedor y las que mando el comprador. Es una
 * proyeccion de lectura: no agrega una tabla ni un estado comercial nuevo.
 */
public final class InquiryGroup {
    private final Long postId;
    private final long albumId;
    private final String title;
    private final String artistName;
    private final String sellerUsername;
    private final Long coverImageId;
    private final PostStatus postStatus;
    private final List<InquirySummary> inquiries;

    public InquiryGroup(final Long postId, final long albumId, final String title, final String artistName,
                        final String sellerUsername, final Long coverImageId,
                        final PostStatus postStatus, final List<InquirySummary> inquiries) {
        this.postId = postId;
        this.albumId = albumId;
        this.title = title;
        this.artistName = artistName;
        this.sellerUsername = sellerUsername;
        this.coverImageId = coverImageId;
        this.postStatus = postStatus;
        this.inquiries = List.copyOf(inquiries);
    }

    public Long getPostId() { return postId; }
    public long getAlbumId() { return albumId; }
    public boolean isPostDeleted() { return postId == null; }
    public String getTitle() { return title; }
    public String getArtistName() { return artistName; }
    // Quien publica es uno solo por publicacion: lo usa la vista de enviadas, donde
    // repetirlo en cada consulta del grupo seria repetir el mismo nombre.
    public String getSellerUsername() { return sellerUsername; }
    public Long getCoverImageId() { return coverImageId; }
    public PostStatus getPostStatus() { return postStatus; }
    public List<InquirySummary> getInquiries() { return inquiries; }
}
```
