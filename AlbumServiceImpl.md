---
title: "AlbumServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# AlbumServiceImpl

Normalizes title with trim and Locale.ROOT lowercase inside a transaction. Looks up the album before creating an image. Existing albums are returned unchanged, discarding any newly submitted cover without validating or storing it. For a new album, null/empty coverData yields null coverImageId; nonempty bytes go through [[ImageService]] before album insert. The image and album writes join the outer publish transaction. There is no automatic fixed cover or album-listing API.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumService]], [[ImageService]].

Referenced by: [[AlbumServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java, lines 1–44](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;

@Service
public class AlbumServiceImpl implements AlbumService {

    private final AlbumDao albumDao;
    private final ImageService imageService;

    @Autowired
    public AlbumServiceImpl(final AlbumDao albumDao, final ImageService imageService) {
        this.albumDao = albumDao;
        this.imageService = imageService;
    }

    /*
     * La portada pertenece al album y la fija quien lo incorpora al catalogo: si el
     * album ya existe, la imagen recibida se descarta sin guardarla. Se busca antes
     * de crear para no dejar imagenes huerfanas en el camino comun.
     */
    @Override
    @Transactional
    public Album findOrCreate(final String title, final long artistId, final int releaseYear,
                              final String coverContentType, final byte[] coverData) {
        final String normalizedTitle = title.trim().toLowerCase(Locale.ROOT);
        return albumDao.findByArtistTitleYear(normalizedTitle, artistId, releaseYear)
                .orElseGet(() -> albumDao.create(normalizedTitle, artistId, releaseYear,
                        storeCover(coverContentType, coverData)));
    }

    private Long storeCover(final String coverContentType, final byte[] coverData) {
        if (coverData == null || coverData.length == 0) {
            return null;
        }
        return imageService.create(coverContentType, coverData).getId();
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
