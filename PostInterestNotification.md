---
title: "PostInterestNotification"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java"]
---

# PostInterestNotification

Mail payload with post ID, seller address, authenticated buyer name/email, optional inquiry message and album facts. [[Inquiry]] stores the request independently of delivery; this payload is not a database entity.

## Connections

Project types referenced: none.

Referenced by: [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java, lines 1–59](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java>)

```java
package ar.edu.itba.paw.services;

public final class PostInterestNotification {

    private final long postId;
    private final String publisherEmail;
    private final String contactName;
    private final String contactEmail;
    private final String message;
    private final String albumTitle;
    private final String artistName;
    private final int releaseYear;

    public PostInterestNotification(final long postId, final String publisherEmail, final String contactName,
                                    final String contactEmail, final String message, final String albumTitle,
                                    final String artistName, final int releaseYear) {
        this.postId = postId;
        this.publisherEmail = publisherEmail;
        this.contactName = contactName;
        this.contactEmail = contactEmail;
        this.message = message;
        this.albumTitle = albumTitle;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
    }

    public long getPostId() {
        return postId;
    }

    public String getPublisherEmail() {
        return publisherEmail;
    }

    public String getContactName() {
        return contactName;
    }

    public String getContactEmail() {
        return contactEmail;
    }

    // null cuando el interesado no dejo ningun mensaje.
    public String getMessage() {
        return message;
    }

    public String getAlbumTitle() {
        return albumTitle;
    }

    public String getArtistName() {
        return artistName;
    }

    public int getReleaseYear() {
        return releaseYear;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
