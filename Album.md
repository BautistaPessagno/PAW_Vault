---
title: "Album"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Album.java"]
---

# Album

Shared catalog work identified by artist ID, normalized title and release year. Optional Genre is fixed when the identity is first created. coverImageId remains for historical album covers; new exemplar photos belong to [[Post]]. Reusing the identity preserves the stored album.

## Connections

Project types referenced: [[Genre]].

Referenced by: [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumService]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]], [[EmailServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Album.java, lines 1–44](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Album.java>)

```java
package ar.edu.itba.paw.models;

public class Album {
    private final long id;
    private final String title;
    private final long artistId;
    private final int releaseYear;
    private final Genre genre;
    private final Long coverImageId;

    public Album(final long id, final String title, final long artistId, final int releaseYear,
                 final Genre genre, final Long coverImageId) {
        this.id = id;
        this.title = title;
        this.artistId = artistId;
        this.releaseYear = releaseYear;
        this.genre = genre;
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

    public Genre getGenre() {
        return genre;
    }

    public Long getCoverImageId() {
        return coverImageId;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
