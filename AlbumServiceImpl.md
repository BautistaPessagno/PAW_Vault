---
title: "AlbumServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# AlbumServiceImpl

Busca o crea el álbum por artista, título y año. Al editar una publicación, si el título o el género difieren, actualiza el registro compartido. El álbum guarda solo datos factuales; las fotos son del post.

## Guía de lectura

Datos y dependencias declaradas: `albumDao`.

Operaciones para localizar en la fuente: `findOrCreate`, `resolveForEdit`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[AlbumDao]], [[AlbumService]], [[Genre]].

Referenciado por: [[AlbumServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>), líneas 1–43.

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
