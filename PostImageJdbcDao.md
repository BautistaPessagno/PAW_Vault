---
title: "PostImageJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/PostImageJdbcDao.java"]
---

# PostImageJdbcDao

Galería con Spring JDBC: lista los ids por `display_order`, agrega y borra por post.

## Guía de lectura

Datos y dependencias declaradas: `IMAGE_ID_MAPPER`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `findImageIdsByPostId`, `add`, `deleteByPostId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostImageDao]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostImageJdbcDao.java>), líneas 1–50.

```java
package ar.edu.itba.paw.persistence;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class PostImageJdbcDao implements PostImageDao {

    private static final RowMapper<Long> IMAGE_ID_MAPPER = (resultSet, rowNum) -> resultSet.getLong("image_id");

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public PostImageJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("post_images")
                .usingColumns("post_id", "image_id", "display_order")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public List<Long> findImageIdsByPostId(final long postId) {
        return List.copyOf(jdbcTemplate.query("SELECT image_id FROM post_images WHERE post_id = ? ORDER BY display_order",
                IMAGE_ID_MAPPER, postId));
    }

    @Override
    public long add(final long postId, final long imageId, final int position) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("post_id", postId);
        parameters.put("image_id", imageId);
        parameters.put("display_order", position);
        return jdbcInsert.executeAndReturnKey(parameters).longValue();
    }

    @Override
    public int deleteByPostId(final long postId) {
        return jdbcTemplate.update("DELETE FROM post_images WHERE post_id = ?", postId);
    }
}
```
