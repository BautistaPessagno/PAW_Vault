---
title: "ImageService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java"]
---

# ImageService

Contrato de imágenes: lectura por pertenencia (post, avatar, álbum), alta validada, borrado condicional y galería.

## Guía de lectura

Operaciones para localizar en la fuente: `findPostImage`, `findUserAvatar`, `findAlbumCover`, `create`, `delete`, `findGalleryImageIds`, `replaceGallery`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]].

Referenciado por: [[ImageController]], [[ImageServiceImpl]], [[ImageServiceImplTest]], [[InMemoryImageService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java>), líneas 1–30.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;

import java.util.List;
import java.util.Optional;

public interface ImageService {

    // Fotos propias de la publicacion y la portada de su album, incluida la de respaldo al editar.
    Optional<Image> findPostImage(long postId, long imageId);

    // La foto de perfil vigente de una Cuenta verificada.
    Optional<Image> findUserAvatar(long userId, long imageId);

    Optional<Image> findAlbumCover(long albumId, long imageId);

    // Lanza InvalidImageException si no cumple ImageRules.
    Image create(String contentType, byte[] data);

    // Borra la imagen solo si ningun album, publicacion ni Cuenta la referencia.
    boolean delete(long id);

    // Las fotos adicionales de una publicacion, en el orden en que se muestran. La principal
    // vive en el post.
    List<Long> findGalleryImageIds(long postId);

    // Reemplaza las fotos adicionales de la publicacion por estas, en este orden.
    void replaceGallery(long postId, List<Long> imageIds);
}
```
