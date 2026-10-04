---
title: "ImageJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java"]
---

# ImageJdbcDao

Imágenes con Spring JDBC. Cada lectura exige con `EXISTS` que la imagen pertenezca al post, usuario verificado o álbum de la URL. El borrado lleva cuatro `NOT EXISTS`: solo elimina lo que nadie referencia.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `IMAGE_SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `findById`, `findPostImage`, `findUserAvatar`, `findAlbumCover`, `create`, `delete`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageDao]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>), líneas 1–87.

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

    private static final String IMAGE_SELECT = "SELECT i.id AS image_id, "
            + "i.content_type AS image_content_type, i.data AS image_data FROM images i ";

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
                        IMAGE_SELECT + "WHERE i.id = ?",
                        ROW_MAPPER, id)
                .stream()
                .findFirst();
    }

    @Override
    public Optional<Image> findPostImage(final long postId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM posts p JOIN albums a ON a.id = p.album_id WHERE p.id = ? "
                        + "AND (p.image_id = i.id OR a.cover_image_id = i.id OR EXISTS ("
                        + "SELECT 1 FROM post_images pi WHERE pi.post_id = p.id AND pi.image_id = i.id)))",
                ROW_MAPPER, imageId, postId).stream().findFirst();
    }

    @Override
    public Optional<Image> findUserAvatar(final long userId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM users u WHERE u.id = ? AND u.verified = TRUE AND u.avatar_image_id = i.id)",
                ROW_MAPPER, imageId, userId).stream().findFirst();
    }

    @Override
    public Optional<Image> findAlbumCover(final long albumId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM albums a WHERE a.id = ? AND a.cover_image_id = i.id)",
                ROW_MAPPER, imageId, albumId).stream().findFirst();
    }

    @Override
    public Image create(final String contentType, final byte[] data) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("content_type", contentType);
        parameters.put("data", data);
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Image(id.longValue(), contentType, data);
    }

    @Override
    public boolean delete(final long id) {
        return jdbcTemplate.update("DELETE FROM images WHERE id = ? " +
                        "AND NOT EXISTS (SELECT 1 FROM albums WHERE cover_image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM posts WHERE image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM post_images WHERE image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM users WHERE avatar_image_id = images.id)", id) == 1;
    }
}
```
