---
title: "ImageServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java"]
---

# ImageServiceImplTest

Tests de `ImageServiceImpl` en `services`: 7 casos declarados. Cubre: validación de tipo, tamaño y firma, y reemplazo de galería. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `PNG_CONTENT_TYPE`, `PNG_DATA`, `MAX_IMAGE_BYTES`, `imageDao`, `postImageDao`, `imageService`, `galleries`, `nextId`.

Operaciones para localizar en la fuente: `findImageIdsByPostId`, `add`, `deleteByPostId`, `positionsOf`.

Casos declarados: 7.

- `testCreateWhenContentTypeIsNotAnImageReturnsInvalidImageException`
- `testCreateWhenDataIsEmptyReturnsInvalidImageException`
- `testCreateWhenDataExceedsMaxSizeReturnsInvalidImageException`
- `testCreateWhenContentDoesNotMatchDeclaredTypeReturnsInvalidImageException`
- `testCreateWhenWebpSignatureMatchesReturnsPersistedImage`
- `testCreateWhenImageIsValidReturnsPersistedImage`
- `testReplaceGalleryWhenPostHadPhotosReturnsOnlyNewOnesFromPositionOne`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageDao]], [[ImageService]], [[ImageServiceImpl]], [[InvalidImageException]], [[PostImageDao]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java>), líneas 1–161.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.persistence.ImageDao;
import ar.edu.itba.paw.persistence.PostImageDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

@ExtendWith(MockitoExtension.class)
public class ImageServiceImplTest {

    private static final String PNG_CONTENT_TYPE = "image/png";
    private static final byte[] PNG_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};
    private static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;

    @Mock
    private ImageDao imageDao;

    @Mock
    private PostImageDao postImageDao;

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
    public void testCreateWhenContentDoesNotMatchDeclaredTypeReturnsInvalidImageException() {
        // 1. Arrange
        final byte[] jpegHeader = {(byte) 0xFF, (byte) 0xD8, (byte) 0xFF};

        // 2. Exercise
        final Executable create = () -> imageService.create(PNG_CONTENT_TYPE, jpegHeader);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, create);
    }

    @Test
    public void testCreateWhenWebpSignatureMatchesReturnsPersistedImage() {
        // 1. Arrange
        final String contentType = "image/webp";
        final byte[] data = {'R', 'I', 'F', 'F', 0, 0, 0, 0, 'W', 'E', 'B', 'P'};
        final Image expected = new Image(8, contentType, data);
        Mockito.when(imageDao.create(contentType, data)).thenReturn(expected);

        // 2. Exercise
        final Image result = imageService.create(contentType, data);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertArrayEquals(data, result.getData());
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

    @Test
    public void testReplaceGalleryWhenPostHadPhotosReturnsOnlyNewOnesFromPositionOne() {
        // 1. Arrange
        final long postId = 5;
        final InMemoryPostImageDao gallery = new InMemoryPostImageDao();
        gallery.add(postId, 4, 1);
        final ImageService service = new ImageServiceImpl(imageDao, gallery);

        // 2. Exercise
        service.replaceGallery(postId, List.of(9L, 8L));

        // 3. Assert
        Assertions.assertEquals(List.of(9L, 8L), service.findGalleryImageIds(postId));
        Assertions.assertEquals(List.of(1, 2), gallery.positionsOf(postId));
    }

    /*
     * Guarda la galeria en memoria para que el test compruebe las posiciones que quedan, en lugar
     * de verificar que se llamo a add. La posicion 0 es la foto principal del post: no va aca.
     */
    private static final class InMemoryPostImageDao implements PostImageDao {
        private final Map<Long, TreeMap<Integer, Long>> galleries = new HashMap<>();
        private long nextId = 1;

        @Override
        public List<Long> findImageIdsByPostId(final long postId) {
            return List.copyOf(galleries.getOrDefault(postId, new TreeMap<>()).values());
        }

        @Override
        public long add(final long postId, final long imageId, final int position) {
            galleries.computeIfAbsent(postId, ignored -> new TreeMap<>()).put(position, imageId);
            return nextId++;
        }

        @Override
        public int deleteByPostId(final long postId) {
            final TreeMap<Integer, Long> removed = galleries.remove(postId);
            return removed == null ? 0 : removed.size();
        }

        private List<Integer> positionsOf(final long postId) {
            return new ArrayList<>(galleries.getOrDefault(postId, new TreeMap<>()).keySet());
        }
    }
}
```
