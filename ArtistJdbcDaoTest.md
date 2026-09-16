---
title: "ArtistJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java"]
---

# ArtistJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[ArtistJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindOrCreateWhenArtistExistsReturnsExistingArtist`
- `testFindOrCreateWhenArtistIsNewReturnsPersistedArtist`
- `testFindAllWhenArtistsExistReturnsThemAlphabetically`

## Connections

Project types referenced: [[Artist]], [[ArtistDao]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java, lines 1–87](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;
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
public class ArtistJdbcDaoTest {

    private static final String ARTISTS_TABLE = "artists";
    private static final long ARTIST_ID = 1;
    private static final String ARTIST_NAME = "illya kuryaki and the valderramas";

    @Autowired
    private ArtistDao artistDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindOrCreateWhenArtistExistsReturnsExistingArtist() {
        // 1. Arrange

        // 2. Exercise
        final Artist result = artistDao.findOrCreate(ARTIST_NAME);

        // 3. Assert
        Assertions.assertEquals(ARTIST_ID, result.getId());
        Assertions.assertEquals(ARTIST_NAME, result.getName());
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenArtistIsNewReturnsPersistedArtist() {
        // 1. Arrange
        final String name = "charly garcía";

        // 2. Exercise
        final Artist result = artistDao.findOrCreate(name);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(name, result.getName());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ARTISTS_TABLE,
                "id = " + result.getId() + " AND name = " + sqlString(name)));
    }

    @Test
    public void testFindAllWhenArtistsExistReturnsThemAlphabetically() {
        // 1. Arrange
        final String lastArtistName = "soda stereo";

        // 2. Exercise
        final List<Artist> result = artistDao.findAll();

        // 3. Assert
        Assertions.assertEquals(2, result.size());
        Assertions.assertEquals(ARTIST_NAME, result.get(0).getName());
        Assertions.assertEquals(lastArtistName, result.get(1).getName());
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
