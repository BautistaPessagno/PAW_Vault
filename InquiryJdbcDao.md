---
title: "InquiryJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java"]
---

# InquiryJdbcDao

Consultas con Spring JDBC. El resumen sale de un `JOIN` que cubre posts eliminados con `COALESCE` y trae el último mensaje con una subconsulta agregada. La bandeja se pagina por grupo en dos sentencias. Las transiciones y el comprobante son `UPDATE` con guarda de estado. `createAll` inserta en lote.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SELECT`, `SUMMARY_ROW_MAPPER`, `PARTIES_ROW_MAPPER`, `RECEIPT_ROW_MAPPER`, `GROUP_KEY`, `GROUP_FROM`, `SUMMARY_SELECT`, `SELLER_WHERE`, `BUYER_WHERE`, `OPEN_STATUS_NAMES`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `readNullableLong`, `readNullableInt`, `readNullablePostStatus`, `readAddress`, `readLastMessage`, `create`, `createAll`, `findById`, `findByIdForUpdate`, `findOpenIdByPostAndBuyer`, `findPostIdsWithOpenInquiry`, `placeholders`, `findByBuyerId`, `findBySellerId`, `countGroupsByBuyerId`, `countGroupsBySellerId`, `findGroupPage`, `updateStatus`, `saveReceipt`, `findReceipt`, `findSummaryById`, `findPartiesById`, `hasOpenSalesBySellerId`, `findPendingByPostId`, `countByBuyerId`, `countBySellerId`, `rejectOtherPending`, `detachFromPost`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressJdbcDao]], [[Inquiry]], [[InquiryDao]], [[InquiryParties]], [[InquiryStatus]], [[InquirySummary]], [[Message]], [[MessageJdbcDao]], [[PaymentInfo]], [[PostStatus]], [[Receipt]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>), líneas 1–373.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.Message;
import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.Receipt;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.SqlParameterSourceUtils;
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
import java.util.Optional;
import java.util.Set;

@Repository
public class InquiryJdbcDao implements InquiryDao {

    private static final RowMapper<Inquiry> ROW_MAPPER = (resultSet, rowNum) -> new Inquiry(
            resultSet.getLong("inquiry_id"),
            readNullableLong(resultSet, "inquiry_post_id"),
            resultSet.getLong("inquiry_buyer_id"),
            InquiryStatus.valueOf(resultSet.getString("inquiry_status"))
    );

    private static final String SELECT = "SELECT id AS inquiry_id, post_id AS inquiry_post_id, "
            + "buyer_id AS inquiry_buyer_id, status AS inquiry_status FROM inquiries ";

    private static final RowMapper<InquirySummary> SUMMARY_ROW_MAPPER = (resultSet, rowNum) -> new InquirySummary(
            resultSet.getLong("inquiry_id"),
            readNullableLong(resultSet, "post_id"),
            resultSet.getLong("album_id"),
            resultSet.getLong("buyer_id"),
            resultSet.getLong("seller_id"),
            resultSet.getString("buyer_username"),
            resultSet.getString("buyer_email"),
            resultSet.getString("buyer_locale"),
            resultSet.getString("seller_username"),
            new PaymentInfo(resultSet.getString("seller_cbu"), resultSet.getString("seller_alias")),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            readNullableLong(resultSet, "post_image_id"),
            readNullableInt(resultSet, "inquiry_price"),
            readLastMessage(resultSet, rowNum),
            InquiryStatus.valueOf(resultSet.getString("inquiry_status")),
            readNullablePostStatus(resultSet, "post_status"),
            readAddress(resultSet, rowNum),
            resultSet.getBoolean("has_receipt")
    );

    private static final RowMapper<InquiryParties> PARTIES_ROW_MAPPER = (resultSet, rowNum) ->
            new InquiryParties(resultSet.getLong("buyer_id"), resultSet.getLong("seller_id"));

    private static final RowMapper<Receipt> RECEIPT_ROW_MAPPER = (resultSet, rowNum) ->
            new Receipt(resultSet.getString("receipt_content_type"), resultSet.getBytes("receipt_data"));

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
            + "a.title AS album_title, ar.name AS artist_name, "
            + "COALESCE(p.image_id, a.cover_image_id) AS post_image_id, "
            + "i.status AS inquiry_status, p.status AS post_status, "
            + "i.buyer_id AS buyer_id, buyer.email AS buyer_email, buyer.preferred_locale AS buyer_locale, "
            + "seller.cbu AS seller_cbu, seller.alias AS seller_alias, COALESCE(i.price, p.price) AS inquiry_price, "
            + "CASE WHEN i.receipt_uploaded_at IS NULL THEN FALSE ELSE TRUE END AS has_receipt, "
            + AddressJdbcDao.columns("ad") + ", " + MessageJdbcDao.columns("m") + " "
            + GROUP_FROM
            + "JOIN users buyer ON buyer.id = i.buyer_id "
            + "JOIN users seller ON seller.id = COALESCE(p.user_id, i.seller_id) "
            + "JOIN albums a ON a.id = COALESCE(p.album_id, i.album_id) JOIN artists ar ON ar.id = a.artist_id "
            + "LEFT JOIN addresses ad ON ad.id = i.address_id "
            // El ultimo Mensaje de cada Consulta, sin N+1: la subquery agregada se resuelve una vez
            // por sentencia y cada Consulta matchea a lo sumo una fila, asi el JOIN no duplica.
            + "LEFT JOIN (SELECT inquiry_id, MAX(id) AS last_id FROM inquiry_messages GROUP BY inquiry_id) lm "
            + "ON lm.inquiry_id = i.id "
            + "LEFT JOIN inquiry_messages m ON m.id = lm.last_id ";

    private static final String SELLER_WHERE = "WHERE COALESCE(p.user_id, i.seller_id) = ? ";

    private static final String BUYER_WHERE = "WHERE i.buyer_id = ? ";

    private static final List<String> OPEN_STATUS_NAMES = InquiryStatus.OPEN_STATUSES.stream()
            .map(InquiryStatus::name)
            .toList();

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    // Los albums sin portada propia quedan en NULL: getLong devuelve 0, hay que consultar wasNull.
    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }

    // Las publicaciones eliminadas no tienen precio propio: getInt devuelve 0, hay que consultar wasNull.
    private static Integer readNullableInt(final ResultSet resultSet, final String column) throws SQLException {
        final int value = resultSet.getInt(column);
        return resultSet.wasNull() ? null : value;
    }

    private static PostStatus readNullablePostStatus(final ResultSet resultSet, final String column)
            throws SQLException {
        final String status = resultSet.getString(column);
        return status == null ? null : PostStatus.valueOf(status);
    }

    // La direccion llega por LEFT JOIN: las consultas sin direccion traen sus columnas en NULL.
    private static Address readAddress(final ResultSet resultSet, final int rowNum) throws SQLException {
        resultSet.getLong("address_id");
        return resultSet.wasNull() ? null : AddressJdbcDao.ROW_MAPPER.mapRow(resultSet, rowNum);
    }

    // Igual que la direccion: una Conversacion vacia trae las columnas del Mensaje en NULL.
    private static Message readLastMessage(final ResultSet resultSet, final int rowNum) throws SQLException {
        resultSet.getLong("message_id");
        return resultSet.wasNull() ? null : MessageJdbcDao.ROW_MAPPER.mapRow(resultSet, rowNum);
    }

    @Autowired
    public InquiryJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("inquiries")
                .usingColumns("post_id", "buyer_id", "status", "address_id", "price")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public Inquiry create(final long postId, final long buyerId, final long addressId, final int price) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("post_id", postId);
        parameters.put("buyer_id", buyerId);
        parameters.put("status", InquiryStatus.PENDING.name());
        parameters.put("address_id", addressId);
        parameters.put("price", price);

        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Inquiry(id.longValue(), postId, buyerId, InquiryStatus.PENDING);
    }

    /*
     * Un batch para los inserts y una consulta para recuperar los ids, que executeBatch no
     * devuelve: la de mayor id por Post es la recien creada, porque los ids crecen y el que llama
     * tiene los Posts bloqueados.
     */
    @Override
    public Map<Long, Inquiry> createAll(final long buyerId, final long addressId,
                                        final Map<Long, Integer> priceByPostId) {
        if (priceByPostId.isEmpty()) {
            return Map.of();
        }
        final List<Map<String, Object>> rows = new ArrayList<>();
        priceByPostId.forEach((postId, price) -> {
            final Map<String, Object> row = new HashMap<>();
            row.put("post_id", postId);
            row.put("buyer_id", buyerId);
            row.put("status", InquiryStatus.PENDING.name());
            row.put("address_id", addressId);
            row.put("price", price);
            rows.add(row);
        });
        jdbcInsert.executeBatch(SqlParameterSourceUtils.createBatch(rows));

        final List<Object> parameters = new ArrayList<>();
        parameters.add(buyerId);
        parameters.addAll(priceByPostId.keySet());
        final Map<Long, Inquiry> created = new HashMap<>();
        jdbcTemplate.query("SELECT post_id, MAX(id) AS id FROM inquiries WHERE buyer_id = ? AND post_id IN ("
                        + placeholders(priceByPostId.size()) + ") GROUP BY post_id",
                (RowCallbackHandler) resultSet -> created.put(resultSet.getLong("post_id"),
                        new Inquiry(resultSet.getLong("id"), resultSet.getLong("post_id"), buyerId,
                                InquiryStatus.PENDING)),
                parameters.toArray());
        return Map.copyOf(created);
    }

    @Override
    public Optional<Inquiry> findById(final long id) {
        return jdbcTemplate.query(SELECT + "WHERE id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public Optional<Inquiry> findByIdForUpdate(final long id) {
        return jdbcTemplate.query(SELECT + "WHERE id = ? FOR UPDATE", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public Optional<Long> findOpenIdByPostAndBuyer(final long postId, final long buyerId) {
        final List<Object> parameters = new ArrayList<>();
        parameters.add(postId);
        parameters.add(buyerId);
        parameters.addAll(OPEN_STATUS_NAMES);
        return jdbcTemplate.queryForList("SELECT id FROM inquiries WHERE post_id = ? AND buyer_id = ? "
                        + "AND status IN (" + placeholders(OPEN_STATUS_NAMES.size()) + ") ORDER BY id DESC LIMIT 1",
                Long.class, parameters.toArray()).stream().findFirst();
    }

    @Override
    public Set<Long> findPostIdsWithOpenInquiry(final long buyerId, final Collection<Long> postIds) {
        if (postIds.isEmpty()) {
            return Set.of();
        }
        final List<Object> parameters = new ArrayList<>();
        parameters.add(buyerId);
        parameters.addAll(OPEN_STATUS_NAMES);
        parameters.addAll(postIds);
        return Set.copyOf(jdbcTemplate.queryForList("SELECT DISTINCT post_id FROM inquiries "
                        + "WHERE buyer_id = ? AND status IN (" + placeholders(OPEN_STATUS_NAMES.size())
                        + ") AND post_id IN (" + placeholders(postIds.size()) + ")",
                Long.class, parameters.toArray()));
    }

    private static String placeholders(final int count) {
        return String.join(", ", Collections.nCopies(count, "?"));
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
    public boolean updateStatus(final long id, final InquiryStatus from, final InquiryStatus to) {
        return jdbcTemplate.update("UPDATE inquiries SET status = ? WHERE id = ? AND status = ?",
                to.name(), id, from.name()) == 1;
    }

    // Guardar el comprobante y pasar a revision es una sola sentencia con su guarda: un
    // segundo envio, o uno despues de cancelar, no encuentra la fila en AWAITING_PAYMENT.
    @Override
    public boolean saveReceipt(final long id, final String contentType, final byte[] data) {
        return jdbcTemplate.update("UPDATE inquiries SET receipt_content_type = ?, receipt_data = ?, "
                        + "receipt_uploaded_at = CURRENT_TIMESTAMP, status = ? WHERE id = ? AND status = ?",
                contentType, data, InquiryStatus.PAYMENT_SUBMITTED.name(), id,
                InquiryStatus.AWAITING_PAYMENT.name()) == 1;
    }

    @Override
    public Optional<Receipt> findReceipt(final long id) {
        return jdbcTemplate.query("SELECT receipt_content_type, receipt_data FROM inquiries "
                + "WHERE id = ? AND receipt_data IS NOT NULL", RECEIPT_ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public Optional<InquirySummary> findSummaryById(final long id) {
        return jdbcTemplate.query(SUMMARY_SELECT + "WHERE i.id = ?", SUMMARY_ROW_MAPPER, id).stream().findFirst();
    }

    // Solo las dos partes: lo que necesitan los chequeos de acceso, sin los JOIN del summary.
    @Override
    public Optional<InquiryParties> findPartiesById(final long id) {
        return jdbcTemplate.query("SELECT i.buyer_id AS buyer_id, COALESCE(p.user_id, i.seller_id) AS seller_id "
                + GROUP_FROM + "WHERE i.id = ?", PARTIES_ROW_MAPPER, id).stream().findFirst();
    }

    // Venta abierta: aceptada y todavia sin confirmar ni cancelar.
    @Override
    public boolean hasOpenSalesBySellerId(final long sellerId) {
        final Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) " + GROUP_FROM + SELLER_WHERE
                        + "AND i.status IN (?, ?)", Integer.class, sellerId,
                InquiryStatus.AWAITING_PAYMENT.name(), InquiryStatus.PAYMENT_SUBMITTED.name());
        return count != null && count > 0;
    }

    @Override
    public List<InquirySummary> findPendingByPostId(final long postId) {
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + "WHERE i.post_id = ? AND i.status = ?",
                SUMMARY_ROW_MAPPER, postId, InquiryStatus.PENDING.name()));
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
