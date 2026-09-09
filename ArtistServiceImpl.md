---
title: "ArtistServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java"]
---

# ArtistServiceImpl

`findOrCreate` applies `name.trim().toLowerCase(Locale.ROOT)` and delegates to [[ArtistDao]] inside a transaction. Trimming removes outer spaces; lowercasing is locale-independent. Accents and internal whitespace are not normalized. During [[Publish flow]] this call joins the outer publish transaction.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]], [[ArtistService]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: [[ArtistServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.persistence.ArtistDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;

@Service
public class ArtistServiceImpl implements ArtistService {

    private final ArtistDao artistDao;

    @Autowired
    public ArtistServiceImpl(final ArtistDao artistDao) {
        this.artistDao = artistDao;
    }

    @Override
    @Transactional
    public Artist findOrCreate(final String name) {
        return artistDao.findOrCreate(name.trim().toLowerCase(Locale.ROOT));
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
