---
title: "AlbumJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java"]
---

# AlbumJdbcDaoTest

Tests de `AlbumJdbcDao` en `persistence`: 10 casos declarados. Cubre: identidad sin distinguir mayúsculas, alta y actualización de metadatos. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `ALBUM_ID`, `ARTIST_ID`, `ALBUM_TITLE`, `ALBUM_RELEASE_YEAR`, `ALBUM_GENRE`, `ALBUM_COVER_IMAGE_ID`, `ALBUMS_TABLE`, `albumDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `sqlString`.

Casos declarados: 10.

- `testFindByArtistTitleYearWhenAlbumExistsReturnsAlbum`
- `testFindByArtistTitleYearWhenTitleDiffersOnlyInCaseReturnsAlbum`
- `testFindByArtistTitleYearWhenAlbumDoesNotExistReturnsEmpty`
- `testCreateWhenAlbumAlreadyExistsReturnsDuplicateKeyExceptionWithoutChanges`
- `testCreateWhenTitleDiffersOnlyInCaseReturnsDuplicateKeyExceptionWithoutChanges`
- `testCreateWhenReleaseYearDiffersReturnsPersistedAlbum`
- `testCreateWhenGenreIsNullThrowsDataIntegrityViolationWithoutPersistingAlbum`
- `testCreateWhenGenreIsUnknownThrowsDataIntegrityViolationWithoutPersistingAlbum`
- `testUpdateMetadataWhenAlbumExistsReturnsPersistedAlbum`
- `testUpdateMetadataWhenAlbumDoesNotExistThrowsIllegalStateException`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[AlbumDao]], [[Genre]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java>), líneas 1–212.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.DuplicateKeyException;
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
public class AlbumJdbcDaoTest {

    private static final long ALBUM_ID = 1;
    private static final long ARTIST_ID = 1;
    private static final String ALBUM_TITLE = "versus";
    private static final int ALBUM_RELEASE_YEAR = 1997;
    private static final Genre ALBUM_GENRE = Genre.HIP_HOP;
    private static final long ALBUM_COVER_IMAGE_ID = 1;
    private static final String ALBUMS_TABLE = "albums";

    @Autowired
    private AlbumDao albumDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByArtistTitleYearWhenAlbumExistsReturnsAlbum() {
        // 1. Arrange
        // No inserts — using data from populator.sql

        // 2. Exercise
        final Optional<Album> result = albumDao.findByArtistTitleYear(ALBUM_TITLE, ARTIST_ID, ALBUM_RELEASE_YEAR);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(ALBUM_ID, result.get().getId());
        Assertions.assertEquals(ALBUM_GENRE, result.get().getGenre());
        Assertions.assertEquals(ALBUM_COVER_IMAGE_ID, result.get().getCoverImageId());
    }

    @Test
    public void testFindByArtistTitleYearWhenTitleDiffersOnlyInCaseReturnsAlbum() {
        // 1. Arrange

        // 2. Exercise
        final Optional<Album> result = albumDao.findByArtistTitleYear("VERSUS", ARTIST_ID, ALBUM_RELEASE_YEAR);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(ALBUM_ID, result.get().getId());
        Assertions.assertEquals(ALBUM_TITLE, result.get().getTitle());
    }

    @Test
    public void testFindByArtistTitleYearWhenAlbumDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final int otherReleaseYear = 2001;

        // 2. Exercise
        final Optional<Album> result = albumDao.findByArtistTitleYear(ALBUM_TITLE, ARTIST_ID, otherReleaseYear);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testCreateWhenAlbumAlreadyExistsReturnsDuplicateKeyExceptionWithoutChanges() {
        // 1. Arrange

        // 2. Exercise
        final Executable create = () -> albumDao.create(ALBUM_TITLE, ARTIST_ID, ALBUM_RELEASE_YEAR,
                ALBUM_GENRE);

        // 3. Assert
        Assertions.assertThrows(DuplicateKeyException.class, create);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + ALBUM_ID +
                        " AND title = " + sqlString(ALBUM_TITLE) +
                        " AND artist_id = " + ARTIST_ID +
                        " AND release_year = " + ALBUM_RELEASE_YEAR +
                        " AND cover_image_id = " + ALBUM_COVER_IMAGE_ID));
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenTitleDiffersOnlyInCaseReturnsDuplicateKeyExceptionWithoutChanges() {
        // 1. Arrange
        final String title = "VERSUS";

        // 2. Exercise
        final Executable create = () -> albumDao.create(title, ARTIST_ID, ALBUM_RELEASE_YEAR, ALBUM_GENRE);

        // 3. Assert
        Assertions.assertThrows(DuplicateKeyException.class, create);
        Assertions.assertEquals(ALBUM_TITLE,
                albumDao.findByArtistTitleYear(title, ARTIST_ID, ALBUM_RELEASE_YEAR).orElseThrow().getTitle());
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenReleaseYearDiffersReturnsPersistedAlbum() {
        // 1. Arrange
        final String title = "Versus";
        final int releaseYear = 1998;

        // 2. Exercise
        final Album result = albumDao.create(title, ARTIST_ID, releaseYear, ALBUM_GENRE);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(title, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(releaseYear, result.getReleaseYear());
        Assertions.assertEquals(ALBUM_GENRE, result.getGenre());
        Assertions.assertNull(result.getCoverImageId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + result.getId() +
                        " AND title = " + sqlString(title) +
                        " AND artist_id = " + ARTIST_ID +
                        " AND release_year = " + releaseYear +
                        " AND genre = " + sqlString(ALBUM_GENRE.name()) +
                        " AND cover_image_id IS NULL"));
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenGenreIsNullThrowsDataIntegrityViolationWithoutPersistingAlbum() {
        // 1. Arrange
        final int releaseYear = 1999;

        // 2. Exercise
        final Executable create = () -> albumDao.create(ALBUM_TITLE, ARTIST_ID, releaseYear, null);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, create);
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenGenreIsUnknownThrowsDataIntegrityViolationWithoutPersistingAlbum() {
        // 1. Arrange
        final int releaseYear = 1999;

        // 2. Exercise
        // El enum Genre impide que el DAO mande un valor desconocido: el INSERT directo prueba que
        // el CHECK de la migracion lo rechaza igual si alguien escribe por fuera de la app.
        final Executable create = () -> jdbcTemplate.update(
                "INSERT INTO albums (title, normalized_title, artist_id, release_year, genre, search_phrase) "
                        + "VALUES (?, ?, ?, ?, ?, ?)",
                ALBUM_TITLE, ALBUM_TITLE, ARTIST_ID, releaseYear, "UNKNOWN", ALBUM_TITLE);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, create);
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testUpdateMetadataWhenAlbumExistsReturnsPersistedAlbum() {
        // 1. Arrange
        final String updatedTitle = "Versus";
        final Genre updatedGenre = Genre.SOUL_FUNK;

        // 2. Exercise
        final Album result = albumDao.updateMetadata(ALBUM_ID, updatedTitle, updatedGenre);

        // 3. Assert
        Assertions.assertEquals(ALBUM_ID, result.getId());
        Assertions.assertEquals(updatedTitle, result.getTitle());
        Assertions.assertEquals(updatedGenre, result.getGenre());
        Assertions.assertEquals(ALBUM_COVER_IMAGE_ID, result.getCoverImageId());
    }

    @Test
    public void testUpdateMetadataWhenAlbumDoesNotExistThrowsIllegalStateException() {
        // 1. Arrange
        final long missingAlbumId = 999;

        // 2. Exercise
        final Executable update = () -> albumDao.updateMetadata(missingAlbumId, "Missing", Genre.ROCK);

        // 3. Assert
        Assertions.assertThrows(IllegalStateException.class, update);
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```
