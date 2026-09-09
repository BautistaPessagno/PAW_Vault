---
title: "AlbumDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java"]
---

# AlbumDao

Catalog identity lookup and insert contract. findByArtistTitleYear returns Optional<Album>; create accepts nullable coverImageId. The unused findFeatured catalog API and [[AlbumSummary]] projection have been removed. Landing reads [[PostDao]] instead.

## Connections

Project types referenced: [[Album]].

Referenced by: [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java, lines 1–11](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;

import java.util.Optional;

public interface AlbumDao {
    Optional<Album> findByArtistTitleYear(String title, long artistId, int releaseYear);

    Album create(String title, long artistId, int releaseYear, Long coverImageId);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
