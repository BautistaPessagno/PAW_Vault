---
title: "PostSummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSummary.java"]
---

# PostSummary

A read projection for a publication joined with its user, album and artist. Its `id` is the Post ID, not the album ID. [[LandingController]] places a list of these in `posts`; [[PostContactController]] places one in `post`. `publisherEmail` is carried server-side for [[PostServiceImpl]] to address mail, but the current JSPs do not render it. One four-table query supplies every field.

## Connections

Project types referenced: none.

Referenced by: [[PostContactController]], [[PostDao]], [[PostJdbcDao]], [[PostService]], [[PostServiceImpl]].

Tests: [[PostJdbcDaoTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `userId` | `long` |
| `publisherEmail` | `String` |
| `albumId` | `long` |
| `title` | `String` |
| `artistName` | `String` |
| `releaseYear` | `int` |
| `coverPath` | `String` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

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
    private final String coverPath;

    public PostSummary(final long id, final long userId, final String publisherEmail, final long albumId,
                       final String title, final String artistName, final int releaseYear,
                       final String coverPath) {
        this.id = id;
        this.userId = userId;
        this.publisherEmail = publisherEmail;
        this.albumId = albumId;
        this.title = title;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
        this.coverPath = coverPath;
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

    public String getCoverPath() {
        return coverPath;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
