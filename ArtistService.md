---
title: "ArtistService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java"]
---

# ArtistService

The business contract for resolving a normalized artist name. [[ArtistServiceImpl]] implements `findOrCreate`; [[PostServiceImpl]] calls it before resolving the album, because an album identity requires the artist ID.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;

public interface ArtistService {
    Artist findOrCreate(String name);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
