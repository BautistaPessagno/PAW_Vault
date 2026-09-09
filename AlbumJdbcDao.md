---
title: "AlbumJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java"]
---

# AlbumJdbcDao

Queries exact artist/title/year identity and inserts an Album with nullable cover_image_id. readCoverImageId checks ResultSet.wasNull after getLong to preserve SQL NULL instead of turning it into 0. [[PostJdbcDao]] reuses this package-visible mapper helper. There is no album-listing query anymore. Database uniqueness remains the final duplicate guard.

## Connections

Project types referenced: [[Album]], [[AlbumDao]].

Referenced by: [[PostJdbcDao]].

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java, lines 1–69](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@Repository
public class AlbumJdbcDao implements AlbumDao {

    private static final RowMapper<Album> ROW_MAPPER = (resultSet, rowNum) -> new Album(
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getLong("album_artist_id"),
            resultSet.getInt("album_release_year"),
            readCoverImageId(resultSet)
    );

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // cover_image_id es nullable: getLong devuelve 0 para NULL, asi que hay que consultar wasNull.
    static Long readCoverImageId(final ResultSet resultSet) throws SQLException {
        final long coverImageId = resultSet.getLong("album_cover_image_id");
        return resultSet.wasNull() ? null : coverImageId;
    }

    @Autowired
    public AlbumJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("albums")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Optional<Album> findByArtistTitleYear(final String title, final long artistId,
                                                 final int releaseYear) {
        return jdbcTemplate.query(
                        "SELECT id AS album_id, title AS album_title, artist_id AS album_artist_id, " +
                                "release_year AS album_release_year, cover_image_id AS album_cover_image_id " +
                                "FROM albums WHERE artist_id = ? AND title = ? AND release_year = ?",
                        ROW_MAPPER, artistId, title, releaseYear)
                .stream()
                .findAny();
    }

    @Override
    public Album create(final String title, final long artistId, final int releaseYear, final Long coverImageId) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("title", title);
        parameters.put("artist_id", artistId);
        parameters.put("release_year", releaseYear);
        parameters.put("cover_image_id", coverImageId);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Album(id.longValue(), title, artistId, releaseYear, coverImageId);
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
