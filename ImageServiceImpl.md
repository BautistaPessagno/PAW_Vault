---
title: "ImageServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java"]
---

# ImageServiceImpl

findById is read-only transactional. create normalizes the declared MIME type and accepts image/png, image/jpeg or image/webp with 1 through 5 * 1024 * 1024 bytes. Invalid inputs raise [[InvalidImageException]]. It does not decode image data or inspect signatures, so an accepted MIME label is not proof of valid image content. The transactional insert delegates to [[ImageDao]]. Logs report IDs, MIME type and byte length.

## Connections

Project types referenced: [[Image]], [[ImageDao]], [[ImageService]], [[InvalidImageException]].

Referenced by: [[ImageServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java, lines 1–56](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.persistence.ImageDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Locale;
import java.util.Optional;
import java.util.Set;

@Service
public class ImageServiceImpl implements ImageService {

    private static final Logger LOGGER = LoggerFactory.getLogger(ImageServiceImpl.class);

    private static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;
    private static final Set<String> ALLOWED_CONTENT_TYPES = Collections.unmodifiableSet(
            new HashSet<>(Arrays.asList("image/png", "image/jpeg", "image/webp")));

    private final ImageDao imageDao;

    @Autowired
    public ImageServiceImpl(final ImageDao imageDao) {
        this.imageDao = imageDao;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Image> findById(final long id) {
        return imageDao.findById(id);
    }

    @Override
    @Transactional
    public Image create(final String contentType, final byte[] data) {
        final String normalizedType = contentType == null ? null : contentType.trim().toLowerCase(Locale.ROOT);
        if (normalizedType == null || !ALLOWED_CONTENT_TYPES.contains(normalizedType)) {
            LOGGER.info("Rejected image with content type {}", contentType);
            throw new InvalidImageException();
        }
        if (data == null || data.length == 0 || data.length > MAX_IMAGE_BYTES) {
            LOGGER.info("Rejected image of {} bytes", data == null ? 0 : data.length);
            throw new InvalidImageException();
        }
        final Image image = imageDao.create(normalizedType, data);
        LOGGER.info("Stored image {} ({}, {} bytes)", image.getId(), image.getContentType(), data.length);
        return image;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
