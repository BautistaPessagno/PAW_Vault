---
title: "InquiryAcceptedNotification"
categories: ["History"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "historical"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryAcceptedNotification.java"]
---

# InquiryAcceptedNotification

> Histórico. Este archivo ya no existe con ese nombre en `41c32af`. El código inferior conserva su revisión original. Fue reemplazado por [[InquiryUpdateNotification]].

Mail payload for the accepted buyer: inquiry ID, buyer email, album title, artist and release year. [[InquiryServiceImpl]] builds it inside the sale transaction and hands it to [[EmailService]] after commit. It is not a database entity.

## Connections

Project types referenced: none.

Referenced by: [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryAcceptedNotification.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryAcceptedNotification.java>)

```java
package ar.edu.itba.paw.services;

public final class InquiryAcceptedNotification {
    private final long inquiryId;
    private final String buyerEmail;
    private final String albumTitle;
    private final String artistName;
    private final int releaseYear;

    public InquiryAcceptedNotification(final long inquiryId, final String buyerEmail, final String albumTitle,
                                       final String artistName, final int releaseYear) {
        this.inquiryId = inquiryId;
        this.buyerEmail = buyerEmail;
        this.albumTitle = albumTitle;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
    }

    public long getInquiryId() { return inquiryId; }
    public String getBuyerEmail() { return buyerEmail; }
    public String getAlbumTitle() { return albumTitle; }
    public String getArtistName() { return artistName; }
    public int getReleaseYear() { return releaseYear; }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
