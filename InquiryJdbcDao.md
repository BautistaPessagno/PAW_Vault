---
title: "InquiryJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java"]
---

# InquiryJdbcDao

Inserts PENDING inquiries and loads a compact [[Inquiry]] with a nullable post ID. Inbox pages use two bounded statements: a page of group keys (the post ID, or album and seller for deleted posts) ordered by each group's newest inquiry ID, then every row for those keys through LEFT JOIN posts and COALESCE over the copied album/seller. It also counts groups and inquiries, applies guarded PENDING updates and rejects competitors. detachFromPost copies album and seller onto each inquiry, clears post_id and rejects the pending ones.

## Connections

Project types referenced: [[Inquiry]], [[InquiryDao]], [[InquiryStatus]], [[InquirySummary]], [[PostStatus]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java, lines 1–214](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostStatus;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class InquiryJdbcDao implements InquiryDao {

    private static final RowMapper<Inquiry> ROW_MAPPER = (resultSet, rowNum) -> new Inquiry(
            resultSet.getLong("inquiry_id"),
            readNullableLong(resultSet, "inquiry_post_id"),
            resultSet.getLong("inquiry_buyer_id"),
            resultSet.getString("inquiry_message"),
            InquiryStatus.valueOf(resultSet.getString("inquiry_status"))
    );

    private static final String SELECT = "SELECT id AS inquiry_id, post_id AS inquiry_post_id, "
            + "buyer_id AS inquiry_buyer_id, message AS inquiry_message, status AS inquiry_status FROM inquiries ";

    private static final RowMapper<InquirySummary> SUMMARY_ROW_MAPPER = (resultSet, rowNum) -> new InquirySummary(
            resultSet.getLong("inquiry_id"),
            readNullableLong(resultSet, "post_id"),
            resultSet.getLong("album_id"),
            resultSet.getLong("seller_id"),
            resultSet.getString("buyer_username"),
            resultSet.getString("seller_username"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            readNullableLong(resultSet, "post_image_id"),
            resultSet.getString("inquiry_message"),
            InquiryStatus.valueOf(resultSet.getString("inquiry_status")),
            readNullablePostStatus(resultSet, "post_status")
    );

    // Clave de grupo de la bandeja: el id del post, o "d<album>-<publicante>" si el post fue
    // eliminado. Una sola expresion valida en PostgreSQL y HSQLDB, para agrupar, contar y filtrar.
    private static final String GROUP_KEY = "COALESCE(CAST(i.post_id AS VARCHAR(20)), "
            + "'d' || CAST(COALESCE(p.album_id, i.album_id) AS VARCHAR(20)) || '-' "
            + "|| CAST(COALESCE(p.user_id, i.seller_id) AS VARCHAR(20)))";

    // Una publicacion eliminada ya no esta en posts: el album y el vendedor salen de la
    // copia que guarda la consulta. Reutilizado por SUMMARY_SELECT para no repetir el FROM.
    private static final String GROUP_FROM = "FROM inquiries i LEFT JOIN posts p ON p.id = i.post_id ";

    private static final String SUMMARY_SELECT = "SELECT i.id AS inquiry_id, p.id AS post_id, "
            + "a.id AS album_id, seller.id AS seller_id, "
            + "buyer.username AS buyer_username, seller.username AS seller_username, "
            + "a.title AS album_title, ar.name AS artist_name, i.message AS inquiry_message, "
            + "COALESCE(p.image_id, a.cover_image_id) AS post_image_id, "
            + "i.status AS inquiry_status, p.status AS post_status "
            + GROUP_FROM
            + "JOIN users buyer ON buyer.id = i.buyer_id "
            + "JOIN users seller ON seller.id = COALESCE(p.user_id, i.seller_id) "
            + "JOIN albums a ON a.id = COALESCE(p.album_id, i.album_id) JOIN artists ar ON ar.id = a.artist_id ";

    private static final String SELLER_WHERE = "WHERE COALESCE(p.user_id, i.seller_id) = ? ";

    private static final String BUYER_WHERE = "WHERE i.buyer_id = ? ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // Los albums sin portada propia quedan en NULL: getLong devuelve 0, hay que consultar wasNull.
    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }

    private static PostStatus readNullablePostStatus(final ResultSet resultSet, final String column)
            throws SQLException {
        final String status = resultSet.getString(column);
        return status == null ? null : PostStatus.valueOf(status);
    }

    @Autowired
    public InquiryJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("inquiries")
                .usingColumns("post_id", "buyer_id", "message", "status")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Inquiry create(final long postId, final long buyerId, final String message) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("post_id", postId);
        parameters.put("buyer_id", buyerId);
        parameters.put("message", message);
        parameters.put("status", InquiryStatus.PENDING.name());

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Inquiry(id.longValue(), postId, buyerId, message, InquiryStatus.PENDING);
    }

    @Override
    public Optional<Inquiry> findById(final long id) {
        return jdbcTemplate.query(SELECT + "WHERE id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public List<InquirySummary> findByBuyerId(final long buyerId, final int groupLimit, final int groupOffset) {
        return findGroupPage(BUYER_WHERE, buyerId, groupLimit, groupOffset);
    }

    @Override
    public List<InquirySummary> findBySellerId(final long sellerId, final int groupLimit, final int groupOffset) {
        return findGroupPage(SELLER_WHERE, sellerId, groupLimit, groupOffset);
    }

    @Override
    public int countGroupsByBuyerId(final long buyerId) {
        return jdbcTemplate.queryForObject("SELECT COUNT(DISTINCT " + GROUP_KEY + ") " + GROUP_FROM + BUYER_WHERE,
                Integer.class, buyerId);
    }

    @Override
    public int countGroupsBySellerId(final long sellerId) {
        return jdbcTemplate.queryForObject("SELECT COUNT(DISTINCT " + GROUP_KEY + ") " + GROUP_FROM + SELLER_WHERE,
                Integer.class, sellerId);
    }

    /*
     * Dos sentencias acotadas, sin N+1: primero la pagina de claves de grupo ordenada por
     * la consulta mas nueva de cada grupo, despues todas las consultas de esas claves. La
     * lista de claves se bindea con un placeholder por clave.
     *
     * El id es serial y se asigna al insertar: "mas nueva" es "id mas alto". Las dos
     * sentencias ordenan por id, asi el orden de los grupos coincide con el de sus filas
     * incluso cuando dos consultas comparten created_at.
     */
    private List<InquirySummary> findGroupPage(final String where, final long userId,
                                               final int groupLimit, final int groupOffset) {
        final List<String> keys = jdbcTemplate.queryForList(
                "SELECT g.group_key FROM (SELECT " + GROUP_KEY + " AS group_key, "
                        + "MAX(i.id) AS last_id " + GROUP_FROM + where
                        + "GROUP BY " + GROUP_KEY + ") g ORDER BY g.last_id DESC LIMIT ? OFFSET ?",
                String.class, userId, groupLimit, groupOffset);
        if (keys.isEmpty()) {
            return List.of();
        }
        final String placeholders = String.join(", ", Collections.nCopies(keys.size(), "?"));
        final List<Object> parameters = new ArrayList<>();
        parameters.add(userId);
        parameters.addAll(keys);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + where + "AND " + GROUP_KEY
                        + " IN (" + placeholders + ") ORDER BY i.id DESC",
                SUMMARY_ROW_MAPPER, parameters.toArray()));
    }

    @Override
    public boolean acceptPending(final long id) {
        return updatePending(id, InquiryStatus.ACCEPTED) == 1;
    }

    @Override
    public boolean rejectPending(final long id) {
        return updatePending(id, InquiryStatus.REJECTED) == 1;
    }

    private int updatePending(final long id, final InquiryStatus status) {
        return jdbcTemplate.update("UPDATE inquiries SET status = ? WHERE id = ? AND status = ?",
                status.name(), id, InquiryStatus.PENDING.name());
    }

    // La otra mitad de la bandeja solo necesita el numero para la sub-nav, no las filas.
    @Override
    public int countByBuyerId(final long buyerId) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) FROM inquiries WHERE buyer_id = ?",
                Integer.class, buyerId);
    }

    @Override
    public int countBySellerId(final long sellerId) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) FROM inquiries i "
                + "LEFT JOIN posts p ON p.id = i.post_id WHERE COALESCE(p.user_id, i.seller_id) = ?",
                Integer.class, sellerId);
    }

    @Override
    public int rejectOtherPending(final long postId, final long acceptedInquiryId) {
        return jdbcTemplate.update("UPDATE inquiries SET status = ? WHERE post_id = ? AND id <> ? AND status = ?",
                InquiryStatus.REJECTED.name(), postId, acceptedInquiryId, InquiryStatus.PENDING.name());
    }

    // Antes de borrar la publicacion, cada consulta se queda con su album y su vendedor y
    // deja de apuntar al post. Las pendientes se cierran: ya no hay nada que aceptar.
    @Override
    public int detachFromPost(final long postId) {
        return jdbcTemplate.update("UPDATE inquiries SET "
                        + "album_id = (SELECT album_id FROM posts WHERE id = inquiries.post_id), "
                        + "seller_id = (SELECT user_id FROM posts WHERE id = inquiries.post_id), "
                        + "post_id = NULL, status = CASE WHEN status = ? THEN ? ELSE status END "
                        + "WHERE post_id = ?",
                InquiryStatus.PENDING.name(), InquiryStatus.REJECTED.name(), postId);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
