---
title: "ArtistJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java"]
---

# ArtistJdbcDao

The constructor creates JdbcTemplate and a SimpleJdbcInsert for artists with generated `id`. `findByName` binds exact name with `?`, maps aliases through a shared static RowMapper, and returns Optional. `create` inserts the supplied name and returns an [[Artist]] with the generated key. `findOrCreate` uses lazy `orElseGet`, so inserts happen only on lookup misses. It does not catch concurrent uniqueness violations.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java, lines 1–55](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>)

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
import java.util.Map;
import java.util.Optional;

@Repository
public class ArtistJdbcDao implements ArtistDao {

    private static final RowMapper<Artist> ROW_MAPPER = (resultSet, rowNum) -> new Artist(
            resultSet.getLong("artist_id"),
            resultSet.getString("artist_name")
    );

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

}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
