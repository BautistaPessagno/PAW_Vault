---
title: "InquiryGroup"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java"]
---

# InquiryGroup

Read projection for one inbox group: post ID (null when the publication was deleted), title, artist, seller display name, cover image ID, post status and an immutable list of its [[InquirySummary]] rows. [[InquiryServiceImpl]] builds groups from DAO rows ordered newest first; both inbox views render one group per publication through ui:inbox-group-header. It adds no table or commercial state.

## Connections

Project types referenced: [[InquirySummary]], [[PostStatus]].

Referenced by: [[InquiryPage]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java, lines 1–41](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java>)

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
    private final String title;
    private final String artistName;
    private final String sellerUsername;
    private final Long coverImageId;
    private final PostStatus postStatus;
    private final List<InquirySummary> inquiries;

    public InquiryGroup(final Long postId, final String title, final String artistName,
                        final String sellerUsername, final Long coverImageId,
                        final PostStatus postStatus, final List<InquirySummary> inquiries) {
        this.postId = postId;
        this.title = title;
        this.artistName = artistName;
        this.sellerUsername = sellerUsername;
        this.coverImageId = coverImageId;
        this.postStatus = postStatus;
        this.inquiries = List.copyOf(inquiries);
    }

    public Long getPostId() { return postId; }
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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
