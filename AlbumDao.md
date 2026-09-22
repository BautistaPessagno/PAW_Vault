---
title: "AlbumDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java"]
---

# AlbumDao

Catalog identity lookup with a case-insensitive title, insertion with a genre, and updateMetadata to rewrite the title text and genre of an existing album. New inserts do not accept an exemplar image; the stored album cover remains a legacy fallback.

## Connections

Project types referenced: [[Album]], [[Genre]].

Referenced by: [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

import java.util.Optional;

public interface AlbumDao {
    Optional<Album> findByArtistTitleYear(String title, long artistId, int releaseYear);

    Album create(String title, long artistId, int releaseYear, Genre genre);

    Album updateMetadata(long id, String title, Genre genre);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
