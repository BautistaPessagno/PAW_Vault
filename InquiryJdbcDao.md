---
title: "InquiryJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java"]
---

# InquiryJdbcDao

Inserts PENDING inquiries, loads a compact Inquiry, and joins users/posts/albums/artists for inbox summaries ordered by created_at DESC, id DESC. Accept/reject updates require PENDING; competitor rejection excludes the accepted inquiry ID.

## Connections

Project types referenced: [[Inquiry]], [[InquiryDao]], [[InquiryStatus]], [[InquirySummary]], [[PostStatus]].

Referenced by: none.

## Exact source

[persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java, lines 1–112](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>)

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
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class InquiryJdbcDao implements InquiryDao {

    private static final RowMapper<Inquiry> ROW_MAPPER = (resultSet, rowNum) -> new Inquiry(
            resultSet.getLong("inquiry_id"),
            resultSet.getLong("inquiry_post_id"),
            resultSet.getLong("inquiry_buyer_id"),
            resultSet.getString("inquiry_message")
    );

    private static final String SELECT = "SELECT id AS inquiry_id, post_id AS inquiry_post_id, "
            + "buyer_id AS inquiry_buyer_id, message AS inquiry_message FROM inquiries ";

    private static final RowMapper<InquirySummary> SUMMARY_ROW_MAPPER = (resultSet, rowNum) -> new InquirySummary(
            resultSet.getLong("inquiry_id"),
            resultSet.getString("buyer_username"),
            resultSet.getString("seller_username"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getString("inquiry_message"),
            InquiryStatus.valueOf(resultSet.getString("inquiry_status")),
            PostStatus.valueOf(resultSet.getString("post_status"))
    );

    private static final String SUMMARY_SELECT = "SELECT i.id AS inquiry_id, "
            + "buyer.username AS buyer_username, seller.username AS seller_username, "
            + "a.title AS album_title, ar.name AS artist_name, i.message AS inquiry_message, "
            + "i.status AS inquiry_status, p.status AS post_status "
            + "FROM inquiries i JOIN posts p ON p.id = i.post_id "
            + "JOIN users buyer ON buyer.id = i.buyer_id JOIN users seller ON seller.id = p.user_id "
            + "JOIN albums a ON a.id = p.album_id JOIN artists ar ON ar.id = a.artist_id ";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

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
        return new Inquiry(id.longValue(), postId, buyerId, message);
    }

    @Override
    public Optional<Inquiry> findById(final long id) {
        return jdbcTemplate.query(SELECT + "WHERE id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public List<InquirySummary> findByBuyerId(final long buyerId) {
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT
                + "WHERE i.buyer_id = ? ORDER BY i.created_at DESC, i.id DESC", SUMMARY_ROW_MAPPER, buyerId));
    }

    @Override
    public List<InquirySummary> findBySellerId(final long sellerId) {
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT
                + "WHERE p.user_id = ? ORDER BY i.created_at DESC, i.id DESC", SUMMARY_ROW_MAPPER, sellerId));
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

    @Override
    public int rejectOtherPending(final long postId, final long acceptedInquiryId) {
        return jdbcTemplate.update("UPDATE inquiries SET status = ? WHERE post_id = ? AND id <> ? AND status = ?",
                InquiryStatus.REJECTED.name(), postId, acceptedInquiryId, InquiryStatus.PENDING.name());
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
