---
title: "ArtistService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java"]
---

# ArtistService

findOrCreate resolves an artist through its normalized identity while keeping the typed display name. resolveForEdit also rewrites the shared display name when it differs. findSuggestions returns up to five ranked names for the publish-form autocomplete.

## Connections

Project types referenced: [[Artist]].

Referenced by: [[ArtistServiceImpl]], [[ArtistSuggestionController]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java, lines 1–13](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistService {
    Artist findOrCreate(String name);

    Artist resolveForEdit(String name);

    List<Artist> findSuggestions(String query);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
