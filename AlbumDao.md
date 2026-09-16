---
title: "AlbumDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java"]
---

# AlbumDao

Catalog identity lookup and insertion with optional genre. New inserts do not accept an exemplar image; the stored album cover remains a legacy fallback.

## Connections

Project types referenced: [[Album]], [[Genre]].

Referenced by: [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

import java.util.Optional;

public interface AlbumDao {
    Optional<Album> findByArtistTitleYear(String title, long artistId, int releaseYear);

    Album create(String title, long artistId, int releaseYear, Genre genre);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
