---
title: "Genre"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Genre.java"]
---

# Genre

Fifteen catalog genre values, including OTHER. Stored on Album, optional for new and legacy data, with localized labels in [[Localization]]. It does not participate in album identity.

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
