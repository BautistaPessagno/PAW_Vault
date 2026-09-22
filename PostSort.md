---
title: "PostSort"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSort.java"]
---

# PostSort

Ten allowed orders: newest/oldest and ascending/descending price, title, artist or release year. [[PostJdbcDao]] maps each value to fixed SQL; default normalization chooses NEWEST.

## Connections

Project types referenced: none.

Referenced by: [[LandingController]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostSort.java, lines 1–15](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSort.java>)

```java
package ar.edu.itba.paw.models;

// Criterios de orden del listado de publicaciones. NEWEST es el default de la landing.
public enum PostSort {
    NEWEST,
    OLDEST,
    PRICE_ASC,
    PRICE_DESC,
    TITLE_ASC,
    TITLE_DESC,
    ARTIST_ASC,
    ARTIST_DESC,
    RELEASE_YEAR_DESC,
    RELEASE_YEAR_ASC
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
