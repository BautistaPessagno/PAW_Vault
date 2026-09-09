---
title: "AlbumJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java"]
---

# AlbumJdbcDaoTest

Runs the real JDBC DAO through a Spring HSQLDB context with transaction rollback. Fixture rows come from test populator.sql. Assertions inspect mapped objects and persisted row counts. This checks the test schema and DAO behavior, not production startup, PostgreSQL concurrency, JSPs or HTTP status.

Production connections: [[Album]], [[AlbumDao]], [[AlbumSummary]].

## Test cases

- `testFindFeaturedWhenAlbumsExistReturnsMappedAlbumSummary`
- `testFindOrCreateWhenAlbumExistsReturnsStoredAlbumWithoutModifyingCover`
- `testFindOrCreateWhenReleaseYearDiffersReturnsPersistedAlbum`

## Exact test source

[persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java, lines 1–117](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.AlbumSummary;
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
import java.util.List;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class AlbumJdbcDaoTest {

    private static final long ALBUM_ID = 1;
    private static final long ARTIST_ID = 1;
    private static final String ALBUM_TITLE = "versus";
    private static final String ALBUM_ARTIST_NAME = "illya kuryaki and the valderramas";
    private static final int ALBUM_RELEASE_YEAR = 1997;
    private static final String ALBUM_COVER_PATH = "/images/covers/versus.png";
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
    public void testFindFeaturedWhenAlbumsExistReturnsMappedAlbumSummary() {
        // 1. Arrange
        // No inserts — using data from populator.sql
        final int limit = 8;

        // 2. Exercise
        final List<AlbumSummary> result = albumDao.findFeatured(limit);

        // 3. Assert
        Assertions.assertEquals(1, result.size());
        final AlbumSummary album = result.get(0);
        Assertions.assertEquals(ALBUM_ID, album.getId());
        Assertions.assertEquals(ALBUM_TITLE, album.getTitle());
        Assertions.assertEquals(ALBUM_ARTIST_NAME, album.getArtistName());
        Assertions.assertEquals(ALBUM_RELEASE_YEAR, album.getReleaseYear());
        Assertions.assertEquals(ALBUM_COVER_PATH, album.getCoverPath());
    }

    @Test
    public void testFindOrCreateWhenAlbumExistsReturnsStoredAlbumWithoutModifyingCover() {
        // 1. Arrange
        final String replacementCoverPath = "/images/covers/replacement.png";

        // 2. Exercise
        final Album result = albumDao.findOrCreate(ALBUM_TITLE, ARTIST_ID, ALBUM_RELEASE_YEAR,
                replacementCoverPath);

        // 3. Assert
        Assertions.assertEquals(ALBUM_ID, result.getId());
        Assertions.assertEquals(ALBUM_TITLE, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(ALBUM_RELEASE_YEAR, result.getReleaseYear());
        Assertions.assertEquals(ALBUM_COVER_PATH, result.getCoverPath());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + ALBUM_ID +
                        " AND title = " + sqlString(ALBUM_TITLE) +
                        " AND artist_id = " + ARTIST_ID +
                        " AND release_year = " + ALBUM_RELEASE_YEAR +
                        " AND cover_path = " + sqlString(ALBUM_COVER_PATH)));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenReleaseYearDiffersReturnsPersistedAlbum() {
        // 1. Arrange
        final int releaseYear = 1998;
        final String coverPath = "/images/covers/new-versus.png";

        // 2. Exercise
        final Album result = albumDao.findOrCreate(ALBUM_TITLE, ARTIST_ID, releaseYear, coverPath);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(ALBUM_TITLE, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(releaseYear, result.getReleaseYear());
        Assertions.assertEquals(coverPath, result.getCoverPath());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ALBUMS_TABLE,
                "id = " + result.getId() +
                        " AND title = " + sqlString(ALBUM_TITLE) +
                        " AND artist_id = " + ARTIST_ID +
                        " AND release_year = " + releaseYear +
                        " AND cover_path = " + sqlString(coverPath)));
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
