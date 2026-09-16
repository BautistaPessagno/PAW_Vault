---
title: "AlbumJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java"]
---

# AlbumJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[AlbumJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindByArtistTitleYearWhenAlbumExistsReturnsAlbum`
- `testFindByArtistTitleYearWhenAlbumDoesNotExistReturnsEmpty`
- `testCreateWhenAlbumAlreadyExistsReturnsDuplicateKeyExceptionWithoutChanges`
- `testCreateWhenReleaseYearDiffersReturnsPersistedAlbum`
- `testCreateWhenGenreIsNullReturnsAlbumWithoutGenreOrCover`

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[Genre]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java, lines 1–139](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java>)

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
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenReleaseYearDiffersReturnsPersistedAlbum() {
        // 1. Arrange
        final int releaseYear = 1998;

        // 2. Exercise
        final Album result = albumDao.create(ALBUM_TITLE, ARTIST_ID, releaseYear, ALBUM_GENRE);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(ALBUM_TITLE, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(releaseYear, result.getReleaseYear());
        Assertions.assertEquals(ALBUM_GENRE, result.getGenre());
        Assertions.assertNull(result.getCoverImageId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + result.getId() +
                        " AND title = " + sqlString(ALBUM_TITLE) +
                        " AND artist_id = " + ARTIST_ID +
                        " AND release_year = " + releaseYear +
                        " AND genre = " + sqlString(ALBUM_GENRE.name()) +
                        " AND cover_image_id IS NULL"));
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenGenreIsNullReturnsAlbumWithoutGenreOrCover() {
        // 1. Arrange
        final int releaseYear = 1999;

        // 2. Exercise
        final Album result = albumDao.create(ALBUM_TITLE, ARTIST_ID, releaseYear, null);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertNull(result.getGenre());
        Assertions.assertNull(result.getCoverImageId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + result.getId() + " AND genre IS NULL AND cover_image_id IS NULL"));
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
