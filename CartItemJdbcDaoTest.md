---
title: "CartItemJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java"]
---

# CartItemJdbcDaoTest

Tests de `CartItemJdbcDao` en `persistence`: 12 casos declarados. Cubre: agregar, repetidos, quitar, quitar varios y el filtro de consultables por estado del post y consultas abiertas. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `CART_ITEMS_TABLE`, `POST_STATUS`, `EXCLUDED_INQUIRY_STATUSES`, `cartItemDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 12.

- `testAddWhenPostIsNotInCartReturnsTrue`
- `testAddWhenPostIsAlreadyInCartReturnsFalse`
- `testRemoveWhenPostIsInCartReturnsTrue`
- `testRemoveWhenPostIsNotInCartReturnsFalse`
- `testRemoveAllWhenIdsGivenReturnsRemovedCountAndRemovesOnlyThose`
- `testContainsWhenPostIsReservedReturnsTrue`
- `testFindByUserIdWhenSomePostsAreFilteredOutReturnsTheRestOrderedBySellerAndAddedAt`
- `testFindByUserIdWhenPostMatchesReturnsItsData`
- `testFindByUserIdWhenPostsHaveAnotherStatusReturnsEmpty`
- `testFindByUserIdWhenBuyerHasInquiryInExcludedStatusReturnsEmpty`
- `testFindByUserIdWhenCartIsEmptyReturnsEmpty`
- `testCountByUserIdWhenSomePostsAreFilteredOutReturnsTheRest`

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartItem]], [[CartItemDao]], [[InquiryStatus]], [[PostStatus]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java>), líneas 1–214.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.CartItem;
import ar.edu.itba.paw.models.InquiryStatus;
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

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class CartItemJdbcDaoTest {

    private static final String CART_ITEMS_TABLE = "cart_items";
    private static final PostStatus POST_STATUS = PostStatus.AVAILABLE;
    private static final List<InquiryStatus> EXCLUDED_INQUIRY_STATUSES = InquiryStatus.OPEN_STATUSES;

    @Autowired
    private CartItemDao cartItemDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testAddWhenPostIsNotInCartReturnsTrue() {
        // 1. Arrange
        final long userId = 1;
        final long postId = 2;

        // 2. Exercise
        final boolean result = cartItemDao.add(userId, postId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 1 AND post_id = 2"));
    }

    @Test
    public void testAddWhenPostIsAlreadyInCartReturnsFalse() {
        // 1. Arrange
        final long userId = 5;
        final long postId = 1;

        // 2. Exercise
        final boolean result = cartItemDao.add(userId, postId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 5 AND post_id = 1"));
    }

    @Test
    public void testRemoveWhenPostIsInCartReturnsTrue() {
        // 1. Arrange
        final long userId = 5;
        final long postId = 1;

        // 2. Exercise
        final boolean result = cartItemDao.remove(userId, postId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 5 AND post_id = 1"));
    }

    @Test
    public void testRemoveWhenPostIsNotInCartReturnsFalse() {
        // 1. Arrange
        final long userId = 1;
        final long postId = 2;

        // 2. Exercise
        final boolean result = cartItemDao.remove(userId, postId);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(8, JdbcTestUtils.countRowsInTable(jdbcTemplate, CART_ITEMS_TABLE));
    }

    @Test
    public void testRemoveAllWhenIdsGivenReturnsRemovedCountAndRemovesOnlyThose() {
        // 1. Arrange
        final long userId = 5;
        final List<Long> postIds = List.of(1L, 3L);

        // 2. Exercise
        final int result = cartItemDao.removeAll(userId, postIds);

        // 3. Assert
        Assertions.assertEquals(2, result);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 5 AND post_id IN (1, 3)"));
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 5 AND post_id IN (2, 4, 7)"));
    }

    @Test
    public void testContainsWhenPostIsReservedReturnsTrue() {
        // 1. Arrange
        final long userId = 6;
        final long reservedPostId = 7;

        // 2. Exercise
        final boolean result = cartItemDao.contains(userId, reservedPostId);

        // 3. Assert
        Assertions.assertTrue(result);
    }

    @Test
    public void testFindByUserIdWhenSomePostsAreFilteredOutReturnsTheRestOrderedBySellerAndAddedAt() {
        // 1. Arrange
        final long userId = 5;
        final List<Long> expectedPostIds = List.of(3L, 1L, 2L);
        final List<String> expectedSellers = List.of("bpessagno", "bpessagno", "tgorganchian");

        // 2. Exercise
        final List<CartItem> result = cartItemDao.findByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES);

        // 3. Assert
        Assertions.assertEquals(expectedPostIds, result.stream().map(CartItem::getPostId).toList());
        Assertions.assertEquals(expectedSellers, result.stream().map(CartItem::getSellerUsername).toList());
    }

    @Test
    public void testFindByUserIdWhenPostMatchesReturnsItsData() {
        // 1. Arrange
        final long userId = 5;

        // 2. Exercise
        final CartItem result = cartItemDao.findByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES).get(0);

        // 3. Assert
        Assertions.assertEquals(3, result.getPostId());
        Assertions.assertEquals(1, result.getSellerId());
        Assertions.assertEquals("bpessagno", result.getSellerUsername());
        Assertions.assertEquals("cancion animal", result.getTitle());
        Assertions.assertEquals("soda stereo", result.getArtistName());
        Assertions.assertEquals(1990, result.getReleaseYear());
        Assertions.assertTrue(result.getCoverImageId().isEmpty());
        Assertions.assertEquals(30000, result.getPrice());
    }

    @Test
    public void testFindByUserIdWhenPostsHaveAnotherStatusReturnsEmpty() {
        // 1. Arrange
        final long userId = 6;

        // 2. Exercise
        final List<CartItem> result = cartItemDao.findByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByUserIdWhenBuyerHasInquiryInExcludedStatusReturnsEmpty() {
        // 1. Arrange
        final long userId = 2;

        // 2. Exercise
        final List<CartItem> result = cartItemDao.findByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByUserIdWhenCartIsEmptyReturnsEmpty() {
        // 1. Arrange
        final long userId = 1;

        // 2. Exercise
        final List<CartItem> result = cartItemDao.findByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testCountByUserIdWhenSomePostsAreFilteredOutReturnsTheRest() {
        // 1. Arrange
        final long userId = 5;

        // 2. Exercise
        final int result = cartItemDao.countByUserId(userId, POST_STATUS, EXCLUDED_INQUIRY_STATUSES);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }
}
```
