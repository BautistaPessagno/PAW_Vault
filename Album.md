---
title: "Album"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/Album.java"]
---

# Album

A catalog work, identified by normalized title, artist ID, and release year. The database ID is a separate surrogate key. `coverPath` is presentation data and does not participate in uniqueness. `artistId` is a primitive `long`, not an embedded [[Artist]]. [[AlbumJdbcDao]] creates it; [[PostServiceImpl]] uses its ID to create a [[Post]]. Getters expose the immutable constructor values.

## Connections

Project types referenced: none.

Referenced by: [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumService]], [[AlbumServiceImpl]], [[PostServiceImpl]].

Tests: [[AlbumJdbcDaoTest]], [[AlbumServiceImplTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `title` | `String` |
| `artistId` | `long` |
| `releaseYear` | `int` |
| `coverPath` | `String` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Album.java, lines 1–38](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Album.java>)

```java
package ar.edu.itba.paw.models;

public class Album {
    private final long id;
    private final String title;
    private final long artistId;
    private final int releaseYear;
    private final String coverPath;

    public Album(final long id, final String title, final long artistId, final int releaseYear,
                 final String coverPath) {
        this.id = id;
        this.title = title;
        this.artistId = artistId;
        this.releaseYear = releaseYear;
        this.coverPath = coverPath;
    }

    public long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public long getArtistId() {
        return artistId;
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
