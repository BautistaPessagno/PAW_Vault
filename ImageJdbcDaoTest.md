---
title: "ImageJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java"]
---

# ImageJdbcDaoTest

Tests de `ImageJdbcDao` en `persistence`: 27 casos declarados. Cubre: lectura por pertenencia a post, usuario y álbum, y borrado condicional. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `IMAGE_ID`, `IMAGE_CONTENT_TYPE`, `IMAGE_DATA`, `MISSING_IMAGE_ID`, `IMAGES_TABLE`, `POSTS_TABLE`, `imageDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 27.

- `testFindByIdWhenImageExistsReturnsImage`
- `testFindByIdWhenImageDoesNotExistReturnsEmpty`
- `testFindPostImageWhenPostUsesAlbumCoverReturnsImage`
- `testFindPostImageWhenPostHasOwnCoverReturnsImage`
- `testFindPostImageWhenImageIsInGalleryReturnsImage`
- `testFindPostImageWhenPostHasOwnCoverReturnsAlbumCoverForEditing`
- `testFindPostImageWhenImageBelongsToAnotherPostReturnsEmpty`
- `testFindPostImageWhenPostDoesNotExistReturnsEmpty`
- `testFindPostImageWhenImageDoesNotExistReturnsEmpty`
- `testFindUserAvatarWhenVerifiedUserHasAvatarReturnsImage`
- `testFindUserAvatarWhenUserIsUnverifiedReturnsEmpty`
- `testFindUserAvatarWhenImageBelongsToAnotherUserReturnsEmpty`
- `testFindUserAvatarWhenUserDoesNotExistReturnsEmpty`
- `testFindUserAvatarWhenImageIsNotTheCurrentAvatarReturnsOnlyCurrentImage`
- `testFindAlbumCoverWhenAlbumHasCoverReturnsImage`
- `testFindAlbumCoverWhenImageBelongsToAnotherAlbumReturnsEmpty`
- `testFindAlbumCoverWhenImageIsOnlyAPostPhotoReturnsEmpty`
- `testFindAlbumCoverWhenAlbumDoesNotExistReturnsEmpty`
- `testFindAlbumCoverWhenImageDoesNotExistReturnsEmpty`
- `testDeleteWhenOnlyAUserAvatarReferencesImageReturnsFalseAndPreservesAvatar`
- `testFindPostImageWhenImageIsNotReferencedByAnyPostReturnsEmpty`
- `testCreateWhenDataIsValidReturnsPersistedImage`
- `testDeleteWhenImageExistsReturnsTrueAndRemovesRow`
- `testDeleteWhenAlbumReferencesImageReturnsFalseAndPreservesImage`
- `testDeleteWhenPostReferencesImageReturnsFalseAndPreservesImage`
- `testDeleteWhenPostGalleryReferencesImageReturnsFalseAndPreservesImage`
- `testDeleteWhenImageDoesNotExistReturnsFalse`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageDao]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java>), líneas 1–402.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.Optional;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class ImageJdbcDaoTest {

    private static final long IMAGE_ID = 1;
    private static final String IMAGE_CONTENT_TYPE = "image/png";
    private static final byte[] IMAGE_DATA = {
            (byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A
    };
    private static final long MISSING_IMAGE_ID = 999;
    private static final String IMAGES_TABLE = "images";
    private static final String POSTS_TABLE = "posts";

    @Autowired
    private ImageDao imageDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByIdWhenImageExistsReturnsImage() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final Optional<Image> result = imageDao.findById(IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(IMAGE_ID, result.get().getId());
        Assertions.assertEquals(IMAGE_CONTENT_TYPE, result.get().getContentType());
        Assertions.assertArrayEquals(IMAGE_DATA, result.get().getData());
    }

    @Test
    public void testFindByIdWhenImageDoesNotExistReturnsEmpty() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final Optional<Image> result = imageDao.findById(MISSING_IMAGE_ID);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testFindPostImageWhenPostUsesAlbumCoverReturnsImage() {
        // 1. Arrange
        final long postId = 1;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, IMAGE_ID);

        // 3. Assert
        Assertions.assertEquals(IMAGE_ID, result.orElseThrow().getId());
        Assertions.assertEquals(IMAGE_CONTENT_TYPE, result.get().getContentType());
        Assertions.assertArrayEquals(IMAGE_DATA, result.get().getData());
    }

    @Test
    public void testFindPostImageWhenPostHasOwnCoverReturnsImage() {
        // 1. Arrange
        final long postId = 5;
        final long imageId = 2;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, imageId);

        // 3. Assert
        Assertions.assertEquals(imageId, result.orElseThrow().getId());
    }

    @Test
    public void testFindPostImageWhenImageIsInGalleryReturnsImage() {
        // 1. Arrange
        final long postId = 5;
        final long imageId = 4;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, imageId);

        // 3. Assert
        Assertions.assertEquals(imageId, result.orElseThrow().getId());
    }

    @Test
    public void testFindPostImageWhenPostHasOwnCoverReturnsAlbumCoverForEditing() {
        // 1. Arrange
        final long postId = 6;
        final long ownImageId = 5;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, IMAGE_ID);

        // 3. Assert
        Assertions.assertEquals(IMAGE_ID, result.orElseThrow().getId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + postId + " AND image_id = " + ownImageId));
    }

    @Test
    public void testFindPostImageWhenImageBelongsToAnotherPostReturnsEmpty() {
        // 1. Arrange
        final long postId = 1;
        final long anotherPostsImageId = 4;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, anotherPostsImageId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindPostImageWhenPostDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingPostId = 999;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(missingPostId, IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindPostImageWhenImageDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long postId = 1;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, MISSING_IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindUserAvatarWhenVerifiedUserHasAvatarReturnsImage() {
        // 1. Arrange
        final long userId = 2;
        final long imageId = 2;

        // 2. Exercise
        final Optional<Image> result = imageDao.findUserAvatar(userId, imageId);

        // 3. Assert
        Assertions.assertEquals(imageId, result.orElseThrow().getId());
    }

    @Test
    public void testFindUserAvatarWhenUserIsUnverifiedReturnsEmpty() {
        // 1. Arrange
        final long userId = 7;

        // 2. Exercise
        final Optional<Image> result = imageDao.findUserAvatar(userId, IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindUserAvatarWhenImageBelongsToAnotherUserReturnsEmpty() {
        // 1. Arrange
        final long userId = 1;
        final long anotherUsersImageId = 2;

        // 2. Exercise
        final Optional<Image> result = imageDao.findUserAvatar(userId, anotherUsersImageId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindUserAvatarWhenUserDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingUserId = 999;

        // 2. Exercise
        final Optional<Image> result = imageDao.findUserAvatar(missingUserId, IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindUserAvatarWhenImageIsNotTheCurrentAvatarReturnsOnlyCurrentImage() {
        // 1. Arrange
        final long userId = 2;
        final long currentImageId = 2;

        // 2. Exercise
        final Optional<Image> notCurrent = imageDao.findUserAvatar(userId, IMAGE_ID);
        final Optional<Image> current = imageDao.findUserAvatar(userId, currentImageId);

        // 3. Assert
        Assertions.assertTrue(notCurrent.isEmpty());
        Assertions.assertEquals(currentImageId, current.orElseThrow().getId());
    }

    @Test
    public void testFindAlbumCoverWhenAlbumHasCoverReturnsImage() {
        // 1. Arrange
        final long albumId = 1;

        // 2. Exercise
        final Optional<Image> result = imageDao.findAlbumCover(albumId, IMAGE_ID);

        // 3. Assert
        Assertions.assertEquals(IMAGE_ID, result.orElseThrow().getId());
    }

    @Test
    public void testFindAlbumCoverWhenImageBelongsToAnotherAlbumReturnsEmpty() {
        // 1. Arrange
        final long albumId = 2;

        // 2. Exercise
        final Optional<Image> result = imageDao.findAlbumCover(albumId, IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindAlbumCoverWhenImageIsOnlyAPostPhotoReturnsEmpty() {
        // 1. Arrange
        final long albumId = 3;
        final long imageId = 2;

        // 2. Exercise
        final Optional<Image> result = imageDao.findAlbumCover(albumId, imageId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindAlbumCoverWhenAlbumDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingAlbumId = 999;

        // 2. Exercise
        final Optional<Image> result = imageDao.findAlbumCover(missingAlbumId, IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindAlbumCoverWhenImageDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long albumId = 1;

        // 2. Exercise
        final Optional<Image> result = imageDao.findAlbumCover(albumId, MISSING_IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testDeleteWhenOnlyAUserAvatarReferencesImageReturnsFalseAndPreservesAvatar() {
        // 1. Arrange
        final long userId = 6;
        final long imageId = 6;

        // 2. Exercise
        final boolean result = imageDao.delete(imageId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(imageId, imageDao.findUserAvatar(userId, imageId).orElseThrow().getId());
    }

    @Test
    public void testFindPostImageWhenImageIsNotReferencedByAnyPostReturnsEmpty() {
        // 1. Arrange
        final long postId = 5;
        final long unreferencedImageId = 3;

        // 2. Exercise
        final Optional<Image> result = imageDao.findPostImage(postId, unreferencedImageId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
        Assertions.assertTrue(imageDao.findById(unreferencedImageId).isPresent());
    }

    @Test
    public void testCreateWhenDataIsValidReturnsPersistedImage() {
        // 1. Arrange
        final String contentType = "image/jpeg";
        final byte[] data = {(byte) 0xFF, (byte) 0xD8, (byte) 0xFF, (byte) 0xE0};

        // 2. Exercise
        final Image result = imageDao.create(contentType, data);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(contentType, result.getContentType());
        Assertions.assertArrayEquals(data, result.getData());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, IMAGES_TABLE,
                "id = " + result.getId() + " AND content_type = '" + contentType + "'"));
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, IMAGES_TABLE));
    }

    @Test
    public void testDeleteWhenImageExistsReturnsTrueAndRemovesRow() {
        // 1. Arrange
        final long unreferencedImageId = 3;

        // 2. Exercise
        final boolean result = imageDao.delete(unreferencedImageId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, IMAGES_TABLE,
                "id = " + unreferencedImageId));
    }

    @Test
    public void testDeleteWhenAlbumReferencesImageReturnsFalseAndPreservesImage() {
        // 1. Arrange
        final long referencedImageId = IMAGE_ID;

        // 2. Exercise
        final boolean result = imageDao.delete(referencedImageId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertTrue(imageDao.findById(referencedImageId).isPresent());
    }

    @Test
    public void testDeleteWhenPostReferencesImageReturnsFalseAndPreservesImage() {
        // 1. Arrange
        final long referencedImageId = 2;

        // 2. Exercise
        final boolean result = imageDao.delete(referencedImageId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertTrue(imageDao.findById(referencedImageId).isPresent());
    }

    @Test
    public void testDeleteWhenPostGalleryReferencesImageReturnsFalseAndPreservesImage() {
        // 1. Arrange
        final long referencedImageId = 4;

        // 2. Exercise
        final boolean result = imageDao.delete(referencedImageId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertTrue(imageDao.findById(referencedImageId).isPresent());
    }

    @Test
    public void testDeleteWhenImageDoesNotExistReturnsFalse() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final boolean result = imageDao.delete(MISSING_IMAGE_ID);

        // 3. Assert
        Assertions.assertFalse(result);
    }
}
```
