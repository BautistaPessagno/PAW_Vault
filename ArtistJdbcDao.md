---
title: "ArtistJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java"]
---

# ArtistJdbcDao

Artistas con Spring JDBC. `findOrCreate` inserta dentro de un savepoint: si otra transacción ganó la carrera, vuelve al savepoint y relee, porque PostgreSQL deja la transacción inutilizable tras una violación de unicidad. Las sugerencias se ordenan con un `CASE` en SQL.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT_ARTIST`, `SUGGESTION_RANK`, `FIND_SUGGESTIONS_QUERY`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `findByNormalizedName`, `create`, `findOrCreate`, `updateDisplayName`, `findSuggestions`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]], [[ArtistDao]], [[SearchText]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>), líneas 1–113.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.SearchText;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.ConnectionCallback;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.Savepoint;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class ArtistJdbcDao implements ArtistDao {

    private static final RowMapper<Artist> ROW_MAPPER = (resultSet, rowNum) -> new Artist(
            resultSet.getLong("artist_id"),
            resultSet.getString("artist_name")
    );

    private static final String SELECT_ARTIST =
            "SELECT id AS artist_id, name AS artist_name FROM artists ";

    // Reproduce en SQL el ranking que antes se calculaba en memoria sobre la tabla
    // entera: coincidencia exacta, prefijo del nombre completo, prefijo de alguna
    // palabra y, por ultimo, aparicion en cualquier posicion.
    private static final String SUGGESTION_RANK =
            "CASE WHEN REPLACE(search_phrase, ' ', '') = ? THEN 0 "
                    + "WHEN REPLACE(search_phrase, ' ', '') LIKE ? THEN 1 "
                    + "WHEN ' ' || search_phrase LIKE ? THEN 2 ELSE 3 END";

    // El WHERE es el caso mas amplio de los cuatro, asi que no descarta ninguna
    // fila que el ranking pudiera puntuar.
    private static final String FIND_SUGGESTIONS_QUERY =
            SELECT_ARTIST + "WHERE REPLACE(search_phrase, ' ', '') LIKE ? "
                    + "ORDER BY " + SUGGESTION_RANK + ", search_phrase, LOWER(name), id LIMIT ?";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public ArtistJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("artists")
                .usingGeneratedKeyColumns("id");
    }

    private Optional<Artist> findByNormalizedName(final String normalizedName) {
        return jdbcTemplate.query(SELECT_ARTIST + "WHERE normalized_name = ?", ROW_MAPPER, normalizedName)
                .stream()
                .findAny();
    }

    private Artist create(final String displayName, final String normalizedName) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("name", displayName);
        parameters.put("normalized_name", normalizedName);
        parameters.put("search_phrase", SearchText.phrase(displayName));

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Artist(id.longValue(), displayName);
    }

    @Override
    public Artist findOrCreate(final String displayName, final String normalizedName) {
        final Optional<Artist> existing = findByNormalizedName(normalizedName);
        if (existing.isPresent()) {
            return existing.get();
        }
        return jdbcTemplate.execute((ConnectionCallback<Artist>) connection -> {
            // PostgreSQL deja la transaccion inutilizable despues de una violacion
            // de unicidad. El savepoint permite releer la fila que gano la carrera.
            final Savepoint savepoint = connection.getAutoCommit() ? null : connection.setSavepoint();
            try {
                return create(displayName, normalizedName);
            } catch (final DuplicateKeyException e) {
                if (savepoint != null) {
                    connection.rollback(savepoint);
                }
                return findByNormalizedName(normalizedName).orElseThrow(() -> e);
            } finally {
                if (savepoint != null) {
                    connection.releaseSavepoint(savepoint);
                }
            }
        });
    }

    @Override
    public Artist updateDisplayName(final long id, final String displayName) {
        if (jdbcTemplate.update("UPDATE artists SET name = ?, search_phrase = ? WHERE id = ?",
                displayName, SearchText.phrase(displayName), id) != 1) {
            throw new IllegalStateException("Artist disappeared while updating display name");
        }
        return jdbcTemplate.queryForObject(SELECT_ARTIST + "WHERE id = ?", ROW_MAPPER, id);
    }

    @Override
    public List<Artist> findSuggestions(final String normalizedQuery, final int limit) {
        return List.copyOf(jdbcTemplate.query(FIND_SUGGESTIONS_QUERY, ROW_MAPPER,
                "%" + normalizedQuery + "%", normalizedQuery, normalizedQuery + "%",
                "% " + normalizedQuery + "%", limit));
    }

}
```
