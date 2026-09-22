---
title: "AlbumService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java"]
---

# AlbumService

findOrCreate resolves the factual artist/title/year identity with a required genre for publishing. resolveForEdit resolves the same identity for an owner's edit and rewrites the shared album when the typed title text or genre differs. Image storage belongs to publishing, outside this catalog API.

## Connections

Project types referenced: [[Album]], [[Genre]].

Referenced by: [[AlbumServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java, lines 1–10](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

public interface AlbumService {
    Album findOrCreate(String title, long artistId, int releaseYear, Genre genre);

    Album resolveForEdit(String title, long artistId, int releaseYear, Genre genre);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
