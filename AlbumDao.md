---
title: "AlbumDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java"]
---

# AlbumDao

Contrato de persistencia de álbumes: buscar por artista, título y año sin distinguir mayúsculas, crear y actualizar título y género. Lo implementa [[AlbumJdbcDao]].

## Guía de lectura

Operaciones para localizar en la fuente: `findByArtistTitleYear`, `create`, `updateMetadata`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[Genre]].

Referenciado por: [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>), líneas 1–14.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

import java.util.Optional;

public interface AlbumDao {
    Optional<Album> findByArtistTitleYear(String title, long artistId, int releaseYear);

    Album create(String title, long artistId, int releaseYear, Genre genre);

    Album updateMetadata(long id, String title, Genre genre);
}
```
