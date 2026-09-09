---
title: "AlbumSummary"
categories: ["History"]
type: "historical-code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
source_commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
tags: ["codemap", "domain"]
sources: []
---

# AlbumSummary

> [!note] Historical source
> This type is absent at ff96f27. The text and excerpt below describe the previous implementation at 041ce34.

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

[models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java, lines 1–38](<https://bitbucket.org/itba/paw-2026b-14/src/041ce34404963b689d05443ca00abb7e75aa7f15/models/src/main/java/ar/edu/itba/paw/models/AlbumSummary.java>)

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
