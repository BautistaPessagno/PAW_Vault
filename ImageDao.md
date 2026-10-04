---
title: "ImageDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java"]
---

# ImageDao

Contrato de imágenes: crear, borrar si nadie la referencia y buscar exigiendo pertenencia a un post, un usuario o un álbum.

## Guía de lectura

Operaciones para localizar en la fuente: `findById`, `findPostImage`, `findUserAvatar`, `findAlbumCover`, `create`, `delete`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]].

Referenciado por: [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageServiceImpl]], [[ImageServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java>), líneas 1–23.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;

import java.util.Optional;

public interface ImageDao {

    Optional<Image> findById(long id);

    /** Own photos and the associated album cover, including the editing fallback. */
    Optional<Image> findPostImage(long postId, long imageId);

    /** The current avatar of a verified account. */
    Optional<Image> findUserAvatar(long userId, long imageId);

    Optional<Image> findAlbumCover(long albumId, long imageId);

    Image create(String contentType, byte[] data);

    /** Deletes an existing image only when no album or post references it. */
    boolean delete(long id);
}
```
