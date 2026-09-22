---
title: "InquiryJdbcDaoTest"
categories: ["Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java"]
---

# InquiryJdbcDaoTest

HSQLDB DAO tests using the Spring test context and SQL fixtures. Source evidence for [[InquiryJdbcDao]]; no new Maven execution is claimed.

Test methods in this revision:

- `testCreateWhenDataIsValidReturnsPendingInquiry`
- `testFindByIdWhenInquiryExistsReturnsFixture`
- `testFindByIdWhenInquiryDoesNotExistReturnsEmpty`
- `testFindBySellerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst`
- `testFindBySellerIdWhenSecondPageOfTwoGroupsReturnsRemainingGroup`
- `testFindBySellerIdWhenGroupHasSeveralInquiriesReturnsWholeGroupNewestFirst`
- `testFindBySellerIdWhenOffsetIsPastTheGroupsReturnsEmptyList`
- `testFindByBuyerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst`
- `testCountGroupsBySellerIdWhenSellerHasThreeGroupsReturnsThree`
- `testCountGroupsBySellerIdWhenSellerHasOneGroupWithTwoInquiriesReturnsOne`
- `testCountGroupsByBuyerIdWhenBuyerHasThreeGroupsReturnsThree`
- `testCountByBuyerIdWhenBuyerHasInquiriesReturnsTotal`
- `testCountBySellerIdWhenSellerHasInquiriesReturnsTotalOfOwnedPosts`
- `testCountBySellerIdWhenSellerHasNoInquiriesReturnsZero`
- `testAcceptPendingWhenInquiryIsPendingReturnsTrueAndAcceptsIt`
- `testRejectPendingWhenInquiryIsPendingReturnsTrueAndRejectsIt`
- `testAcceptPendingWhenInquiryIsAlreadyClosedReturnsFalse`
- `testRejectPendingWhenInquiryIsAlreadyClosedReturnsFalse`
- `testRejectOtherPendingWhenPostHasCompetitorsReturnsClosedCount`
- `testRejectOtherPendingWhenNoCompetitorRemainsReturnsZero`
- `testFindByBuyerIdWhenPostWasDeletedReturnsInquiryWithAlbumAndSeller`
- `testDetachFromPostWhenPostHasInquiriesReturnsCountAndKeepsAlbumAndSeller`

## Connections

Project types referenced: [[Inquiry]], [[InquiryDao]], [[InquiryStatus]], [[InquirySummary]], [[PostStatus]], [[TestConfiguration]].

Referenced by: none.

## Exact source

[persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java, lines 1–363](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java>)

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
        Assertions.assertEquals(InquiryStatus.PENDING, result.getStatus());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.getId() + " AND post_id = " + postId + " AND buyer_id = " + buyerId
                        + " AND status = 'PENDING' AND created_at IS NOT NULL"));
        Assertions.assertEquals(8, JdbcTestUtils.countRowsInTable(jdbcTemplate, INQUIRIES_TABLE));
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
        Assertions.assertEquals(InquiryStatus.PENDING, result.get().getStatus());
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
    public void testFindBySellerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, 2, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(7L, 4L), ids(result));
        Assertions.assertNull(result.get(0).getPostId());
        Assertions.assertEquals(1L, result.get(1).getPostId());
    }

    @Test
    public void testFindBySellerIdWhenSecondPageOfTwoGroupsReturnsRemainingGroup() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, 2, 2);

        // 3. Assert
        Assertions.assertEquals(List.of(3L), ids(result));
    }

    @Test
    public void testFindBySellerIdWhenGroupHasSeveralInquiriesReturnsWholeGroupNewestFirst() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, 1, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(2L, 1L), ids(result));
        Assertions.assertEquals("legacy", result.get(0).getBuyerUsername());
        Assertions.assertEquals(InquiryStatus.PENDING, result.get(0).getStatus());
        Assertions.assertEquals("versus", result.get(0).getTitle());
        Assertions.assertEquals("illya kuryaki and the valderramas", result.get(0).getArtistName());
        Assertions.assertEquals("tgorganchian", result.get(0).getSellerUsername());
        Assertions.assertEquals(PostStatus.AVAILABLE, result.get(0).getPostStatus());
    }

    @Test
    public void testFindBySellerIdWhenOffsetIsPastTheGroupsReturnsEmptyList() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, 2, 4);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByBuyerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId, 2, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(6L, 4L), ids(result));
        Assertions.assertEquals(PostStatus.SOLD, result.get(0).getPostStatus());
    }

    @Test
    public void testCountGroupsBySellerIdWhenSellerHasThreeGroupsReturnsThree() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final int result = inquiryDao.countGroupsBySellerId(sellerId);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testCountGroupsBySellerIdWhenSellerHasOneGroupWithTwoInquiriesReturnsOne() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countGroupsBySellerId(sellerId);

        // 3. Assert
        Assertions.assertEquals(1, result);
    }

    @Test
    public void testCountGroupsByBuyerIdWhenBuyerHasThreeGroupsReturnsThree() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countGroupsByBuyerId(buyerId);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testCountByBuyerIdWhenBuyerHasInquiriesReturnsTotal() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countByBuyerId(buyerId);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testCountBySellerIdWhenSellerHasInquiriesReturnsTotalOfOwnedPosts() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countBySellerId(sellerId);

        // 3. Assert
        Assertions.assertEquals(2, result);
    }

    @Test
    public void testCountBySellerIdWhenSellerHasNoInquiriesReturnsZero() {
        // 1. Arrange
        final long missingSellerId = 999;

        // 2. Exercise
        final int result = inquiryDao.countBySellerId(missingSellerId);

        // 3. Assert
        Assertions.assertEquals(0, result);
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

    @Test
    public void testFindByBuyerIdWhenPostWasDeletedReturnsInquiryWithAlbumAndSeller() {
        // 1. Arrange
        final long buyerId = 3;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId, 2, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(7L, 2L), ids(result));
        Assertions.assertNull(result.get(0).getPostId());
        Assertions.assertNull(result.get(0).getPostStatus());
        Assertions.assertEquals("sold only album", result.get(0).getTitle());
        Assertions.assertEquals("sold only artist", result.get(0).getArtistName());
        Assertions.assertEquals("bpessagno", result.get(0).getSellerUsername());
        Assertions.assertEquals(3L, result.get(0).getAlbumId());
        Assertions.assertEquals(1L, result.get(0).getSellerId());
        Assertions.assertEquals(2L, result.get(1).getPostId());
    }

    @Test
    public void testDetachFromPostWhenPostHasInquiriesReturnsCountAndKeepsAlbumAndSeller() {
        // 1. Arrange
        final long postId = 2;

        // 2. Exercise
        final int detached = inquiryDao.detachFromPost(postId);

        // 3. Assert
        Assertions.assertEquals(2, detached);
        Assertions.assertEquals(2, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id IN (1, 2) AND post_id IS NULL AND album_id = 1 AND seller_id = 2 AND status = 'REJECTED'"));
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "post_id = " + postId));
    }

    private static List<Long> ids(final List<InquirySummary> inquiries) {
        return inquiries.stream().map(InquirySummary::getId).collect(Collectors.toList());
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
