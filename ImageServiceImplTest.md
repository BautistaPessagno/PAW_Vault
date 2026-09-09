---
title: "ImageServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java"]
---

# ImageServiceImplTest

Four Mockito tests cover unsupported MIME type, empty bytes, bytes above 5 MiB and valid PNG-labeled data. Does not cover the exact upper boundary, MIME normalization, null MIME/data, JPEG/WebP success or byte-signature validation. Direct service instances do not activate transactions.

## Test methods

- `testCreateWhenContentTypeIsNotAnImageReturnsInvalidImageException`
- `testCreateWhenDataIsEmptyReturnsInvalidImageException`
- `testCreateWhenDataExceedsMaxSizeReturnsInvalidImageException`
- `testCreateWhenImageIsValidReturnsPersistedImage`

These are source assertions, not a fresh passing test run.

## Connections

Project types referenced: [[Image]], [[ImageDao]], [[ImageServiceImpl]], [[InvalidImageException]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java, lines 1–77](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.persistence.ImageDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class ImageServiceImplTest {

    private static final String PNG_CONTENT_TYPE = "image/png";
    private static final byte[] PNG_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47};
    private static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;

    @Mock
    private ImageDao imageDao;

    @InjectMocks
    private ImageServiceImpl imageService;

    @Test
    public void testCreateWhenContentTypeIsNotAnImageReturnsInvalidImageException() {
        // 1. Arrange
        final String contentType = "text/html";

        // 2. Exercise
        final Executable create = () -> imageService.create(contentType, PNG_DATA);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, create);
    }

    @Test
    public void testCreateWhenDataIsEmptyReturnsInvalidImageException() {
        // 1. Arrange
        final byte[] emptyData = {};

        // 2. Exercise
        final Executable create = () -> imageService.create(PNG_CONTENT_TYPE, emptyData);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, create);
    }

    @Test
    public void testCreateWhenDataExceedsMaxSizeReturnsInvalidImageException() {
        // 1. Arrange
        final byte[] oversizedData = new byte[MAX_IMAGE_BYTES + 1];

        // 2. Exercise
        final Executable create = () -> imageService.create(PNG_CONTENT_TYPE, oversizedData);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, create);
    }

    @Test
    public void testCreateWhenImageIsValidReturnsPersistedImage() {
        // 1. Arrange
        final Image expected = new Image(7, PNG_CONTENT_TYPE, PNG_DATA);
        Mockito.when(imageDao.create(PNG_CONTENT_TYPE, PNG_DATA)).thenReturn(expected);

        // 2. Exercise
        final Image result = imageService.create(PNG_CONTENT_TYPE, PNG_DATA);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(PNG_CONTENT_TYPE, result.getContentType());
        Assertions.assertArrayEquals(PNG_DATA, result.getData());
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
