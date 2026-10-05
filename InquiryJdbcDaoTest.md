---
title: "InquiryJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java"]
---

# InquiryJdbcDaoTest

Tests de `InquiryJdbcDao` en `persistence`: 54 casos declarados. Cubre: bandejas agrupadas y paginadas (incluidos posts eliminados), filtro por estado (grupos mixtos, sin coincidencias, conteo de grupos) y conteo por estado, guardas de estado, `startSale` con precio fijado, precio actual mientras está pendiente, avatares de las partes, comprobante, consultas abiertas, alta en lote y desenganche. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `INQUIRIES_TABLE`, `ALL_STATUSES`, `inquiryDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `ids`.

Casos declarados: 54.

- `testStartSaleWhenSaleAlreadyStartedReturnsFalseAndPreservesPrice`
- `testStartSaleWhenInquiryDoesNotExistReturnsFalse`
- `testFindSummaryByIdWhenPendingPriceChangedReturnsCurrentPostPrice`
- `testStartSaleWhenInquiryIsPendingReturnsFrozenPriceAndAwaitingPayment`
- `testCreateWhenDataIsValidReturnsPendingInquiry`
- `testFindSummaryByIdWhenSellerHasAvatarReturnsAccountAppearance`
- `testCreateAllWhenBuyerAlreadyConsultedOneOfThePostsReturnsTheNewInquiries`
- `testFindByIdWhenInquiryExistsReturnsFixture`
- `testFindByIdWhenInquiryDoesNotExistReturnsEmpty`
- `testCreateWhenAddressIsGivenReturnsInquiryWithAddressId`
- `testFindBySellerIdWhenInquiryHasAddressReturnsSummaryWithAddress`
- `testFindBySellerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst`
- `testFindBySellerIdWhenSecondPageOfTwoGroupsReturnsRemainingGroup`
- `testFindBySellerIdWhenGroupHasSeveralInquiriesReturnsWholeGroupNewestFirst`
- `testFindBySellerIdWhenOffsetIsPastTheGroupsReturnsEmptyList`
- `testFindByBuyerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst`
- `testCountGroupsBySellerIdWhenSellerHasThreeGroupsReturnsThree`
- `testCountGroupsBySellerIdWhenSellerHasOneGroupWithTwoInquiriesReturnsOne`
- `testCountGroupsByBuyerIdWhenBuyerHasThreeGroupsReturnsThree`
- `testFindBySellerIdWhenFilteringPendingReturnsOnlyPendingInquiries`
- `testFindBySellerIdWhenGroupHasMixedStatusesReturnsOnlyMatchingInquiries`
- `testFindBySellerIdWhenNoGroupMatchesReturnsEmpty`
- `testCountGroupsBySellerIdWhenFilteringClosedReturnsOnlyGroupsWithClosedInquiries`
- `testFindByBuyerIdWhenFilteringInProgressReturnsAwaitingAndSubmitted`
- `testCountByStatusForSellerWhenSellerHasMixedStatusesReturnsCountPerStatus`
- `testCountByStatusForSellerWhenPostWasDeletedReturnsItsInquiries`
- `testCountByStatusForBuyerWhenBuyerHasNoInquiriesReturnsEmptyMap`
- `testCountByBuyerIdWhenBuyerHasInquiriesReturnsTotal`
- `testCountBySellerIdWhenSellerHasInquiriesReturnsTotalOfOwnedPosts`
- `testCountBySellerIdWhenSellerHasNoInquiriesReturnsZero`
- `testUpdateStatusWhenInquiryIsInExpectedStateReturnsTrue`
- `testUpdateStatusWhenInquiryIsInAnotherStateReturnsFalse`
- `testSaveReceiptWhenAwaitingPaymentReturnsTrueAndSubmitsPayment`
- `testSaveReceiptWhenPaymentWasAlreadySubmittedReturnsFalse`
- `testFindReceiptWhenReceiptWasUploadedReturnsFile`
- `testFindReceiptWhenNothingWasUploadedReturnsEmpty`
- `testFindPartiesByIdWhenPostWasDeletedReturnsStoredSeller`
- `testFindPartiesByIdWhenInquiryDoesNotExistReturnsEmpty`
- `testHasOpenSalesBySellerIdWhenSellerHasReservedPostsReturnsTrue`
- `testHasOpenSalesBySellerIdWhenSellerOnlyHasClosedOrPendingInquiriesReturnsFalse`
- `testFindSummaryByIdWhenInquiryPredatesTheStoredPriceReturnsCurrentPostPrice`
- `testFindSummaryByIdWhenSaleIsOpenReturnsPartiesPriceAtInquiryAndPaymentInfo`
- `testFindSummaryByIdWhenConversationHasRepliesReturnsLastMessage`
- `testFindSummaryByIdWhenConversationIsEmptyReturnsNullLastMessage`
- `testFindBySellerIdWhenConversationHasSeveralMessagesReturnsOneRowPerInquiry`
- `testFindOpenIdByPostAndBuyerWhenInquiryIsPendingReturnsItsId`
- `testFindOpenIdByPostAndBuyerWhenInquiryWasRejectedReturnsEmpty`
- `testFindPostIdsWithOpenInquiryWhenOneWasRejectedReturnsOnlyPendingPosts`
- `testFindPostIdsWithOpenInquiryWhenSalesAreInProgressReturnsTheirPosts`
- `testFindPendingByPostIdWhenPostHasWaitingInquiryReturnsOnlyPendingOnes`
- `testRejectOtherPendingWhenPostHasCompetitorsReturnsClosedCount`
- `testRejectOtherPendingWhenNoCompetitorRemainsReturnsZero`
- `testFindByBuyerIdWhenPostWasDeletedReturnsInquiryWithAlbumAndSeller`
- `testDetachFromPostWhenPostHasInquiriesReturnsCountAndKeepsAlbumAndSeller`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Inquiry]], [[InquiryDao]], [[InquiryParties]], [[InquiryStatus]], [[InquirySummary]], [[Message]], [[PostStatus]], [[Receipt]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java>), líneas 1–806.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.Message;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.Receipt;
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
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class InquiryJdbcDaoTest {

    private static final String INQUIRIES_TABLE = "inquiries";
    private static final List<InquiryStatus> ALL_STATUSES = List.of(InquiryStatus.values());

    @Autowired
    private InquiryDao inquiryDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @Test
    public void testStartSaleWhenSaleAlreadyStartedReturnsFalseAndPreservesPrice() {
        // 1. Arrange
        final long inquiryId = 8;

        // 2. Exercise
        final boolean changed = inquiryDao.startSale(inquiryId, 99000);
        final InquirySummary result = inquiryDao.findSummaryById(inquiryId).orElseThrow();

        // 3. Assert
        Assertions.assertFalse(changed);
        Assertions.assertEquals(InquiryStatus.AWAITING_PAYMENT, result.getStatus());
        Assertions.assertEquals(45000, result.getPrice());
    }

    @Test
    public void testStartSaleWhenInquiryDoesNotExistReturnsFalse() {
        // 1. Arrange

        // 2. Exercise
        final boolean changed = inquiryDao.startSale(999999, 42000);

        // 3. Assert
        Assertions.assertFalse(changed);
    }

    @Test
    public void testFindSummaryByIdWhenPendingPriceChangedReturnsCurrentPostPrice() {
        // 1. Arrange
        final long inquiryId = 3;

        // 2. Exercise
        final InquirySummary result = inquiryDao.findSummaryById(inquiryId).orElseThrow();

        // 3. Assert
        Assertions.assertEquals(30000, result.getPrice());
        Assertions.assertEquals(30000, inquiryDao.findByBuyerId(result.getBuyerId(), ALL_STATUSES, 20, 0).stream()
                .filter(summary -> summary.getId() == inquiryId).findFirst().orElseThrow().getPrice());
        Assertions.assertEquals(30000, inquiryDao.findBySellerId(result.getSellerId(), ALL_STATUSES, 20, 0).stream()
                .filter(summary -> summary.getId() == inquiryId).findFirst().orElseThrow().getPrice());
    }

    @Test
    public void testStartSaleWhenInquiryIsPendingReturnsFrozenPriceAndAwaitingPayment() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final boolean started = inquiryDao.startSale(inquiryId, 42000);
        final InquirySummary result = inquiryDao.findSummaryById(inquiryId).orElseThrow();

        // 3. Assert
        Assertions.assertTrue(started);
        Assertions.assertEquals(InquiryStatus.AWAITING_PAYMENT, result.getStatus());
        Assertions.assertEquals(42000, result.getPrice());
    }

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testCreateWhenDataIsValidReturnsPendingInquiry() {
        // 1. Arrange
        final long postId = 2;
        final long buyerId = 1;
        final long addressId = 1;

        // 2. Exercise
        final Inquiry result = inquiryDao.create(postId, buyerId, addressId, 38000);

        // 3. Assert
        Assertions.assertTrue(result.getId() > 0);
        Assertions.assertEquals(postId, result.getPostId());
        Assertions.assertEquals(buyerId, result.getBuyerId());
        Assertions.assertEquals(InquiryStatus.PENDING, result.getStatus());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.getId() + " AND post_id = " + postId + " AND buyer_id = " + buyerId
                        + " AND status = 'PENDING' AND price = 38000 AND created_at IS NOT NULL"));
        Assertions.assertEquals(24, JdbcTestUtils.countRowsInTable(jdbcTemplate, INQUIRIES_TABLE));
    }

    @Test
    public void testFindSummaryByIdWhenSellerHasAvatarReturnsAccountAppearance() {
        // 1. Arrange
        final long inquiryId = 1;

        // 2. Exercise
        final InquirySummary result = inquiryDao.findSummaryById(inquiryId).orElseThrow();

        // 3. Assert
        Assertions.assertEquals(2L, result.getSellerAvatarImageId());
        Assertions.assertNull(result.getBuyerAvatarImageId());
        Assertions.assertEquals(2L, result.withAddress(result.getAddress()).getSellerAvatarImageId());
    }

    @Test
    public void testCreateAllWhenBuyerAlreadyConsultedOneOfThePostsReturnsTheNewInquiries() {
        // 1. Arrange
        final long buyerId = 1;
        final long addressId = 1;
        final Map<Long, Integer> priceByPostId = Map.of(2L, 45000, 3L, 30000);

        // 2. Exercise
        final Map<Long, Inquiry> result = inquiryDao.createAll(buyerId, addressId, priceByPostId);

        // 3. Assert
        Assertions.assertEquals(Set.of(2L, 3L), result.keySet());
        // El comprador ya tenia la consulta 1 sobre el post 2: se devuelve la nueva, no esa.
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.get(2L).getId() + " AND id <> 1 AND post_id = 2 AND buyer_id = " + buyerId
                        + " AND status = 'PENDING' AND address_id = " + addressId + " AND price = 45000"
                        + " AND created_at IS NOT NULL"));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.get(3L).getId() + " AND post_id = 3 AND buyer_id = " + buyerId
                        + " AND status = 'PENDING' AND address_id = " + addressId + " AND price = 30000"
                        + " AND created_at IS NOT NULL"));
        Assertions.assertEquals(25, JdbcTestUtils.countRowsInTable(jdbcTemplate, INQUIRIES_TABLE));
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
    public void testCreateWhenAddressIsGivenReturnsInquiryWithAddressId() {
        // 1. Arrange
        final long postId = 3;
        final long buyerId = 1;
        final long addressId = 1;

        // 2. Exercise
        final Inquiry result = inquiryDao.create(postId, buyerId, addressId, 38000);

        // 3. Assert
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = " + result.getId() + " AND address_id = 1"));
    }

    @Test
    public void testFindBySellerIdWhenInquiryHasAddressReturnsSummaryWithAddress() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 5, 0);

        // 3. Assert
        final InquirySummary withAddress = result.stream().filter(i -> i.getId() == 1).findFirst().get();
        Assertions.assertEquals("Av. Madero", withAddress.getAddress().getStreet());
        final InquirySummary withoutAddress = result.stream().filter(i -> i.getId() == 2).findFirst().get();
        Assertions.assertNull(withoutAddress.getAddress());
    }

    @Test
    public void testFindBySellerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 2, 0);

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
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 2, 2);

        // 3. Assert
        Assertions.assertEquals(List.of(3L), ids(result));
    }

    @Test
    public void testFindBySellerIdWhenGroupHasSeveralInquiriesReturnsWholeGroupNewestFirst() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 1, 0);

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
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 2, 4);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByBuyerIdWhenFirstPageOfTwoGroupsReturnsNewestGroupsFirst() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId, ALL_STATUSES, 2, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(6L, 4L), ids(result));
        Assertions.assertEquals(PostStatus.SOLD, result.get(0).getPostStatus());
    }

    @Test
    public void testCountGroupsBySellerIdWhenSellerHasThreeGroupsReturnsThree() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final int result = inquiryDao.countGroupsBySellerId(sellerId, ALL_STATUSES);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testCountGroupsBySellerIdWhenSellerHasOneGroupWithTwoInquiriesReturnsOne() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countGroupsBySellerId(sellerId, ALL_STATUSES);

        // 3. Assert
        Assertions.assertEquals(1, result);
    }

    @Test
    public void testCountGroupsByBuyerIdWhenBuyerHasThreeGroupsReturnsThree() {
        // 1. Arrange
        final long buyerId = 2;

        // 2. Exercise
        final int result = inquiryDao.countGroupsByBuyerId(buyerId, ALL_STATUSES);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testFindBySellerIdWhenFilteringPendingReturnsOnlyPendingInquiries() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, List.of(InquiryStatus.PENDING), 5, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(4L, 3L), result.stream().map(InquirySummary::getId).toList());
    }

    @Test
    public void testFindBySellerIdWhenGroupHasMixedStatusesReturnsOnlyMatchingInquiries() {
        // 1. Arrange
        final long sellerId = 3;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, List.of(InquiryStatus.ACCEPTED), 5, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(5L), result.stream().map(InquirySummary::getId).toList());
    }

    @Test
    public void testFindBySellerIdWhenNoGroupMatchesReturnsEmpty() {
        // 1. Arrange
        final long sellerId = 3;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, List.of(InquiryStatus.PENDING), 5, 0);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testCountGroupsBySellerIdWhenFilteringClosedReturnsOnlyGroupsWithClosedInquiries() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final int result = inquiryDao.countGroupsBySellerId(sellerId,
                List.of(InquiryStatus.REJECTED, InquiryStatus.CANCELLED));

        // 3. Assert
        Assertions.assertEquals(1, result);
    }

    @Test
    public void testFindByBuyerIdWhenFilteringInProgressReturnsAwaitingAndSubmitted() {
        // 1. Arrange
        final long buyerId = 5;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId,
                List.of(InquiryStatus.AWAITING_PAYMENT, InquiryStatus.PAYMENT_SUBMITTED), 5, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(9L, 8L), result.stream().map(InquirySummary::getId).toList());
    }

    @Test
    public void testCountByStatusForSellerWhenSellerHasMixedStatusesReturnsCountPerStatus() {
        // 1. Arrange
        final long sellerId = 4;

        // 2. Exercise
        final Map<InquiryStatus, Integer> result = inquiryDao.countByStatusForSeller(sellerId);

        // 3. Assert
        Assertions.assertEquals(Map.of(InquiryStatus.PENDING, 1, InquiryStatus.AWAITING_PAYMENT, 1,
                InquiryStatus.PAYMENT_SUBMITTED, 1), result);
    }

    @Test
    public void testCountByStatusForSellerWhenPostWasDeletedReturnsItsInquiries() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final Map<InquiryStatus, Integer> result = inquiryDao.countByStatusForSeller(sellerId);

        // 3. Assert
        Assertions.assertEquals(Map.of(InquiryStatus.PENDING, 2, InquiryStatus.REJECTED, 1), result);
    }

    @Test
    public void testCountByStatusForBuyerWhenBuyerHasNoInquiriesReturnsEmptyMap() {
        // 1. Arrange
        final long buyerId = 4;

        // 2. Exercise
        final Map<InquiryStatus, Integer> result = inquiryDao.countByStatusForBuyer(buyerId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
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
    public void testUpdateStatusWhenInquiryIsInExpectedStateReturnsTrue() {
        // 1. Arrange
        final long pendingId = 1;

        // 2. Exercise
        final boolean result = inquiryDao.updateStatus(pendingId, InquiryStatus.PENDING, InquiryStatus.AWAITING_PAYMENT);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = 1 AND status = 'AWAITING_PAYMENT'"));
    }

    @Test
    public void testUpdateStatusWhenInquiryIsInAnotherStateReturnsFalse() {
        // 1. Arrange
        final long rejectedId = 6;

        // 2. Exercise
        final boolean result = inquiryDao.updateStatus(rejectedId, InquiryStatus.PENDING, InquiryStatus.REJECTED);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = 6 AND status = 'REJECTED'"));
    }

    @Test
    public void testSaveReceiptWhenAwaitingPaymentReturnsTrueAndSubmitsPayment() {
        // 1. Arrange
        final long awaitingId = 8;

        // 2. Exercise
        final boolean result = inquiryDao.saveReceipt(awaitingId, "image/png", new byte[]{1, 2, 3});

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = 8 AND status = 'PAYMENT_SUBMITTED' AND receipt_content_type = 'image/png'"
                        + " AND receipt_uploaded_at IS NOT NULL"));
    }

    @Test
    public void testSaveReceiptWhenPaymentWasAlreadySubmittedReturnsFalse() {
        // 1. Arrange
        final long submittedId = 9;

        // 2. Exercise
        final boolean result = inquiryDao.saveReceipt(submittedId, "image/png", new byte[]{1, 2, 3});

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, INQUIRIES_TABLE,
                "id = 9 AND receipt_content_type = 'application/pdf'"));
    }

    @Test
    public void testFindReceiptWhenReceiptWasUploadedReturnsFile() {
        // 1. Arrange
        final long submittedId = 9;

        // 2. Exercise
        final Optional<Receipt> result = inquiryDao.findReceipt(submittedId);

        // 3. Assert
        Assertions.assertEquals("application/pdf", result.get().getContentType());
        Assertions.assertArrayEquals(new byte[]{0x25, 0x50, 0x44, 0x46, 0x2D}, result.get().getData());
    }

    @Test
    public void testFindReceiptWhenNothingWasUploadedReturnsEmpty() {
        // 1. Arrange
        final long awaitingId = 8;

        // 2. Exercise
        final Optional<Receipt> result = inquiryDao.findReceipt(awaitingId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindPartiesByIdWhenPostWasDeletedReturnsStoredSeller() {
        // 1. Arrange
        final long detachedId = 7;

        // 2. Exercise
        final Optional<InquiryParties> result = inquiryDao.findPartiesById(detachedId);

        // 3. Assert
        Assertions.assertEquals(3L, result.get().getBuyerId());
        Assertions.assertEquals(1L, result.get().getSellerId());
    }

    @Test
    public void testFindPartiesByIdWhenInquiryDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingId = 999;

        // 2. Exercise
        final Optional<InquiryParties> result = inquiryDao.findPartiesById(missingId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testHasOpenSalesBySellerIdWhenSellerHasReservedPostsReturnsTrue() {
        // 1. Arrange
        final long sellerId = 4;

        // 2. Exercise
        final boolean result = inquiryDao.hasOpenSalesBySellerId(sellerId);

        // 3. Assert
        Assertions.assertTrue(result);
    }

    @Test
    public void testHasOpenSalesBySellerIdWhenSellerOnlyHasClosedOrPendingInquiriesReturnsFalse() {
        // 1. Arrange
        final long sellerId = 1;

        // 2. Exercise
        final boolean result = inquiryDao.hasOpenSalesBySellerId(sellerId);

        // 3. Assert
        Assertions.assertFalse(result);
    }

    @Test
    public void testFindSummaryByIdWhenInquiryPredatesTheStoredPriceReturnsCurrentPostPrice() {
        // 1. Arrange
        final long submittedId = 9;

        // 2. Exercise
        final Optional<InquirySummary> result = inquiryDao.findSummaryById(submittedId);

        // 3. Assert
        Assertions.assertEquals(40000, result.get().getPrice());
    }

    @Test
    public void testFindSummaryByIdWhenSaleIsOpenReturnsPartiesPriceAtInquiryAndPaymentInfo() {
        // 1. Arrange
        final long awaitingId = 8;

        // 2. Exercise
        final Optional<InquirySummary> result = inquiryDao.findSummaryById(awaitingId);

        // 3. Assert
        final InquirySummary summary = result.get();
        Assertions.assertEquals(5L, summary.getBuyerId());
        Assertions.assertEquals(4L, summary.getSellerId());
        Assertions.assertEquals("comprador@example.com", summary.getBuyerEmail());
        Assertions.assertEquals("en", summary.getBuyerLocale());
        Assertions.assertEquals(45000, summary.getPrice());
        Assertions.assertNull(summary.getSellerPaymentInfo().getCbu());
        Assertions.assertEquals("vende.discos", summary.getSellerPaymentInfo().getAlias());
        Assertions.assertEquals("Belgrano", summary.getAddress().getStreet());
        Assertions.assertFalse(summary.isHasReceipt());
        Assertions.assertEquals(InquiryStatus.AWAITING_PAYMENT, summary.getStatus());
    }

    @Test
    public void testFindSummaryByIdWhenConversationHasRepliesReturnsLastMessage() {
        // 1. Arrange
        final long repliedId = 1;

        // 2. Exercise
        final Optional<InquirySummary> result = inquiryDao.findSummaryById(repliedId);

        // 3. Assert
        final Message last = result.get().getLastMessage();
        Assertions.assertEquals(2L, last.getId());
        Assertions.assertEquals(2L, last.getSenderId());
        Assertions.assertEquals("Puedo dejarlo en 42000.", last.getBody());
    }

    @Test
    public void testFindSummaryByIdWhenConversationIsEmptyReturnsNullLastMessage() {
        // 1. Arrange
        final long emptyConversationId = 2;

        // 2. Exercise
        final Optional<InquirySummary> result = inquiryDao.findSummaryById(emptyConversationId);

        // 3. Assert
        Assertions.assertNull(result.get().getLastMessage());
    }

    @Test
    public void testFindBySellerIdWhenConversationHasSeveralMessagesReturnsOneRowPerInquiry() {
        // 1. Arrange
        final long sellerId = 2;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findBySellerId(sellerId, ALL_STATUSES, 5, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(2L, 1L), ids(result));
        Assertions.assertNull(result.get(0).getLastMessage());
        Assertions.assertEquals(2L, result.get(1).getLastMessage().getId());
    }

    @Test
    public void testFindOpenIdByPostAndBuyerWhenInquiryIsPendingReturnsItsId() {
        // 1. Arrange
        final long postId = 2;
        final long buyerId = 1;

        // 2. Exercise
        final Optional<Long> result = inquiryDao.findOpenIdByPostAndBuyer(postId, buyerId);

        // 3. Assert
        Assertions.assertEquals(Optional.of(1L), result);
    }

    @Test
    public void testFindOpenIdByPostAndBuyerWhenInquiryWasRejectedReturnsEmpty() {
        // 1. Arrange
        final long postId = 4;
        final long buyerId = 2;

        // 2. Exercise
        final Optional<Long> result = inquiryDao.findOpenIdByPostAndBuyer(postId, buyerId);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindPostIdsWithOpenInquiryWhenOneWasRejectedReturnsOnlyPendingPosts() {
        // 1. Arrange
        final long buyerId = 2;
        final List<Long> postIds = List.of(1L, 2L, 3L, 4L);

        // 2. Exercise
        final Set<Long> result = inquiryDao.findPostIdsWithOpenInquiry(buyerId, postIds);

        // 3. Assert
        Assertions.assertEquals(Set.of(1L, 3L), result);
    }

    @Test
    public void testFindPostIdsWithOpenInquiryWhenSalesAreInProgressReturnsTheirPosts() {
        // 1. Arrange
        final long buyerId = 5;
        final List<Long> postIds = List.of(1L, 6L, 7L);

        // 2. Exercise
        final Set<Long> result = inquiryDao.findPostIdsWithOpenInquiry(buyerId, postIds);

        // 3. Assert
        Assertions.assertEquals(Set.of(6L, 7L), result);
    }

    @Test
    public void testFindPendingByPostIdWhenPostHasWaitingInquiryReturnsOnlyPendingOnes() {
        // 1. Arrange
        final long reservedPostId = 6;

        // 2. Exercise
        final List<InquirySummary> result = inquiryDao.findPendingByPostId(reservedPostId);

        // 3. Assert
        Assertions.assertEquals(List.of(10L), result.stream().map(InquirySummary::getId).toList());
        Assertions.assertEquals("esperando@example.com", result.get(0).getBuyerEmail());
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
        final List<InquirySummary> result = inquiryDao.findByBuyerId(buyerId, ALL_STATUSES, 2, 0);

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
