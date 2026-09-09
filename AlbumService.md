---
title: "AlbumService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java"]
---

# AlbumService

The catalog service contract exposes `getFeatured()` with no caller-selected limit and `findOrCreate(title, artistId, releaseYear)` with no caller-selected cover. [[AlbumServiceImpl]] owns the limit of eight, title normalization and fixed cover choice. [[PostServiceImpl]] uses the write method; the current landing uses PostService instead of the catalog read method.

## Connections

Project types referenced: [[Album]], [[AlbumSummary]].

Referenced by: [[AlbumServiceImpl]], [[PostServiceImpl]].

Tests: [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.AlbumSummary;

import java.util.List;

public interface AlbumService {
    List<AlbumSummary> getFeatured();

    Album findOrCreate(String title, long artistId, int releaseYear);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
