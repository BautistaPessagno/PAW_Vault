---
title: "AlbumServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# AlbumServiceImpl

`getFeatured` asks [[AlbumDao]] for eight album summaries and has no transaction annotation in this snapshot. `findOrCreate` is transactional, trims and lowercases the title, and supplies `/images/covers/versus.png`. It delegates identity lookup to [[AlbumJdbcDao]], which preserves the stored cover on reuse. The featured method orders catalog entries differently from the current landing.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumService]], [[AlbumSummary]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: [[AlbumServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.AlbumSummary;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Locale;

@Service
public class AlbumServiceImpl implements AlbumService {

    private static final int FEATURED_LIMIT = 8;
    private static final String DEFAULT_COVER_PATH = "/images/covers/versus.png";

    private final AlbumDao albumDao;

    @Autowired
    public AlbumServiceImpl(final AlbumDao albumDao) {
        this.albumDao = albumDao;
    }

    @Override
    public List<AlbumSummary> getFeatured() {
        return albumDao.findFeatured(FEATURED_LIMIT);
    }

    @Override
    @Transactional
    public Album findOrCreate(final String title, final long artistId, final int releaseYear) {
        return albumDao.findOrCreate(title.trim().toLowerCase(Locale.ROOT), artistId, releaseYear, DEFAULT_COVER_PATH);
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
