---
title: "AlbumDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java"]
---

# AlbumDao

The persistence contract for the albums table. `findFeatured(limit)` returns joined [[AlbumSummary]] objects; `findOrCreate(title, artistId, releaseYear, coverPath)` returns the existing identity or inserts a new [[Album]]. Input normalization is a service responsibility. The implementation is [[AlbumJdbcDao]]. Existing album cover paths remain unchanged.

## Connections

Project types referenced: [[Album]], [[AlbumSummary]].

Referenced by: [[AlbumJdbcDao]], [[AlbumServiceImpl]].

Tests: [[AlbumJdbcDaoTest]], [[AlbumServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.AlbumSummary;

import java.util.List;

public interface AlbumDao {
    List<AlbumSummary> findFeatured(int limit);

    Album findOrCreate(String title, long artistId, int releaseYear, String coverPath);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
