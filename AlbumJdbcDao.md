---
title: "AlbumJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java"]
---

# AlbumJdbcDao

Two shared RowMappers distinguish [[Album]] from [[AlbumSummary]]. `findByArtistTitleYear` binds artist ID, title and year. `findFeatured` joins artists, sorts year descending then title ascending, applies LIMIT and wraps the list as unmodifiable. `create` inserts title, artist_id, release_year and cover_path using a generated key. `findOrCreate` returns an existing album without updating its cover; a missing identity triggers the lazy insert. Concurrent inserts can still collide with the unique constraint.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumSummary]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java, lines 1–86](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.AlbumSummary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class AlbumJdbcDao implements AlbumDao {

    private static final RowMapper<AlbumSummary> SUMMARY_ROW_MAPPER = (resultSet, rowNum) -> new AlbumSummary(
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getInt("album_release_year"),
            resultSet.getString("album_cover_path")
    );
    private static final RowMapper<Album> ROW_MAPPER = (resultSet, rowNum) -> new Album(
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getLong("album_artist_id"),
            resultSet.getInt("album_release_year"),
            resultSet.getString("album_cover_path")
    );

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public AlbumJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("albums")
                .usingGeneratedKeyColumns("id");
    }

    private Optional<Album> findByArtistTitleYear(final String title, final long artistId,
                                                   final int releaseYear) {
        return jdbcTemplate.query(
                        "SELECT id AS album_id, title AS album_title, artist_id AS album_artist_id, " +
                                "release_year AS album_release_year, cover_path AS album_cover_path " +
                                "FROM albums WHERE artist_id = ? AND title = ? AND release_year = ?",
                        ROW_MAPPER, artistId, title, releaseYear)
                .stream()
                .findAny();
    }

    @Override
    public List<AlbumSummary> findFeatured(final int limit) {
        return Collections.unmodifiableList(jdbcTemplate.query(
                "SELECT a.id AS album_id, a.title AS album_title, ar.name AS artist_name, " +
                        "a.release_year AS album_release_year, a.cover_path AS album_cover_path " +
                        "FROM albums a JOIN artists ar ON ar.id = a.artist_id " +
                        "ORDER BY a.release_year DESC, a.title ASC LIMIT ?",
                SUMMARY_ROW_MAPPER, limit));
    }

    private Album create(final String title, final long artistId, final int releaseYear, final String coverPath) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("title", title);
        parameters.put("artist_id", artistId);
        parameters.put("release_year", releaseYear);
        parameters.put("cover_path", coverPath);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Album(id.longValue(), title, artistId, releaseYear, coverPath);
    }

    @Override
    public Album findOrCreate(final String title, final long artistId, final int releaseYear,
                              final String coverPath) {
        return findByArtistTitleYear(title, artistId, releaseYear)
                .orElseGet(() -> create(title, artistId, releaseYear, coverPath));
    }

}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
