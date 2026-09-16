---
title: "ArtistDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java"]
---

# ArtistDao

Find or create an artist and list all artists for the landing filter. [[ArtistJdbcDao]] returns the list in alphabetical name order.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistJdbcDao]], [[ArtistJdbcDaoTest]], [[ArtistServiceImpl]], [[ArtistServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java, lines 1–11](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistDao {
    Artist findOrCreate(String name);

    List<Artist> findAll();
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
