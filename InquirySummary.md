---
title: "InquirySummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java"]
---

# InquirySummary

Inbox projection with buyer/seller display names, album title/artist, optional message, inquiry status and post status. isPending and isPostAvailable control action visibility; service authorization still checks ownership.

## Connections

Project types referenced: [[InquiryStatus]], [[PostStatus]].

Referenced by: [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java>)

```java
package ar.edu.itba.paw.models;

/*
 * Una consulta como la muestra la bandeja: quien la mando, quien la recibio, que album
 * es y en que estado quedaron la consulta y la publicacion.
 */
public final class InquirySummary {
    private final long id;
    private final String buyerUsername;
    private final String sellerUsername;
    private final String title;
    private final String artistName;
    private final String message;
    private final InquiryStatus status;
    private final PostStatus postStatus;

    public InquirySummary(final long id, final String buyerUsername, final String sellerUsername,
                          final String title, final String artistName, final String message,
                          final InquiryStatus status, final PostStatus postStatus) {
        this.id = id;
        this.buyerUsername = buyerUsername;
        this.sellerUsername = sellerUsername;
        this.title = title;
        this.artistName = artistName;
        this.message = message;
        this.status = status;
        this.postStatus = postStatus;
    }

    public long getId() { return id; }
    public String getBuyerUsername() { return buyerUsername; }
    public String getSellerUsername() { return sellerUsername; }
    public String getTitle() { return title; }
    public String getArtistName() { return artistName; }
    public String getMessage() { return message; }
    public InquiryStatus getStatus() { return status; }
    public PostStatus getPostStatus() { return postStatus; }

    // La bandeja solo ofrece aceptar o rechazar mientras la consulta sigue abierta y el
    // ejemplar sigue a la venta.
    public boolean isPending() { return status == InquiryStatus.PENDING; }
    public boolean isPostAvailable() { return postStatus == PostStatus.AVAILABLE; }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
