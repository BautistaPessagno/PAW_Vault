---
title: "PostInterestNotification"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java"]
---

# PostInterestNotification

An immutable payload crossing from [[PostServiceImpl]] to [[EmailServiceImpl]]. It carries post ID, private recipient address, contact name and email, album title, artist name and year. It has no persistence mapping and creates no contact-request row. The post ID is used in logs; contact email becomes Reply-To; the remaining fields populate the HTML template.

## Connections

Project types referenced: none.

Referenced by: [[EmailService]], [[EmailServiceImpl]], [[PostServiceImpl]].

Tests: [[EmailServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java, lines 1–52](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java>)

```java
package ar.edu.itba.paw.services;

public final class PostInterestNotification {

    private final long postId;
    private final String publisherEmail;
    private final String contactName;
    private final String contactEmail;
    private final String albumTitle;
    private final String artistName;
    private final int releaseYear;

    public PostInterestNotification(final long postId, final String publisherEmail, final String contactName,
                                    final String contactEmail, final String albumTitle, final String artistName,
                                    final int releaseYear) {
        this.postId = postId;
        this.publisherEmail = publisherEmail;
        this.contactName = contactName;
        this.contactEmail = contactEmail;
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

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
