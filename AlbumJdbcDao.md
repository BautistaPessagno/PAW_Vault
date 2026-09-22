---
title: "AlbumJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java"]
---

# AlbumJdbcDao

A shared SELECT_ALBUM alias list feeds the static RowMapper. findByArtistTitleYear compares LOWER(title) = LOWER(?) with artist and year; create stores the title as given, the required genre and a search_phrase from [[SearchText]]. updateMetadata rewrites title, genre and search_phrase, then rereads the row, throwing IllegalStateException if it disappeared. readGenre now assumes a non-null genre.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[Genre]], [[SearchText]].

Referenced by: [[PostJdbcDao]].

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java, lines 1–93](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.SearchText;
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
            readGenre(resultSet),
            readCoverImageId(resultSet)
    );

    private static final String SELECT_ALBUM =
            "SELECT id AS album_id, title AS album_title, artist_id AS album_artist_id, "
                    + "release_year AS album_release_year, genre AS album_genre, "
                    + "cover_image_id AS album_cover_image_id FROM albums ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // cover_image_id es nullable: getLong devuelve 0 para NULL, asi que hay que consultar wasNull.
    static Long readCoverImageId(final ResultSet resultSet) throws SQLException {
        final long coverImageId = resultSet.getLong("album_cover_image_id");
        return resultSet.wasNull() ? null : coverImageId;
    }

    static Genre readGenre(final ResultSet resultSet) throws SQLException {
        return Genre.valueOf(resultSet.getString("album_genre"));
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
                        SELECT_ALBUM + "WHERE artist_id = ? AND LOWER(title) = LOWER(?) AND release_year = ?",
                        ROW_MAPPER, artistId, title, releaseYear)
                .stream()
                .findAny();
    }

    /*
     * cover_image_id no se escribe: la portada vive en la publicacion. La columna queda
     * como dato heredado que sigue leyendo el COALESCE de PostJdbcDao.
     */
    @Override
    public Album create(final String title, final long artistId, final int releaseYear, final Genre genre) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("title", title);
        parameters.put("artist_id", artistId);
        parameters.put("release_year", releaseYear);
        parameters.put("genre", genre == null ? null : genre.name());
        parameters.put("search_phrase", SearchText.phrase(title));

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Album(id.longValue(), title, artistId, releaseYear, genre, null);
    }

    @Override
    public Album updateMetadata(final long id, final String title, final Genre genre) {
        if (jdbcTemplate.update("UPDATE albums SET title = ?, genre = ?, search_phrase = ? WHERE id = ?",
                title, genre == null ? null : genre.name(), SearchText.phrase(title), id) != 1) {
            throw new IllegalStateException("Album disappeared while updating metadata");
        }
        return jdbcTemplate.queryForObject(SELECT_ALBUM + "WHERE id = ?", ROW_MAPPER, id);
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
