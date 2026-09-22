---
title: "Genre"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Genre.java"]
---

# Genre

Fifteen catalog genre values, including OTHER. Stored on [[Album]] and now required: PublishForm rejects a missing genre, and schema.sql backfills legacy nulls to OTHER before adding NOT NULL and a CHECK listing the fifteen names. Localized labels live in [[Localization]]. It does not participate in album identity, and an owner's edit can change the shared album's genre.

## Connections

Project types referenced: none.

Referenced by: [[Album]], [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumService]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]], [[LandingController]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]], [[PublishController]], [[PublishForm]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Genre.java, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Genre.java>)

```java
package ar.edu.itba.paw.models;

public enum Genre {
    ROCK,
    POP,
    JAZZ,
    BLUES,
    SOUL_FUNK,
    HIP_HOP,
    ELECTRONIC,
    CLASSICAL,
    TANGO,
    FOLKLORE,
    CUMBIA,
    REGGAE,
    METAL,
    PUNK,
    OTHER
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
