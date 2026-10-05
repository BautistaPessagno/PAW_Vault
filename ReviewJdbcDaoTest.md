---
title: "ReviewJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/ReviewJdbcDaoTest.java"]
---

# ReviewJdbcDaoTest

Tests de `ReviewJdbcDao` en `persistence`: 19 casos declarados. Cubre: alta, actualización que reactiva, desactivación, listado y estadísticas por rol, paginación con `OFFSET` y foto del autor. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `REVIEWS_TABLE`, `LIMIT`, `CONFIRMED_SALE_ID`, `BUYER_ID`, `BUYER_USERNAME`, `SELLER_ID`, `BUYER_REVIEW_ID`, `SELLER_REVIEW_ID`, `OTHER_INQUIRY_ID`, `OTHER_BUYER_ID`, `NEWEST_REVIEW_ID`, `REMOVED_REVIEW_ID`, `UNREVIEWED_INQUIRY_ID`, `UNREVIEWED_BUYER_ID`, `UNREVIEWED_SELLER_ID`, `reviewDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 19.

- `testFindActiveBySubjectIdWhenUserHasBothRolesReturnsOnlySelectedRole`
- `testStatsBySubjectIdWhenUserHasBothRolesReturnsIndependentActiveTotals`
- `testFindActiveBySubjectIdWhenOffsetIsTenReturnsLastReviewWithoutRepeats`
- `testFindActiveBySubjectIdWhenRoleHasNoReviewsReturnsEmptyList`
- `testFindActiveBySubjectIdWhenAuthorHasAvatarReturnsAccountAppearance`
- `testFindByInquiryAndAuthorWhenReviewExistsReturnsReviewWithAuthorName`
- `testFindByInquiryAndAuthorWhenAuthorHasNoReviewReturnsEmpty`
- `testFindActiveBySubjectIdWhenSubjectHasTwoActiveReviewsReturnsNewestFirst`
- `testFindActiveBySubjectIdWhenLimitIsOneReturnsOnlyTheNewest`
- `testFindActiveBySubjectIdWhenOnlyReviewIsRemovedReturnsEmptyList`
- `testStatsBySubjectIdWhenSubjectHasActiveReviewsReturnsCountAndAverage`
- `testStatsBySubjectIdWhenOnlyReviewIsRemovedReturnsZero`
- `testCreateWhenAuthorHasNoReviewReturnsPersistedReview`
- `testCreateWhenSameAuthorReviewsSaleTwiceReturnsConstraintError`
- `testCreateWhenRatingIsOutsideStarsReturnsConstraintError`
- `testUpdateWhenReviewWasRemovedReturnsSameRowReactivated`
- `testUpdateWhenAuthorHasNoReviewReturnsEmpty`
- `testDeactivateWhenReviewIsActiveReturnsTrueAndKeepsOtherPartysReview`
- `testDeactivateWhenReviewIsAlreadyRemovedReturnsFalseAndKeepsTheRow`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewDao]], [[ReviewStats]], [[ReviewSubjectRole]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/ReviewJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ReviewJdbcDaoTest.java>), líneas 1–317.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewStats;
import ar.edu.itba.paw.models.ReviewSubjectRole;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
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
public class ReviewJdbcDaoTest {
    private static final String REVIEWS_TABLE = "reviews";
    private static final int LIMIT = 10;
    // Venta confirmada (consulta 5): el usuario 1 le compro al 3 y se calificaron con las resenas 1 y 2.
    private static final long CONFIRMED_SALE_ID = 5;
    private static final long BUYER_ID = 1;
    private static final String BUYER_USERNAME = "bpessagno";
    private static final long SELLER_ID = 3;
    private static final long BUYER_REVIEW_ID = 1;
    private static final long SELLER_REVIEW_ID = 2;
    // Consulta 6: la resena 3 del usuario 2 sobre el 3 esta vigente y es la mas nueva; la 4 del 3 sobre el 2, quitada.
    private static final long OTHER_INQUIRY_ID = 6;
    private static final long OTHER_BUYER_ID = 2;
    private static final long NEWEST_REVIEW_ID = 3;
    private static final long REMOVED_REVIEW_ID = 4;
    // Consulta 8 todavia sin resenas: el usuario 5 le compra al 4.
    private static final long UNREVIEWED_INQUIRY_ID = 8;
    private static final long UNREVIEWED_BUYER_ID = 5;
    private static final long UNREVIEWED_SELLER_ID = 4;

    @Autowired
    private ReviewDao reviewDao;

    @Test
    public void testFindActiveBySubjectIdWhenUserHasBothRolesReturnsOnlySelectedRole() {
        // 1. Arrange
        final long subjectId = 6;

        // 2. Exercise
        final List<Review> sellers = reviewDao.findActiveBySubjectId(subjectId, ReviewSubjectRole.SELLER, 10, 0);
        final List<Review> buyers = reviewDao.findActiveBySubjectId(subjectId, ReviewSubjectRole.BUYER, 10, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(30L, 29L, 28L, 27L, 26L, 25L, 24L, 23L, 22L, 21L),
                sellers.stream().map(Review::getId).collect(Collectors.toList()));
        Assertions.assertEquals(List.of(31L), buyers.stream().map(Review::getId).collect(Collectors.toList()));
    }

    @Autowired
    private DataSource dataSource;

    @Test
    public void testStatsBySubjectIdWhenUserHasBothRolesReturnsIndependentActiveTotals() {
        // 1. Arrange
        final long subjectId = 6;

        // 2. Exercise
        final ReviewStats seller = reviewDao.statsBySubjectId(subjectId, ReviewSubjectRole.SELLER);
        final ReviewStats buyer = reviewDao.statsBySubjectId(subjectId, ReviewSubjectRole.BUYER);

        // 3. Assert
        Assertions.assertEquals(11, seller.getCount());
        Assertions.assertEquals(4.0, seller.getAverage());
        Assertions.assertEquals(1, buyer.getCount());
        Assertions.assertEquals(2.0, buyer.getAverage());
    }

    private JdbcTemplate jdbcTemplate;

    @Test
    public void testFindActiveBySubjectIdWhenOffsetIsTenReturnsLastReviewWithoutRepeats() {
        // 1. Arrange
        final long subjectId = 6;

        // 2. Exercise
        final List<Review> first = reviewDao.findActiveBySubjectId(subjectId, ReviewSubjectRole.SELLER, 10, 0);
        final List<Review> second = reviewDao.findActiveBySubjectId(subjectId, ReviewSubjectRole.SELLER, 10, 10);

        // 3. Assert
        Assertions.assertEquals(10, first.size());
        Assertions.assertEquals(List.of(20L), second.stream().map(Review::getId).collect(Collectors.toList()));
        Assertions.assertTrue(first.stream().noneMatch(review -> review.getId() == second.get(0).getId()));
    }

    @Test
    public void testFindActiveBySubjectIdWhenRoleHasNoReviewsReturnsEmptyList() {
        // 1. Arrange

        // 2. Exercise
        final List<Review> result = reviewDao.findActiveBySubjectId(SELLER_ID, ReviewSubjectRole.BUYER, LIMIT, 0);
        final ReviewStats stats = reviewDao.statsBySubjectId(SELLER_ID, ReviewSubjectRole.BUYER);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
        Assertions.assertEquals(0, stats.getCount());
        Assertions.assertEquals(0.0, stats.getAverage());
    }

    @Test
    public void testFindActiveBySubjectIdWhenAuthorHasAvatarReturnsAccountAppearance() {
        // 1. Arrange

        // 2. Exercise
        final List<Review> reviews = reviewDao.findActiveBySubjectId(SELLER_ID, ReviewSubjectRole.SELLER, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(2L, reviews.get(0).getAuthorAvatarImageId());
        Assertions.assertNull(reviews.get(1).getAuthorAvatarImageId());
    }

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindByInquiryAndAuthorWhenReviewExistsReturnsReviewWithAuthorName() {
        // 1. Arrange

        // 2. Exercise
        final Optional<Review> result = reviewDao.findByInquiryAndAuthor(CONFIRMED_SALE_ID, BUYER_ID);

        // 3. Assert
        final Review review = result.orElseThrow();
        Assertions.assertEquals(BUYER_REVIEW_ID, review.getId());
        Assertions.assertEquals(SELLER_ID, review.getSubjectId());
        Assertions.assertEquals(BUYER_USERNAME, review.getAuthorUsername());
        Assertions.assertEquals(5, review.getRating());
        Assertions.assertEquals("Muy buen vendedor", review.getBody());
        Assertions.assertTrue(review.isActive());
    }

    @Test
    public void testFindByInquiryAndAuthorWhenAuthorHasNoReviewReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<Review> result = reviewDao.findByInquiryAndAuthor(UNREVIEWED_INQUIRY_ID, UNREVIEWED_BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindActiveBySubjectIdWhenSubjectHasTwoActiveReviewsReturnsNewestFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<Review> result = reviewDao.findActiveBySubjectId(SELLER_ID, ReviewSubjectRole.SELLER, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(NEWEST_REVIEW_ID, BUYER_REVIEW_ID),
                result.stream().map(Review::getId).collect(Collectors.toList()));
    }

    @Test
    public void testFindActiveBySubjectIdWhenLimitIsOneReturnsOnlyTheNewest() {
        // 1. Arrange
        final int limit = 1;

        // 2. Exercise
        final List<Review> result = reviewDao.findActiveBySubjectId(SELLER_ID, ReviewSubjectRole.SELLER, limit, 0);

        // 3. Assert
        Assertions.assertEquals(1, result.size());
        Assertions.assertEquals(NEWEST_REVIEW_ID, result.get(0).getId());
    }

    @Test
    public void testFindActiveBySubjectIdWhenOnlyReviewIsRemovedReturnsEmptyList() {
        // 1. Arrange

        // 2. Exercise
        final List<Review> result = reviewDao.findActiveBySubjectId(OTHER_BUYER_ID, ReviewSubjectRole.BUYER, LIMIT, 0);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testStatsBySubjectIdWhenSubjectHasActiveReviewsReturnsCountAndAverage() {
        // 1. Arrange

        // 2. Exercise
        final ReviewStats result = reviewDao.statsBySubjectId(SELLER_ID, ReviewSubjectRole.SELLER);

        // 3. Assert
        Assertions.assertEquals(2, result.getCount());
        Assertions.assertEquals(3.5, result.getAverage());
    }

    @Test
    public void testStatsBySubjectIdWhenOnlyReviewIsRemovedReturnsZero() {
        // 1. Arrange

        // 2. Exercise
        final ReviewStats result = reviewDao.statsBySubjectId(OTHER_BUYER_ID, ReviewSubjectRole.BUYER);

        // 3. Assert
        Assertions.assertEquals(0, result.getCount());
        Assertions.assertEquals(0.0, result.getAverage());
    }

    @Test
    public void testCreateWhenAuthorHasNoReviewReturnsPersistedReview() {
        // 1. Arrange
        final int rating = 5;

        // 2. Exercise
        final Review created = reviewDao.create(UNREVIEWED_INQUIRY_ID, UNREVIEWED_BUYER_ID, UNREVIEWED_SELLER_ID,
                rating, "Muy buena vendedora");

        // 3. Assert
        Assertions.assertEquals(UNREVIEWED_SELLER_ID, created.getSubjectId());
        Assertions.assertTrue(created.isActive());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, REVIEWS_TABLE,
                "id = " + created.getId() + " AND inquiry_id = " + UNREVIEWED_INQUIRY_ID
                        + " AND author_id = " + UNREVIEWED_BUYER_ID + " AND subject_id = " + UNREVIEWED_SELLER_ID
                        + " AND rating = " + rating + " AND body = 'Muy buena vendedora' AND active = TRUE"));
    }

    @Test
    public void testCreateWhenSameAuthorReviewsSaleTwiceReturnsConstraintError() {
        // 1. Arrange

        // 2. Exercise
        final Class<? extends Throwable> error = Assertions.assertThrows(DataIntegrityViolationException.class,
                () -> reviewDao.create(CONFIRMED_SALE_ID, BUYER_ID, SELLER_ID, 4, null)).getClass();

        // 3. Assert
        Assertions.assertTrue(DataIntegrityViolationException.class.isAssignableFrom(error));
    }

    @Test
    public void testCreateWhenRatingIsOutsideStarsReturnsConstraintError() {
        // 1. Arrange

        // 2. Exercise
        final Class<? extends Throwable> error = Assertions.assertThrows(DataIntegrityViolationException.class,
                () -> reviewDao.create(UNREVIEWED_INQUIRY_ID, UNREVIEWED_BUYER_ID, UNREVIEWED_SELLER_ID, 0,
                        null)).getClass();

        // 3. Assert
        Assertions.assertTrue(DataIntegrityViolationException.class.isAssignableFrom(error));
    }

    @Test
    public void testUpdateWhenReviewWasRemovedReturnsSameRowReactivated() {
        // 1. Arrange
        final int rating = 4;

        // 2. Exercise
        final Optional<Review> result = reviewDao.update(OTHER_INQUIRY_ID, SELLER_ID, rating, "Corregido");

        // 3. Assert
        Assertions.assertEquals(REMOVED_REVIEW_ID, result.orElseThrow().getId());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, REVIEWS_TABLE,
                "id = " + REMOVED_REVIEW_ID + " AND rating = " + rating
                        + " AND body = 'Corregido' AND active = TRUE"));
    }

    @Test
    public void testUpdateWhenAuthorHasNoReviewReturnsEmpty() {
        // 1. Arrange

        // 2. Exercise
        final Optional<Review> result = reviewDao.update(UNREVIEWED_INQUIRY_ID, UNREVIEWED_BUYER_ID, 3, null);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testDeactivateWhenReviewIsActiveReturnsTrueAndKeepsOtherPartysReview() {
        // 1. Arrange

        // 2. Exercise
        final boolean result = reviewDao.deactivate(CONFIRMED_SALE_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, REVIEWS_TABLE,
                "id = " + BUYER_REVIEW_ID + " AND active = FALSE"));
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, REVIEWS_TABLE,
                "id = " + SELLER_REVIEW_ID + " AND active = TRUE"));
    }

    @Test
    public void testDeactivateWhenReviewIsAlreadyRemovedReturnsFalseAndKeepsTheRow() {
        // 1. Arrange

        // 2. Exercise
        final boolean result = reviewDao.deactivate(OTHER_INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, REVIEWS_TABLE,
                "id = " + REMOVED_REVIEW_ID + " AND active = FALSE"));
    }
}
```
