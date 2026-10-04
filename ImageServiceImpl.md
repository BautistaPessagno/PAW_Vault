---
title: "ImageServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java"]
---

# ImageServiceImpl

Valida tipo, tamaño y firma antes de guardar; lee por pertenencia; borra solo lo no referenciado; reemplaza la galería completa. Ver [[Cover image flow]] y [[Gallery flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `imageDao`, `postImageDao`.

Operaciones para localizar en la fuente: `findPostImage`, `findUserAvatar`, `findAlbumCover`, `create`, `delete`, `findGalleryImageIds`, `replaceGallery`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageDao]], [[ImageRules]], [[ImageService]], [[InvalidImageException]], [[PostImageDao]].

Referenciado por: [[ImageServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>), líneas 1–82.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.persistence.ImageDao;
import ar.edu.itba.paw.persistence.PostImageDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private static final Logger LOGGER = LoggerFactory.getLogger(ImageServiceImpl.class);

    private final ImageDao imageDao;
    private final PostImageDao postImageDao;

    @Autowired
    public ImageServiceImpl(final ImageDao imageDao, final PostImageDao postImageDao) {
        this.imageDao = imageDao;
        this.postImageDao = postImageDao;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Image> findPostImage(final long postId, final long imageId) {
        return imageDao.findPostImage(postId, imageId);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Image> findUserAvatar(final long userId, final long imageId) {
        return imageDao.findUserAvatar(userId, imageId);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Image> findAlbumCover(final long albumId, final long imageId) {
        return imageDao.findAlbumCover(albumId, imageId);
    }

    @Override
    @Transactional
    public Image create(final String contentType, final byte[] data) {
        final String normalizedType = ImageRules.normalizeContentType(contentType);
        if (!ImageRules.isValid(normalizedType, data)) {
            LOGGER.warn("Rejected image contentType={} bytes={}", normalizedType, data == null ? 0 : data.length);
            throw new InvalidImageException();
        }
        final Image image = imageDao.create(normalizedType, data);
        LOGGER.info("Stored image {} ({}, {} bytes)", image.getId(), image.getContentType(), data.length);
        return image;
    }

    @Override
    @Transactional
    public boolean delete(final long id) {
        return imageDao.delete(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Long> findGalleryImageIds(final long postId) {
        return postImageDao.findImageIdsByPostId(postId);
    }

    // La posicion 0 es la foto principal del post: las adicionales arrancan en 1.
    @Override
    @Transactional
    public void replaceGallery(final long postId, final List<Long> imageIds) {
        postImageDao.deleteByPostId(postId);
        for (int index = 0; index < imageIds.size(); index++) {
            postImageDao.add(postId, imageIds.get(index), index + 1);
        }
    }
}
```
