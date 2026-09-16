---
title: "InquiryJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java"]
---

# InquiryJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[InquiryJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testCreateWhenDataIsValidReturnsPendingInquiry`
- `testFindByIdWhenInquiryExistsReturnsFixture`
- `testFindByIdWhenInquiryDoesNotExistReturnsEmpty`
- `testFindByBuyerIdWhenInquiriesExistReturnsNewestFirstWithPostData`
- `testFindBySellerIdWhenInquiriesExistReturnsOnlyOwnedPosts`
- `testAcceptPendingWhenInquiryIsPendingReturnsTrueAndAcceptsIt`
- `testRejectPendingWhenInquiryIsPendingReturnsTrueAndRejectsIt`
- `testAcceptPendingWhenInquiryIsAlreadyClosedReturnsFalse`
- `testRejectPendingWhenInquiryIsAlreadyClosedReturnsFalse`
- `testRejectOtherPendingWhenPostHasCompetitorsReturnsClosedCount`
- `testRejectOtherPendingWhenNoCompetitorRemainsReturnsZero`

## Connections

Project types referenced: [[Inquiry]], [[InquiryDao]], [[InquiryStatus]], [[InquirySummary]], [[PostStatus]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java, lines 1–214](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostStatus;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class InquiryJdbcDaoTest {

    private static final String INQUIRIES_TABLE = "inquiries";

    @Autowired
    private InquiryDao inquiryDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testCreateWhenDataIsValidReturnsPendingInquiry() {
        // 1. Arrange
        final long postId = 2;
        final long buyerId = 1;
        final String message = "Me interesa, gracias";

        // 2. Exercise
        final Inquiry result = inquiryDao.create(postId, buyerId, message);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(postId, result.getPostId());
        Assertions.assertEquals(buyerId, result.getBuyerId());
        Assertions.assertEquals(message, result.getMessage());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.getId() + " AND post_id = " + postId + " AND buyer_id = " + buyerId
                        + " AND status = 'PENDING' AND created_at IS NOT NULL"));
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, INQUIRIES_TABLE));
    }

    @Test
    public void testFindByIdWhenInquiryExistsReturnsFixture() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final Optional<Inquiry> result = inquiryDao.findById(inquiryId);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(2, result.get().getPostId());
        Assertions.assertEquals(1, result.get().getBuyerId());
        Assertions.assertEquals("¿Aceptarías una oferta?", result.get().getMessage());
    }

    @Test
    public void testFindByIdWhenInquiryDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<Inquiry> result = inquiryDao.findById(missingId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByBuyerIdWhenInquiriesExistReturnsNewestFirstWithPostData() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId);

        // 3. Assert
        Assertions.assertEquals(List.of(6L, 4L, 3L),
                result.stream().map(InquirySummary::getId).collect(Collectors.toList()));
        Assertions.assertEquals("cancion animal", result.get(0).getTitle());
        Assertions.assertEquals("legacy", result.get(0).getSellerUsername());
        Assertions.assertEquals(InquiryStatus.REJECTED, result.get(0).getStatus());
        Assertions.assertEquals(PostStatus.SOLD, result.get(0).getPostStatus());
        Assertions.assertEquals("versus", result.get(1).getTitle());
        Assertions.assertEquals("bpessagno", result.get(1).getSellerUsername());
    }

    @Test
    public void testFindBySellerIdWhenInquiriesExistReturnsOnlyOwnedPosts() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId);

        // 3. Assert
        Assertions.assertEquals(List.of(2L, 1L),
                result.stream().map(InquirySummary::getId).collect(Collectors.toList()));
        Assertions.assertEquals("legacy", result.get(0).getBuyerUsername());
        Assertions.assertEquals(InquiryStatus.PENDING, result.get(0).getStatus());
    }

    @Test
    public void testAcceptPendingWhenInquiryIsPendingReturnsTrueAndAcceptsIt() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final boolean accepted = inquiryDao.acceptPending(inquiryId);

        // 3. Assert
        Assertions.assertTrue(accepted);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + inquiryId + " AND status = 'ACCEPTED'"));
    }

    @Test
    public void testRejectPendingWhenInquiryIsPendingReturnsTrueAndRejectsIt() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final boolean rejected = inquiryDao.rejectPending(inquiryId);

        // 3. Assert
        Assertions.assertTrue(rejected);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + inquiryId + " AND status = 'REJECTED'"));
    }

    @Test
    public void testAcceptPendingWhenInquiryIsAlreadyClosedReturnsFalse() {
        // 1. Arrange
        final long rejectedInquiryId = 6;

        // 2. Exercise
        final boolean accepted = inquiryDao.acceptPending(rejectedInquiryId);

        // 3. Assert
        Assertions.assertFalse(accepted);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + rejectedInquiryId + " AND status = 'REJECTED'"));
    }

    @Test
    public void testRejectPendingWhenInquiryIsAlreadyClosedReturnsFalse() {
        // 1. Arrange
        final long acceptedInquiryId = 5;

        // 2. Exercise
        final boolean rejected = inquiryDao.rejectPending(acceptedInquiryId);

        // 3. Assert
        Assertions.assertFalse(rejected);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + acceptedInquiryId + " AND status = 'ACCEPTED'"));
    }

    @Test
    public void testRejectOtherPendingWhenPostHasCompetitorsReturnsClosedCount() {
        // 1. Arrange
        final long postId = 2;
        final long acceptedId = 1;

        // 2. Exercise
        final int rejected = inquiryDao.rejectOtherPending(postId, acceptedId);

        // 3. Assert
        Assertions.assertEquals(1, rejected);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = 2 AND status = 'REJECTED'"));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + acceptedId + " AND status = 'PENDING'"));
    }

    @Test
    public void testRejectOtherPendingWhenNoCompetitorRemainsReturnsZero() {
        // 1. Arrange
        final long acceptedId = 3;
        final long postId = 3;

        // 2. Exercise
        final int rejected = inquiryDao.rejectOtherPending(postId, acceptedId);

        // 3. Assert
        Assertions.assertEquals(0, rejected);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "post_id = " + postId + " AND status = 'PENDING'"));
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
