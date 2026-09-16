---
title: "AlbumServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# AlbumServiceImpl

Normalizes title with trim and Locale.ROOT lowercasing, then looks up artist/title/year under a transaction. Existing albums keep their genre and legacy cover; new albums store the supplied genre without an exemplar image.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumService]], [[Genre]].

Referenced by: [[AlbumServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;

@Service
public class AlbumServiceImpl implements AlbumService {

    private final AlbumDao albumDao;
    @Autowired
    public AlbumServiceImpl(final AlbumDao albumDao) {
        this.albumDao = albumDao;
    }

    /*
     * El album conserva solamente datos factuales compartidos. Las fotografias del
     * ejemplar pertenecen a la publicacion que lo ofrece.
     */
    @Override
    @Transactional
    public Album findOrCreate(final String title, final long artistId, final int releaseYear, final Genre genre) {
        final String normalizedTitle = title.trim().toLowerCase(Locale.ROOT);
        return albumDao.findByArtistTitleYear(normalizedTitle, artistId, releaseYear)
                .orElseGet(() -> albumDao.create(normalizedTitle, artistId, releaseYear, genre));
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
