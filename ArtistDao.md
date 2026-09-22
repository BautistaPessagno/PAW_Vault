---
title: "ArtistDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java"]
---

# ArtistDao

findOrCreate receives both the display name and the precomputed normalized identity. updateDisplayName rewrites the shown name. findSuggestions receives a query already compacted by [[SearchText]] and returns a ranked, limited list. The former findAll listing for a landing filter has been removed.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistJdbcDao]], [[ArtistJdbcDaoTest]], [[ArtistServiceImpl]], [[ArtistServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java, lines 1–15](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistDao {
    Artist findOrCreate(String displayName, String normalizedName);

    Artist updateDisplayName(long id, String displayName);

    // normalizedQuery llega ya pasada por SearchText.compact: el ranking se
    // resuelve contra la columna search_phrase, sin traer la tabla entera.
    List<Artist> findSuggestions(String normalizedQuery, int limit);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
