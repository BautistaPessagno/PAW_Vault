---
title: "InMemoryImageService"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java"]
---

# InMemoryImageService

Doble de [[ImageService]] en memoria para los tests de services: aplica las mismas [[ImageRules]] y permite assertear el estado guardado sin `Mockito.verify`.

## Guía de lectura

Datos y dependencias declaradas: `images`, `galleries`, `nextId`.

Operaciones para localizar en la fuente: `findPostImage`, `findUserAvatar`, `findAlbumCover`, `create`, `delete`, `findGalleryImageIds`, `replaceGallery`, `contains`, `dataOf`.

Casos declarados: 0.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageRules]], [[ImageService]], [[InvalidImageException]].

Referenciado por: [[PostServiceImplTest]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java>), líneas 1–73.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.models.ImageRules;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/*
 * Guarda las imagenes y las galerias en memoria para que los tests comprueben cuales quedan
 * despues de publicar, eliminar o cambiar una foto, en lugar de verificar que se llamo a un
 * metodo. Aplica las mismas ImageRules que ImageServiceImpl y numera desde firstId.
 */
final class InMemoryImageService implements ImageService {

    private final Map<Long, Image> images = new HashMap<>();
    private final Map<Long, List<Long>> galleries = new HashMap<>();
    private long nextId;

    InMemoryImageService(final long firstId) {
        this.nextId = firstId;
    }

    @Override
    public Optional<Image> findPostImage(final long postId, final long imageId) {
        return Optional.empty();
    }

    @Override
    public Optional<Image> findUserAvatar(final long userId, final long imageId) {
        return Optional.empty();
    }

    @Override
    public Optional<Image> findAlbumCover(final long albumId, final long imageId) {
        return Optional.empty();
    }

    @Override
    public Image create(final String contentType, final byte[] data) {
        if (!ImageRules.isValid(ImageRules.normalizeContentType(contentType), data)) {
            throw new InvalidImageException();
        }
        final Image created = new Image(nextId++, contentType, data);
        images.put(created.getId(), created);
        return created;
    }

    @Override
    public boolean delete(final long id) {
        return images.remove(id) != null;
    }

    @Override
    public List<Long> findGalleryImageIds(final long postId) {
        return galleries.getOrDefault(postId, List.of());
    }

    @Override
    public void replaceGallery(final long postId, final List<Long> imageIds) {
        galleries.put(postId, List.copyOf(imageIds));
    }

    boolean contains(final long id) {
        return images.containsKey(id);
    }

    byte[] dataOf(final long id) {
        return images.get(id).getData();
    }
}
```
