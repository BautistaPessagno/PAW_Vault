---
title: "AlbumService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java"]
---

# AlbumService

Catalog findOrCreate contract with title, artist ID, year, coverContentType and coverData. [[AlbumServiceImpl]] defines normalization and first-cover ownership. The former getFeatured API has been removed; [[PostService]] serves landing reads.

## Connections

Project types referenced: [[Album]].

Referenced by: [[AlbumServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;

public interface AlbumService {
    Album findOrCreate(String title, long artistId, int releaseYear, String coverContentType, byte[] coverData);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
