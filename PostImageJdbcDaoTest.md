---
title: "PostImageJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/PostImageJdbcDaoTest.java"]
---

# PostImageJdbcDaoTest

Tests de `PostImageJdbcDao` en `persistence`: 4 casos declarados. Cubre: orden de la galería, alta y borrado por post. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `POST_IMAGES_TABLE`, `POST_ID`, `GALLERY_IMAGE_ID`, `UNREFERENCED_IMAGE_ID`, `postImageDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 4.

- `testFindImageIdsByPostIdWhenPostHasExtraImageReturnsOrderedIds`
- `testAddWhenPositionIsAvailableReturnsPersistedImageInOrder`
- `testDeleteByPostIdWhenExtraImageExistsReturnsCountAndClearsGallery`
- `testAddWhenPositionExceedsGalleryLimitReturnsDataIntegrityViolation`

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostImageDao]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/PostImageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostImageJdbcDaoTest.java>), líneas 1–100.

```java
package ar.edu.itba.paw.persistence;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.List;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class PostImageJdbcDaoTest {

    private static final String POST_IMAGES_TABLE = "post_images";
    // La publicacion 5 tiene la imagen 4 en la posicion 1; la imagen 3 no la referencia nadie.
    private static final long POST_ID = 5;
    private static final long GALLERY_IMAGE_ID = 4;
    private static final long UNREFERENCED_IMAGE_ID = 3;

    @Autowired
    private PostImageDao postImageDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindImageIdsByPostIdWhenPostHasExtraImageReturnsOrderedIds() {
        // 1. Arrange
        // La publicacion y su foto adicional vienen de populator.sql.

        // 2. Exercise
        final List<Long> imageIds = postImageDao.findImageIdsByPostId(POST_ID);

        // 3. Assert
        Assertions.assertEquals(List.of(GALLERY_IMAGE_ID), imageIds);
    }

    @Test
    public void testAddWhenPositionIsAvailableReturnsPersistedImageInOrder() {
        // 1. Arrange
        final int position = 2;

        // 2. Exercise
        final long id = postImageDao.add(POST_ID, UNREFERENCED_IMAGE_ID, position);

        // 3. Assert
        Assertions.assertTrue(id > 0);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POST_IMAGES_TABLE,
                "id = " + id + " AND post_id = " + POST_ID + " AND image_id = " + UNREFERENCED_IMAGE_ID
                        + " AND display_order = " + position));
    }

    @Test
    public void testDeleteByPostIdWhenExtraImageExistsReturnsCountAndClearsGallery() {
        // 1. Arrange
        // La publicacion 5 ya tiene una foto adicional en populator.sql.

        // 2. Exercise
        final int deleted = postImageDao.deleteByPostId(POST_ID);

        // 3. Assert
        Assertions.assertEquals(1, deleted);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POST_IMAGES_TABLE,
                "post_id = " + POST_ID));
    }

    @Test
    public void testAddWhenPositionExceedsGalleryLimitReturnsDataIntegrityViolation() {
        // 1. Arrange
        // Solo valen las posiciones 1 a 4: la 0 es la foto principal, en posts.image_id.
        final int position = 5;

        // 2. Exercise
        final Executable add = () -> postImageDao.add(POST_ID, UNREFERENCED_IMAGE_ID, position);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, add);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POST_IMAGES_TABLE,
                "image_id = " + UNREFERENCED_IMAGE_ID));
    }
}
```
