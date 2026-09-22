---
title: "AlbumServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# AlbumServiceImpl

Trims the title and looks up artist/title/year case-insensitively under a transaction; a miss creates the album with the supplied genre and the title as typed. resolveForEdit does the same, then calls updateMetadata when the stored title text or genre differs, so an edit updates the shared catalog row for every publication of that album.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumService]], [[Genre]].

Referenced by: [[AlbumServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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
        final String trimmedTitle = title.trim();
        return albumDao.findByArtistTitleYear(trimmedTitle, artistId, releaseYear)
                .orElseGet(() -> albumDao.create(trimmedTitle, artistId, releaseYear, genre));
    }

    @Override
    @Transactional
    public Album resolveForEdit(final String title, final long artistId, final int releaseYear,
                                final Genre genre) {
        final String trimmedTitle = title.trim();
        final Album album = albumDao.findByArtistTitleYear(trimmedTitle, artistId, releaseYear)
                .orElseGet(() -> albumDao.create(trimmedTitle, artistId, releaseYear, genre));
        if (album.getTitle().equals(trimmedTitle) && album.getGenre() == genre) {
            return album;
        }
        return albumDao.updateMetadata(album.getId(), trimmedTitle, genre);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
