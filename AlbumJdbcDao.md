---
title: "AlbumJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java"]
---

# AlbumJdbcDao

Álbumes con Spring JDBC. Busca por artista, `normalized_title` y año; al crear o editar recalcula `normalized_title` y `search_phrase`. No escribe `cover_image_id`: la portada del álbum es un dato heredado.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT_ALBUM`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `readCoverImageId`, `readGenre`, `findByArtistTitleYear`, `create`, `updateMetadata`, `normalizeTitle`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[AlbumDao]], [[Genre]], [[SearchText]].

Referenciado por: [[PostJdbcDao]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>), líneas 1–102.

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
import java.util.Locale;
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
                        SELECT_ALBUM + "WHERE artist_id = ? AND normalized_title = ? AND release_year = ?",
                        ROW_MAPPER, artistId, normalizeTitle(title), releaseYear)
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
        parameters.put("normalized_title", normalizeTitle(title));
        parameters.put("artist_id", artistId);
        parameters.put("release_year", releaseYear);
        parameters.put("genre", genre == null ? null : genre.name());
        parameters.put("search_phrase", SearchText.phrase(title));

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Album(id.longValue(), title, artistId, releaseYear, genre, null);
    }

    @Override
    public Album updateMetadata(final long id, final String title, final Genre genre) {
        if (jdbcTemplate.update(
                "UPDATE albums SET title = ?, normalized_title = ?, genre = ?, search_phrase = ? WHERE id = ?",
                title, normalizeTitle(title), genre == null ? null : genre.name(), SearchText.phrase(title),
                id) != 1) {
            throw new IllegalStateException("Album disappeared while updating metadata");
        }
        return jdbcTemplate.queryForObject(SELECT_ALBUM + "WHERE id = ?", ROW_MAPPER, id);
    }

    // Misma regla que el LOWER(title) con que la migracion relleno las filas anteriores.
    private static String normalizeTitle(final String title) {
        return title.toLowerCase(Locale.ROOT);
    }

}
```
