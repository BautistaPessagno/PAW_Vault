---
title: "ArtistServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java"]
---

# ArtistServiceImpl

Trims and lowercases artist names before findOrCreate. findAll delegates under a read-only transaction to the alphabetical DAO query.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]], [[ArtistService]].

Referenced by: [[ArtistServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java, lines 1–33](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.persistence.ArtistDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;
import java.util.List;

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

    @Override
    @Transactional(readOnly = true)
    public List<Artist> findAll() {
        return artistDao.findAll();
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
