---
title: "Album"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/Album.java"]
---

# Album

A catalog work identified by normalized title, artist ID and release year. coverImageId is a nullable Long referencing [[Image]], replacing coverPath. The cover does not participate in uniqueness. [[AlbumServiceImpl]] preserves the first stored album and its cover when another publisher reuses that identity.

## Connections

Project types referenced: none.

Referenced by: [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumService]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]], [[EmailServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Album.java, lines 1–38](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Album.java>)

```java
package ar.edu.itba.paw.models;

public class Album {
    private final long id;
    private final String title;
    private final long artistId;
    private final int releaseYear;
    private final Long coverImageId;

    public Album(final long id, final String title, final long artistId, final int releaseYear,
                 final Long coverImageId) {
        this.id = id;
        this.title = title;
        this.artistId = artistId;
        this.releaseYear = releaseYear;
        this.coverImageId = coverImageId;
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

    public Long getCoverImageId() {
        return coverImageId;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
