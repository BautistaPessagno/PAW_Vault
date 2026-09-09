---
title: "ImageJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java"]
---

# ImageJdbcDao

Uses JdbcTemplate and SimpleJdbcInsert against images. findById selects aliased ID, content type and binary data into [[Image]]; a missing ID returns Optional.empty. create binds content_type and data and returns the generated ID. It does not validate MIME content or size; [[ImageServiceImpl]] owns that policy.

## Connections

Project types referenced: [[Image]], [[ImageDao]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java, lines 1–53](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;
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
public class ImageJdbcDao implements ImageDao {

    private static final RowMapper<Image> ROW_MAPPER = (resultSet, rowNum) -> new Image(
            resultSet.getLong("image_id"),
            resultSet.getString("image_content_type"),
            resultSet.getBytes("image_data")
    );

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public ImageJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("images")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Optional<Image> findById(final long id) {
        return jdbcTemplate.query(
                        "SELECT id AS image_id, content_type AS image_content_type, data AS image_data " +
                                "FROM images WHERE id = ?",
                        ROW_MAPPER, id)
                .stream()
                .findFirst();
    }

    @Override
    public Image create(final String contentType, final byte[] data) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("content_type", contentType);
        parameters.put("data", data);
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Image(id.longValue(), contentType, data);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
