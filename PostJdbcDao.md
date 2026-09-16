---
title: "PostJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java"]
---

# PostJdbcDao

Builds parameterized AND filters for AVAILABLE posts and title/artist text. Escapes LIKE wildcards, maps sort enums to fixed ORDER BY clauses and applies LIMIT. Nullable prices sort last; most ties use created_at DESC then id DESC. Images use COALESCE(post image, legacy album cover). findByIdForUpdate locks the posts row before the joined read. New inserts set stock=1 and AVAILABLE; markSoldIfAvailable is conditional.

## Connections

Project types referenced: [[AlbumJdbcDao]], [[Condition]], [[DuplicatePostKeyException]], [[Post]], [[PostDao]], [[PostSearchCriteria]], [[PostSort]], [[PostStatus]], [[PostSummary]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, lines 1–224](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.PostSearchCriteria;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.Optional;

@Repository
public class PostJdbcDao implements PostDao {

    private static final RowMapper<PostSummary> ROW_MAPPER = (resultSet, rowNum) -> new PostSummary(
            resultSet.getLong("post_id"),
            resultSet.getLong("user_id"),
            resultSet.getString("publisher_email"),
            resultSet.getString("publisher_locale"),
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getInt("album_release_year"),
            AlbumJdbcDao.readGenre(resultSet),
            readNullableLong(resultSet, "post_image_id"),
            readNullableInt(resultSet, "post_price"),
            resultSet.getString("post_description"),
            readCondition(resultSet),
            readNullableInt(resultSet, "post_pressing_year"),
            resultSet.getString("post_zone"),
            PostStatus.valueOf(resultSet.getString("post_status"))
    );

    private static final String SUMMARY_SELECT =
            "SELECT p.id AS post_id, u.id AS user_id, u.email AS publisher_email, " +
                    "u.preferred_locale AS publisher_locale, " +
                    "a.id AS album_id, a.title AS album_title, ar.name AS artist_name, " +
                    "a.release_year AS album_release_year, a.genre AS album_genre, " +
                    "COALESCE(p.image_id, a.cover_image_id) AS post_image_id, " +
                    "p.price AS post_price, p.description AS post_description, " +
                    "p.item_condition AS post_condition, p.pressing_year AS post_pressing_year, " +
                    "p.zone AS post_zone, p.status AS post_status " +
                    "FROM posts p JOIN users u ON u.id = p.user_id " +
                    "JOIN albums a ON a.id = p.album_id JOIN artists ar ON ar.id = a.artist_id ";

    private static final String LIKE_ESCAPE = "\\";
    // El SQL y escapeLike() salen del mismo caracter: si cambia uno, cambia el otro.
    private static final String LIKE_ESCAPE_CLAUSE = "ESCAPE '" + LIKE_ESCAPE + "'";
    // Desempate de todo orden: lo publicado mas recientemente primero. Los posts
    // anteriores a created_at comparten fecha y se desempatan por id.
    private static final String NEWEST_FIRST = "p.created_at DESC, p.id DESC";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // Los posts anteriores a las columnas comerciales tienen NULL: getInt devuelve 0, hay que consultar wasNull.
    private static Integer readNullableInt(final ResultSet resultSet, final String column) throws SQLException {
        final int value = resultSet.getInt(column);
        return resultSet.wasNull() ? null : value;
    }

    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }

    private static Condition readCondition(final ResultSet resultSet) throws SQLException {
        final String condition = resultSet.getString("post_condition");
        return condition == null ? null : Condition.valueOf(condition);
    }

    @Autowired
    public PostJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("posts")
                // No incluimos created_at: el DEFAULT de la base es el único reloj de publicación.
                .usingColumns("user_id", "album_id", "price", "description", "item_condition", "pressing_year",
                        "zone", "stock", "image_id", "status")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public List<PostSummary> search(final PostSearchCriteria criteria, final int limit) {
        final List<String> clauses = new ArrayList<>();
        final List<Object> parameters = new ArrayList<>();
        // Los vendidos no se ofrecen: la landing solo lista lo que todavia se puede comprar.
        clauses.add("p.status = ?");
        parameters.add(PostStatus.AVAILABLE.name());
        if (criteria.getQuery() != null) {
            final String pattern = "%" + escapeLike(criteria.getQuery().toLowerCase(Locale.ROOT)) + "%";
            clauses.add("(LOWER(a.title) LIKE ? " + LIKE_ESCAPE_CLAUSE
                    + " OR LOWER(ar.name) LIKE ? " + LIKE_ESCAPE_CLAUSE + ")");
            parameters.add(pattern);
            parameters.add(pattern);
        }
        if (criteria.getGenre() != null) {
            clauses.add("a.genre = ?");
            parameters.add(criteria.getGenre().name());
        }
        if (criteria.getCondition() != null) {
            clauses.add("p.item_condition = ?");
            parameters.add(criteria.getCondition().name());
        }
        if (criteria.getArtistId() != null) {
            clauses.add("a.artist_id = ?");
            parameters.add(criteria.getArtistId());
        }
        if (criteria.getReleaseYear() != null) {
            clauses.add("a.release_year = ?");
            parameters.add(criteria.getReleaseYear());
        }
        if (criteria.getMinPrice() != null) {
            clauses.add("p.price >= ?");
            parameters.add(criteria.getMinPrice());
        }
        if (criteria.getMaxPrice() != null) {
            clauses.add("p.price <= ?");
            parameters.add(criteria.getMaxPrice());
        }
        final String where = "WHERE " + String.join(" AND ", clauses) + " ";
        parameters.add(limit);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + where + "ORDER BY "
                + orderBy(criteria.getSort()) + " LIMIT ?", ROW_MAPPER, parameters.toArray()));
    }

    // Cada criterio mapea a un ORDER BY fijo: al SQL nunca entra texto del usuario.
    // El precio es nullable en los posts viejos, por eso van ultimos en ambas direcciones.
    private static String orderBy(final PostSort sort) {
        switch (sort) {
            case OLDEST:
                return "p.created_at ASC, p.id ASC";
            case PRICE_ASC:
                return "p.price ASC NULLS LAST, " + NEWEST_FIRST;
            case PRICE_DESC:
                return "p.price DESC NULLS LAST, " + NEWEST_FIRST;
            case TITLE_ASC:
                return "LOWER(a.title) ASC, " + NEWEST_FIRST;
            case TITLE_DESC:
                return "LOWER(a.title) DESC, " + NEWEST_FIRST;
            case ARTIST_ASC:
                return "LOWER(ar.name) ASC, " + NEWEST_FIRST;
            case ARTIST_DESC:
                return "LOWER(ar.name) DESC, " + NEWEST_FIRST;
            case RELEASE_YEAR_ASC:
                return "a.release_year ASC, " + NEWEST_FIRST;
            case RELEASE_YEAR_DESC:
                return "a.release_year DESC, " + NEWEST_FIRST;
            case NEWEST:
            default:
                return NEWEST_FIRST;
        }
    }

    // Los comodines de LIKE que escriba el usuario se buscan literalmente: "%" no puede traer todo el catalogo.
    private static String escapeLike(final String value) {
        return value.replace(LIKE_ESCAPE, LIKE_ESCAPE + LIKE_ESCAPE)
                .replace("%", LIKE_ESCAPE + "%")
                .replace("_", LIKE_ESCAPE + "_");
    }

    @Override
    public Optional<PostSummary> findById(final long id) {
        return jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public Optional<PostSummary> findByIdForUpdate(final long id) {
        if (jdbcTemplate.queryForList("SELECT id FROM posts WHERE id = ? FOR UPDATE", Long.class, id).isEmpty()) {
            return Optional.empty();
        }
        return findById(id);
    }

    @Override
    public boolean existsByUserIdAndAlbumId(final long userId, final long albumId) {
        return Boolean.TRUE.equals(jdbcTemplate.queryForObject(
                "SELECT COUNT(*) > 0 AS post_exists FROM posts WHERE user_id = ? AND album_id = ?",
                Boolean.class, userId, albumId));
    }

    @Override
    public Post create(final long userId, final long albumId, final int price, final String description,
                       final Condition condition, final Integer pressingYear, final String zone, final Long imageId) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("album_id", albumId);
        parameters.put("price", price);
        parameters.put("description", description);
        parameters.put("item_condition", condition == null ? null : condition.name());
        parameters.put("pressing_year", pressingYear);
        parameters.put("zone", zone);
        parameters.put("stock", 1);
        parameters.put("image_id", imageId);
        parameters.put("status", PostStatus.AVAILABLE.name());
        try {
            final Number id = jdbcInsert.executeAndReturnKey(parameters);
            return new Post(id.longValue(), userId, albumId, price, description, condition, pressingYear, zone,
                    imageId, PostStatus.AVAILABLE);
        } catch (final DuplicateKeyException e) {
            throw new DuplicatePostKeyException();
        }
    }

    @Override
    public boolean markSoldIfAvailable(final long id) {
        return jdbcTemplate.update("UPDATE posts SET status = ? WHERE id = ? AND status = ?",
                PostStatus.SOLD.name(), id, PostStatus.AVAILABLE.name()) == 1;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
