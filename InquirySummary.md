---
title: "InquirySummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java"]
---

# InquirySummary

Inbox row projection: inquiry ID, nullable post ID, album ID and seller ID, buyer and seller display names, album title/artist, cover image ID, optional message, inquiry status and nullable post status. For a deleted publication the album and seller come from the copy stored on the inquiry. isPending and isPostAvailable control action visibility; the service still checks ownership.

## Connections

Project types referenced: [[InquiryStatus]], [[PostStatus]].

Referenced by: [[InquiryDao]], [[InquiryGroup]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java, lines 1–59](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java>)

```java
package ar.edu.itba.paw.models;

/*
 * Una consulta como la muestra la bandeja: quien la mando, quien la recibio, que album
 * es y en que estado quedaron la consulta y la publicacion. Si la publicacion fue
 * eliminada, postId y postStatus vienen en null y el album y el vendedor salen de la
 * copia que guarda la consulta. albumId y sellerId identifican ese vinilo aunque la
 * publicacion ya no exista.
 */
public final class InquirySummary {
    private final long id;
    private final Long postId;
    private final long albumId;
    private final long sellerId;
    private final String buyerUsername;
    private final String sellerUsername;
    private final String title;
    private final String artistName;
    private final Long coverImageId;
    private final String message;
    private final InquiryStatus status;
    private final PostStatus postStatus;

    public InquirySummary(final long id, final Long postId, final long albumId, final long sellerId,
                          final String buyerUsername, final String sellerUsername, final String title,
                          final String artistName, final Long coverImageId, final String message,
                          final InquiryStatus status, final PostStatus postStatus) {
        this.id = id;
        this.postId = postId;
        this.albumId = albumId;
        this.sellerId = sellerId;
        this.buyerUsername = buyerUsername;
        this.sellerUsername = sellerUsername;
        this.title = title;
        this.artistName = artistName;
        this.coverImageId = coverImageId;
        this.message = message;
        this.status = status;
        this.postStatus = postStatus;
    }

    public long getId() { return id; }
    public Long getPostId() { return postId; }
    public long getAlbumId() { return albumId; }
    public long getSellerId() { return sellerId; }
    public String getBuyerUsername() { return buyerUsername; }
    public String getSellerUsername() { return sellerUsername; }
    public String getTitle() { return title; }
    public String getArtistName() { return artistName; }
    public Long getCoverImageId() { return coverImageId; }
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
