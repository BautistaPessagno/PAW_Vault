---
title: "ReviewJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java"]
---

# ReviewJdbcDao

Reseñas con Spring JDBC. `update` reactiva la fila existente; `deactivate` solo afecta una reseña activa. El listado y las estadísticas filtran por rol uniendo con la consulta (`i.buyer_id` para comprador, `COALESCE(p.user_id, i.seller_id)` para vendedor) y traen la foto del autor.

## Guía de lectura

Datos y dependencias declaradas: `REVIEW_MAPPER`, `STATS_MAPPER`, `REVIEW_SELECT`, `ROLE_FROM`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `findByInquiryAndAuthor`, `findActiveBySubjectId`, `roleWhere`, `statsBySubjectId`, `create`, `update`, `deactivate`, `readNullableLong`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewDao]], [[ReviewStats]], [[ReviewSubjectRole]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java>), líneas 1–108.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewStats;
import ar.edu.itba.paw.models.ReviewSubjectRole;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class ReviewJdbcDao implements ReviewDao {
    private static final RowMapper<Review> REVIEW_MAPPER = (resultSet, rowNum) -> new Review(
            resultSet.getLong("id"), resultSet.getLong("inquiry_id"), resultSet.getLong("author_id"),
            resultSet.getLong("subject_id"), resultSet.getString("username"),
            readNullableLong(resultSet, "avatar_image_id"), resultSet.getInt("rating"),
            resultSet.getString("body"), resultSet.getBoolean("active"),
            resultSet.getTimestamp("created_at").toLocalDateTime());
    private static final RowMapper<ReviewStats> STATS_MAPPER = (resultSet, rowNum) ->
            new ReviewStats(resultSet.getInt("review_count"), resultSet.getDouble("average_rating"));
    private static final String REVIEW_SELECT = "SELECT r.id, r.inquiry_id, r.author_id, r.subject_id, "
            + "u.username, u.avatar_image_id, r.rating, r.body, r.active, r.created_at "
            + "FROM reviews r JOIN users u ON u.id = r.author_id ";
    private static final String ROLE_FROM = "JOIN inquiries i ON i.id = r.inquiry_id "
            + "LEFT JOIN posts p ON p.id = i.post_id ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    @Autowired
    public ReviewJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource).withTableName("reviews")
                .usingColumns("inquiry_id", "author_id", "subject_id", "rating", "body")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Optional<Review> findByInquiryAndAuthor(final long inquiryId, final long authorId) {
        return jdbcTemplate.query(REVIEW_SELECT + "WHERE r.inquiry_id = ? AND r.author_id = ?",
                REVIEW_MAPPER, inquiryId, authorId).stream().findFirst();
    }

    @Override
    public List<Review> findActiveBySubjectId(final long subjectId, final ReviewSubjectRole role,
                                            final int limit, final int offset) {
        return List.copyOf(jdbcTemplate.query(REVIEW_SELECT + ROLE_FROM + roleWhere(role)
                + " ORDER BY r.created_at DESC, r.id DESC LIMIT ? OFFSET ?",
                REVIEW_MAPPER, subjectId, limit, offset));
    }

    private static String roleWhere(final ReviewSubjectRole role) {
        return "WHERE r.subject_id = ? AND r.active = TRUE AND "
                + (role == ReviewSubjectRole.BUYER ? "i.buyer_id = r.subject_id"
                : "COALESCE(p.user_id, i.seller_id) = r.subject_id");
    }

    @Override
    public ReviewStats statsBySubjectId(final long subjectId, final ReviewSubjectRole role) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) AS review_count, "
                        + "COALESCE(AVG(CAST(r.rating AS DECIMAL(10, 2))), 0) AS average_rating "
                        + "FROM reviews r " + ROLE_FROM + roleWhere(role),
                STATS_MAPPER, subjectId);
    }

    @Override
    public Review create(final long inquiryId, final long authorId, final long subjectId,
                         final int rating, final String body) {
        final Map<String, Object> values = new HashMap<>();
        values.put("inquiry_id", inquiryId);
        values.put("author_id", authorId);
        values.put("subject_id", subjectId);
        values.put("rating", rating);
        values.put("body", body);
        final long id = jdbcInsert.executeAndReturnKey(values).longValue();
        return jdbcTemplate.query(REVIEW_SELECT + "WHERE r.id = ?", REVIEW_MAPPER, id).get(0);
    }

    @Override
    public Optional<Review> update(final long inquiryId, final long authorId, final int rating, final String body) {
        if (jdbcTemplate.update("UPDATE reviews SET rating = ?, body = ?, active = TRUE "
                + "WHERE inquiry_id = ? AND author_id = ?", rating, body, inquiryId, authorId) != 1) {
            return Optional.empty();
        }
        return findByInquiryAndAuthor(inquiryId, authorId);
    }

    @Override
    public boolean deactivate(final long inquiryId, final long authorId) {
        return jdbcTemplate.update("UPDATE reviews SET active = FALSE "
                + "WHERE inquiry_id = ? AND author_id = ? AND active = TRUE", inquiryId, authorId) == 1;
    }

    // Las Cuentas sin foto quedan en NULL: getLong devuelve 0, hay que consultar wasNull.
    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }
}
```
