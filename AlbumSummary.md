---
title: "AlbumSummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java"]
---

# AlbumSummary

A read projection containing album ID, title, artist name, year and cover path. [[AlbumJdbcDao]] joins albums with artists to create it in one query. It replaces the artist ID with display text for consumers of [[AlbumService]]. The current landing consumes [[PostSummary]] instead, so this older catalog projection has no current controller caller.

## Connections

Project types referenced: none.

Referenced by: [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumService]], [[AlbumServiceImpl]].

Tests: [[AlbumJdbcDaoTest]]. See [[Testing and evidence]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `title` | `String` |
| `artistName` | `String` |
| `releaseYear` | `int` |
| `coverPath` | `String` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java, lines 1–38](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java>)

```java
package ar.edu.itba.paw.models;

public class AlbumSummary {
    private final long id;
    private final String title;
    private final String artistName;
    private final int releaseYear;
    private final String coverPath;

    public AlbumSummary(final long id, final String title, final String artistName, final int releaseYear,
                        final String coverPath) {
        this.id = id;
        this.title = title;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
        this.coverPath = coverPath;
    }

    public long getId() {
        return id;
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
