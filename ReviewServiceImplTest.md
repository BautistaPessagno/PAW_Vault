---
title: "ReviewServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ReviewServiceImplTest.java"]
---

# ReviewServiceImplTest

Tests de `ReviewServiceImpl` en `services`: 8 casos declarados. Cubre: guardar, reemplazar, quitar y reglas de la reseña. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `INQUIRY_ID`, `BUYER_ID`, `SELLER_ID`, `reviewService`.

Operaciones para localizar en la fuente: `setUp`, `review`.

Casos declarados: 8.

- `testSaveWhenAuthorHasNoReviewReturnsCreatedReview`
- `testSaveWhenReviewAlreadyExistsReturnsUpdatedRating`
- `testSaveWhenBodyHasLineBreaksAndSpacesReturnsReviewWithNormalizedBody`
- `testSaveWhenBodyIsBlankReturnsReviewWithoutBody`
- `testSaveWhenMultilineBodyFitsAfterNormalizingReturnsReview`
- `testSaveWhenRatingIsOutOfRangeReturnsInvalidReviewException`
- `testSaveWhenBodyIsTooLongReturnsInvalidReviewException`
- `testFindActiveWhenReviewIsInactiveReturnsEmpty`

## Conexiones

Referencias estáticas a tipos del proyecto: [[InvalidReviewException]], [[Review]], [[ReviewDao]], [[ReviewRules]], [[ReviewService]], [[ReviewServiceImpl]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/ReviewServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ReviewServiceImplTest.java>), líneas 1–144.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewRules;
import ar.edu.itba.paw.persistence.ReviewDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class ReviewServiceImplTest {
    private static final long INQUIRY_ID = 5;
    private static final long BUYER_ID = 1;
    private static final long SELLER_ID = 3;

    @Mock private ReviewDao reviewDao;
    private ReviewService reviewService;

    @BeforeEach
    public void setUp() {
        reviewService = new ReviewServiceImpl(reviewDao);
    }

    @Test
    public void testSaveWhenAuthorHasNoReviewReturnsCreatedReview() {
        // 1. Arrange
        Mockito.when(reviewDao.update(INQUIRY_ID, BUYER_ID, 5, "Bien")).thenReturn(Optional.empty());
        Mockito.when(reviewDao.create(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, "Bien"))
                .thenReturn(review(5, "Bien", true));

        // 2. Exercise
        final Review saved = reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, "Bien");

        // 3. Assert
        Assertions.assertEquals(SELLER_ID, saved.getSubjectId());
        Assertions.assertEquals(5, saved.getRating());
    }

    @Test
    public void testSaveWhenReviewAlreadyExistsReturnsUpdatedRating() {
        // 1. Arrange
        Mockito.when(reviewDao.update(INQUIRY_ID, BUYER_ID, 4, "Mejoró"))
                .thenReturn(Optional.of(review(4, "Mejoró", true)));

        // 2. Exercise
        final Review updated = reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 4, "Mejoró");

        // 3. Assert
        Assertions.assertEquals(4, updated.getRating());
        Assertions.assertEquals("Mejoró", updated.getBody());
    }

    @Test
    public void testSaveWhenBodyHasLineBreaksAndSpacesReturnsReviewWithNormalizedBody() {
        // 1. Arrange
        Mockito.when(reviewDao.update(INQUIRY_ID, BUYER_ID, 5, "Linea uno\nLinea dos")).thenReturn(Optional.empty());
        Mockito.when(reviewDao.create(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, "Linea uno\nLinea dos"))
                .thenReturn(review(5, "Linea uno\nLinea dos", true));

        // 2. Exercise
        final Review saved = reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, "  Linea uno\r\nLinea dos  ");

        // 3. Assert
        Assertions.assertEquals("Linea uno\nLinea dos", saved.getBody());
    }

    @Test
    public void testSaveWhenBodyIsBlankReturnsReviewWithoutBody() {
        // 1. Arrange
        Mockito.when(reviewDao.update(INQUIRY_ID, BUYER_ID, 3, null)).thenReturn(Optional.empty());
        Mockito.when(reviewDao.create(INQUIRY_ID, BUYER_ID, SELLER_ID, 3, null)).thenReturn(review(3, null, true));

        // 2. Exercise
        final Review saved = reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 3, "   ");

        // 3. Assert
        Assertions.assertNull(saved.getBody());
    }

    @Test
    public void testSaveWhenMultilineBodyFitsAfterNormalizingReturnsReview() {
        // 1. Arrange
        // 249 + LF + 250 = 500: con CRLF serian 501 y quedaria afuera del tope.
        final String body = "A".repeat(249) + "\n" + "B".repeat(250);
        Mockito.when(reviewDao.update(INQUIRY_ID, BUYER_ID, 5, body)).thenReturn(Optional.empty());
        Mockito.when(reviewDao.create(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, body)).thenReturn(review(5, body, true));

        // 2. Exercise
        final Review saved = reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, body.replace("\n", "\r\n"));

        // 3. Assert
        Assertions.assertEquals(ReviewRules.MAX_BODY_LENGTH, saved.getBody().length());
    }

    @Test
    public void testSaveWhenRatingIsOutOfRangeReturnsInvalidReviewException() {
        // 1. Arrange
        final int rating = ReviewRules.MAX_RATING + 1;

        // 2. Exercise
        final Executable save = () -> reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, rating, null);

        // 3. Assert
        Assertions.assertThrows(InvalidReviewException.class, save);
    }

    @Test
    public void testSaveWhenBodyIsTooLongReturnsInvalidReviewException() {
        // 1. Arrange
        final String body = "A".repeat(ReviewRules.MAX_BODY_LENGTH + 1);

        // 2. Exercise
        final Executable save = () -> reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, body);

        // 3. Assert
        Assertions.assertThrows(InvalidReviewException.class, save);
    }

    @Test
    public void testFindActiveWhenReviewIsInactiveReturnsEmpty() {
        // 1. Arrange
        Mockito.when(reviewDao.findByInquiryAndAuthor(INQUIRY_ID, BUYER_ID))
                .thenReturn(Optional.of(review(5, null, false)));

        // 2. Exercise
        final Optional<Review> result = reviewService.findActive(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    private static Review review(final int rating, final String body, final boolean active) {
        return new Review(1, INQUIRY_ID, BUYER_ID, SELLER_ID, "buyer", rating, body, active,
                LocalDateTime.of(2026, 1, 1, 12, 0));
    }
}
```
