---
title: "PostSummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSummary.java"]
---

# PostSummary

Joined read projection for a Post, publisher and album/artist. Contains id, userId, publisherEmail, albumId, title, artistName, releaseYear and nullable Long coverImageId. [[PostJdbcDao]] reads only the image ID, not its bytes. [[UI components]] chooses the placeholder or /covers/{id}; publisherEmail stays server-side for [[Contact flow]].

## Connections

Project types referenced: none.

Referenced by: [[PostContactController]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostSummary.java, lines 1–57](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSummary.java>)

```java
package ar.edu.itba.paw.models;

public class PostSummary {
    private final long id;
    private final long userId;
    private final String publisherEmail;
    private final long albumId;
    private final String title;
    private final String artistName;
    private final int releaseYear;
    private final Long coverImageId;

    public PostSummary(final long id, final long userId, final String publisherEmail, final long albumId,
                       final String title, final String artistName, final int releaseYear,
                       final Long coverImageId) {
        this.id = id;
        this.userId = userId;
        this.publisherEmail = publisherEmail;
        this.albumId = albumId;
        this.title = title;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
        this.coverImageId = coverImageId;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getPublisherEmail() {
        return publisherEmail;
    }

    public long getAlbumId() {
        return albumId;
    }

    public String getTitle() {
        return title;
    }

    public String getArtistName() {
        return artistName;
    }

    public int getReleaseYear() {
        return releaseYear;
    }

    public Long getCoverImageId() {
        return coverImageId;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
