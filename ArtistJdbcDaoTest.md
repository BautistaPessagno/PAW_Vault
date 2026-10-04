---
title: "ArtistJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java"]
---

# ArtistJdbcDaoTest

Tests de `ArtistJdbcDao` en `persistence`: 11 casos declarados. Cubre: buscar o crear por nombre normalizado, nombre visible y sugerencias sin tildes. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `ARTISTS_TABLE`, `ARTIST_ID`, `ARTIST_NAME`, `ARTIST_NORMALIZED_NAME`, `artistDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `sqlString`.

Casos declarados: 11.

- `testFindOrCreateWhenArtistExistsReturnsExistingArtist`
- `testFindOrCreateWhenNameDiffersOnlyInCaseReturnsExistingArtist`
- `testFindOrCreateWhenNameDiffersOnlyInSeparatorsReturnsExistingArtist`
- `testFindOrCreateWhenArtistIsNewReturnsPersistedArtist`
- `testUpdateDisplayNameWhenArtistExistsReturnsPersistedArtist`
- `testUpdateDisplayNameWhenArtistDoesNotExistThrowsIllegalStateException`
- `testFindSuggestionsWhenQueryOmitsAccentReturnsMatch`
- `testFindSuggestionsWhenQueryMatchesWordStartReturnsMatch`
- `testFindSuggestionsWhenSeveralArtistsSharePrefixReturnsAlphabeticalOrder`
- `testFindSuggestionsWhenLimitIsBelowMatchCountReturnsBestRanked`
- `testFindSuggestionsWhenQueryMatchesNothingReturnsEmptyList`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]], [[ArtistDao]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java>), líneas 1–192.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
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
    private static final String ARTIST_NORMALIZED_NAME = "illyakuryakiandthevalderramas";

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
        final Artist result = artistDao.findOrCreate(ARTIST_NAME, ARTIST_NORMALIZED_NAME);

        // 3. Assert
        Assertions.assertEquals(ARTIST_ID, result.getId());
        Assertions.assertEquals(ARTIST_NAME, result.getName());
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenNameDiffersOnlyInCaseReturnsExistingArtist() {
        // 1. Arrange

        // 2. Exercise
        final Artist result = artistDao.findOrCreate(
                "ILLYA KURYAKI AND THE VALDERRAMAS", ARTIST_NORMALIZED_NAME);

        // 3. Assert
        Assertions.assertEquals(ARTIST_ID, result.getId());
        Assertions.assertEquals(ARTIST_NAME, result.getName());
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenNameDiffersOnlyInSeparatorsReturnsExistingArtist() {
        // 1. Arrange
        final String displayName = "Illya-Kuryaki-and-the-Valderramas";

        // 2. Exercise
        final Artist result = artistDao.findOrCreate(displayName, ARTIST_NORMALIZED_NAME);

        // 3. Assert
        Assertions.assertEquals(ARTIST_ID, result.getId());
        Assertions.assertEquals(ARTIST_NAME, result.getName());
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
    }

    @Test
    public void testFindOrCreateWhenArtistIsNewReturnsPersistedArtist() {
        // 1. Arrange
        final String name = "Charly García";
        final String normalizedName = "charlygarcía";

        // 2. Exercise
        final Artist result = artistDao.findOrCreate(name, normalizedName);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(name, result.getName());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, ARTISTS_TABLE,
                "id = " + result.getId() + " AND name = " + sqlString(name)
                        + " AND normalized_name = " + sqlString(normalizedName)));
    }

    @Test
    public void testUpdateDisplayNameWhenArtistExistsReturnsPersistedArtist() {
        // 1. Arrange
        final String updatedName = "Illya Kuryaki and the Valderramas";

        // 2. Exercise
        final Artist result = artistDao.updateDisplayName(ARTIST_ID, updatedName);

        // 3. Assert
        Assertions.assertEquals(ARTIST_ID, result.getId());
        Assertions.assertEquals(updatedName, result.getName());
        Assertions.assertEquals(updatedName, artistDao.findOrCreate(updatedName, ARTIST_NORMALIZED_NAME).getName());
    }

    @Test
    public void testUpdateDisplayNameWhenArtistDoesNotExistThrowsIllegalStateException() {
        // 1. Arrange
        final long missingArtistId = 999;

        // 2. Exercise
        final Executable update = () -> artistDao.updateDisplayName(missingArtistId, "Missing");

        // 3. Assert
        Assertions.assertThrows(IllegalStateException.class, update);
    }

    @Test
    public void testFindSuggestionsWhenQueryOmitsAccentReturnsMatch() {
        // 1. Arrange
        final String query = "cafe";

        // 2. Exercise
        final List<Artist> result = artistDao.findSuggestions(query, 5);

        // 3. Assert
        Assertions.assertEquals(List.of("Café Tacvba"), result.stream().map(Artist::getName).toList());
    }

    @Test
    public void testFindSuggestionsWhenQueryMatchesWordStartReturnsMatch() {
        // 1. Arrange
        final String query = "tacvba";

        // 2. Exercise
        final List<Artist> result = artistDao.findSuggestions(query, 5);

        // 3. Assert
        Assertions.assertEquals(List.of("Café Tacvba"), result.stream().map(Artist::getName).toList());
    }

    @Test
    public void testFindSuggestionsWhenSeveralArtistsSharePrefixReturnsAlphabeticalOrder() {
        // 1. Arrange
        final String query = "so";

        // 2. Exercise
        final List<Artist> result = artistDao.findSuggestions(query, 5);

        // 3. Assert
        Assertions.assertEquals(List.of("soda stereo", "sold only artist"),
                result.stream().map(Artist::getName).toList());
    }

    @Test
    public void testFindSuggestionsWhenLimitIsBelowMatchCountReturnsBestRanked() {
        // 1. Arrange
        final String query = "so";

        // 2. Exercise
        final List<Artist> result = artistDao.findSuggestions(query, 1);

        // 3. Assert
        Assertions.assertEquals(List.of("soda stereo"), result.stream().map(Artist::getName).toList());
    }

    @Test
    public void testFindSuggestionsWhenQueryMatchesNothingReturnsEmptyList() {
        // 1. Arrange
        final String query = "zzz";

        // 2. Exercise
        final List<Artist> result = artistDao.findSuggestions(query, 5);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    private String sqlString(final String value) {
        return "'" + value.replace("'", "''") + "'";
    }
}
```
