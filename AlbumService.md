---
title: "AlbumService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java"]
---

# AlbumService

Find or create the factual artist/title/year catalog identity with optional genre. Image storage is handled by publishing, outside this catalog API.

## Connections

Project types referenced: [[Album]], [[Genre]].

Referenced by: [[AlbumServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java, lines 1–8](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

public interface AlbumService {
    Album findOrCreate(String title, long artistId, int releaseYear, Genre genre);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
