---
title: "PostJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java"]
---

# PostJdbcDao

Reads PostSummary through a four-table INNER JOIN of posts, users, albums and artists. Queries include albums.cover_image_id and use AlbumJdbcDao.readCoverImageId to preserve null. Image bytes are fetched separately through [[ImageController]]. findFeatured orders post IDs descending and binds the limit; findById filters one ID. Pair existence is a pre-check, and insert translates DuplicateKeyException to [[DuplicatePostKeyException]].

## Connections

Project types referenced: [[AlbumJdbcDao]], [[DuplicatePostKeyException]], [[Post]], [[PostDao]], [[PostSummary]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, lines 1–82](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
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
public class PostJdbcDao implements PostDao {

    private static final RowMapper<PostSummary> ROW_MAPPER = (resultSet, rowNum) -> new PostSummary(
            resultSet.getLong("post_id"),
            resultSet.getLong("user_id"),
            resultSet.getString("publisher_email"),
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getInt("album_release_year"),
            AlbumJdbcDao.readCoverImageId(resultSet)
    );

    private static final String SUMMARY_SELECT =
            "SELECT p.id AS post_id, u.id AS user_id, u.email AS publisher_email, " +
                    "a.id AS album_id, a.title AS album_title, ar.name AS artist_name, " +
                    "a.release_year AS album_release_year, a.cover_image_id AS album_cover_image_id " +
                    "FROM posts p JOIN users u ON u.id = p.user_id " +
                    "JOIN albums a ON a.id = p.album_id JOIN artists ar ON ar.id = a.artist_id ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public PostJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("posts")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public List<PostSummary> findFeatured(final int limit) {
        return Collections.unmodifiableList(jdbcTemplate.query(
                SUMMARY_SELECT + "ORDER BY p.id DESC LIMIT ?", ROW_MAPPER, limit));
    }

    @Override
    public Optional<PostSummary> findById(final long id) {
        return jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public boolean existsByUserIdAndAlbumId(final long userId, final long albumId) {
        return Boolean.TRUE.equals(jdbcTemplate.queryForObject(
                "SELECT COUNT(*) > 0 AS post_exists FROM posts WHERE user_id = ? AND album_id = ?",
                Boolean.class, userId, albumId));
    }

    @Override
    public Post create(final long userId, final long albumId) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("album_id", albumId);

        try {
            final Number id = jdbcInsert.executeAndReturnKey(parameters);
            return new Post(id.longValue(), userId, albumId);
        } catch (final DuplicateKeyException e) {
            throw new DuplicatePostKeyException();
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
