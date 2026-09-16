---
title: "ArtistService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java"]
---

# ArtistService

Normalizes artist identity through its implementation and exposes all artists for the catalog filter.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistServiceImpl]], [[LandingController]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java, lines 1–11](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistService {
    Artist findOrCreate(String name);

    List<Artist> findAll();
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
