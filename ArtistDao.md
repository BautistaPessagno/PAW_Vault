---
title: "ArtistDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java"]
---

# ArtistDao

The persistence contract exposes only `findOrCreate(name)`. [[ArtistJdbcDao]] searches by exact name and inserts if absent. The caller [[ArtistServiceImpl]] supplies the normalized name. The find-then-insert sequence is not an atomic upsert; database uniqueness decides races.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistJdbcDao]], [[ArtistServiceImpl]].

Tests: [[ArtistJdbcDaoTest]], [[ArtistServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;

public interface ArtistDao {
    Artist findOrCreate(String name);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
