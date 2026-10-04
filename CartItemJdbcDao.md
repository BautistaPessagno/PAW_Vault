---
title: "CartItemJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/CartItemJdbcDao.java"]
---

# CartItemJdbcDao

Carrito con Spring JDBC. La clave es `(user_id, post_id)`, así que inserta con `execute` y trata el duplicado como "ya estaba". Listar y contar comparten un `FROM` filtrado por estado del post y por `NOT EXISTS` de una consulta abierta del comprador, ordenado por publicante.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `FILTERED_FROM`, `FILTERED_SELECT`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `readNullableLong`, `add`, `remove`, `removeAll`, `contains`, `findByUserId`, `countByUserId`, `filtered`, `filterParameters`, `placeholders`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartItem]], [[CartItemDao]], [[InquiryStatus]], [[PostStatus]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/CartItemJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/CartItemJdbcDao.java>), líneas 1–138.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.CartItem;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.PostStatus;
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
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Repository
public class CartItemJdbcDao implements CartItemDao {

    private static final RowMapper<CartItem> ROW_MAPPER = (resultSet, rowNum) -> new CartItem(
            resultSet.getLong("post_id"),
            resultSet.getLong("seller_id"),
            resultSet.getString("seller_username"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getInt("album_release_year"),
            readNullableLong(resultSet, "post_image_id"),
            resultSet.getInt("post_price"));

    // El filtro llega del service: el estado del Post y los de las Consultas que lo ocultan.
    private static final String FILTERED_FROM = "FROM cart_items ci "
            + "JOIN posts p ON p.id = ci.post_id "
            + "JOIN users s ON s.id = p.user_id "
            + "JOIN albums a ON a.id = p.album_id JOIN artists ar ON ar.id = a.artist_id "
            + "WHERE ci.user_id = ? AND p.status = ? "
            + "AND NOT EXISTS (SELECT 1 FROM inquiries i WHERE i.buyer_id = ci.user_id "
            + "AND i.post_id = ci.post_id AND i.status IN (%s)) ";

    private static final String FILTERED_SELECT = "SELECT p.id AS post_id, s.id AS seller_id, "
            + "s.username AS seller_username, a.title AS album_title, ar.name AS artist_name, "
            + "a.release_year AS album_release_year, COALESCE(p.image_id, a.cover_image_id) AS post_image_id, "
            + "p.price AS post_price " + FILTERED_FROM;

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // Un album sin portada trae NULL: getLong devuelve 0, hay que consultar wasNull.
    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }

    @Autowired
    public CartItemJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        // added_at queda afuera: lo pone el DEFAULT de la base.
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("cart_items")
                .usingColumns("user_id", "post_id");
    }

    // execute y no executeAndReturnKey: la clave es (user_id, post_id), no hay id generado.
    @Override
    public boolean add(final long userId, final long postId) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("post_id", postId);
        try {
            return jdbcInsert.execute(parameters) == 1;
        } catch (final DuplicateKeyException e) {
            return false;
        }
    }

    @Override
    public boolean remove(final long userId, final long postId) {
        return jdbcTemplate.update("DELETE FROM cart_items WHERE user_id = ? AND post_id = ?",
                userId, postId) == 1;
    }

    @Override
    public int removeAll(final long userId, final Collection<Long> postIds) {
        if (postIds.isEmpty()) {
            return 0;
        }
        final List<Object> parameters = new ArrayList<>();
        parameters.add(userId);
        parameters.addAll(postIds);
        return jdbcTemplate.update("DELETE FROM cart_items WHERE user_id = ? AND post_id IN ("
                + placeholders(postIds.size()) + ")", parameters.toArray());
    }

    @Override
    public boolean contains(final long userId, final long postId) {
        return !jdbcTemplate.queryForList("SELECT post_id FROM cart_items WHERE user_id = ? AND post_id = ?",
                Long.class, userId, postId).isEmpty();
    }

    @Override
    public List<CartItem> findByUserId(final long userId, final PostStatus postStatus,
                                       final Collection<InquiryStatus> excludedInquiryStatuses) {
        return List.copyOf(jdbcTemplate.query(
                filtered(FILTERED_SELECT, excludedInquiryStatuses) + "ORDER BY s.username, ci.added_at, p.id",
                ROW_MAPPER, filterParameters(userId, postStatus, excludedInquiryStatuses)));
    }

    @Override
    public int countByUserId(final long userId, final PostStatus postStatus,
                             final Collection<InquiryStatus> excludedInquiryStatuses) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) " + filtered(FILTERED_FROM, excludedInquiryStatuses),
                Integer.class, filterParameters(userId, postStatus, excludedInquiryStatuses));
    }

    // Sin estados que excluir, el IN queda con un valor que ninguna Consulta tiene.
    private static String filtered(final String sql, final Collection<InquiryStatus> excludedInquiryStatuses) {
        return String.format(sql, excludedInquiryStatuses.isEmpty() ? "NULL"
                : placeholders(excludedInquiryStatuses.size()));
    }

    private static Object[] filterParameters(final long userId, final PostStatus postStatus,
                                             final Collection<InquiryStatus> excludedInquiryStatuses) {
        final List<Object> parameters = new ArrayList<>();
        parameters.add(userId);
        parameters.add(postStatus.name());
        excludedInquiryStatuses.forEach(status -> parameters.add(status.name()));
        return parameters.toArray();
    }

    private static String placeholders(final int count) {
        return String.join(", ", Collections.nCopies(count, "?"));
    }
}
```
