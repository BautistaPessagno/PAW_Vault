---
title: "ArtistJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java"]
---

# ArtistJdbcDao

Looks up an artist name before inserting it and lists artists with ORDER BY LOWER(name). The unique name constraint arbitrates competing inserts; the outer publishing service translates integrity errors.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java, lines 1–66](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
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

    // Los artistas se guardan en minuscula, pero el filtro de la landing los lista
    // alfabeticamente igual que se ven en pantalla.
    private static final String FIND_ALL_QUERY =
            "SELECT id AS artist_id, name AS artist_name FROM artists ORDER BY LOWER(name)";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public ArtistJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("artists")
                .usingGeneratedKeyColumns("id");
    }

    private Optional<Artist> findByName(final String name) {
        return jdbcTemplate.query(
                        "SELECT id AS artist_id, name AS artist_name FROM artists WHERE name = ?",
                        ROW_MAPPER, name)
                .stream()
                .findAny();
    }

    private Artist create(final String name) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("name", name);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Artist(id.longValue(), name);
    }

    @Override
    public Artist findOrCreate(final String name) {
        return findByName(name).orElseGet(() -> create(name));
    }

    @Override
    public List<Artist> findAll() {
        return List.copyOf(jdbcTemplate.query(FIND_ALL_QUERY, ROW_MAPPER));
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
