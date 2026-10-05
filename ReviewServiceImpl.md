---
title: "ReviewServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ReviewServiceImpl.java"]
---

# ReviewServiceImpl

Guarda (actualizando la fila existente o creando) y quita (borrado lógico) reseñas con propagación `MANDATORY`; lee la reseña activa y arma páginas de 10 por rol con sus estadísticas. Ver [[Reviews flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `PAGE_SIZE`, `reviewDao`.

Operaciones para localizar en la fuente: `save`, `remove`, `findActive`, `findPageForUser`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InvalidReviewException]], [[PageNotFoundException]], [[Pagination]], [[Review]], [[ReviewDao]], [[ReviewPage]], [[ReviewRules]], [[ReviewService]], [[ReviewStats]], [[ReviewSubjectRole]].

Referenciado por: [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/ReviewServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ReviewServiceImpl.java>), líneas 1–80.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewRules;
import ar.edu.itba.paw.models.ReviewStats;
import ar.edu.itba.paw.models.ReviewPage;
import ar.edu.itba.paw.models.ReviewSubjectRole;
import ar.edu.itba.paw.persistence.ReviewDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class ReviewServiceImpl implements ReviewService {
    private static final Logger LOGGER = LoggerFactory.getLogger(ReviewServiceImpl.class);
    private static final int PAGE_SIZE = 10;

    private final ReviewDao reviewDao;

    @Autowired
    public ReviewServiceImpl(final ReviewDao reviewDao) {
        this.reviewDao = reviewDao;
    }

    // MANDATORY: sin la transaccion de InquiryService, el lock de la consulta no protegeria nada.
    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public Review save(final long inquiryId, final long authorId, final long subjectId, final int rating,
                       final String body) {
        final String normalizedBody = ReviewRules.normalize(body);
        if (!ReviewRules.isValid(rating, normalizedBody)) {
            LOGGER.warn("Rejected review inquiryId={} authorId={} rating={}", inquiryId, authorId, rating);
            throw new InvalidReviewException();
        }
        // Una Resena quitada vuelve a ser la misma fila: el autor califica una sola vez por venta.
        final Optional<Review> updated = reviewDao.update(inquiryId, authorId, rating, normalizedBody);
        if (updated.isPresent()) {
            LOGGER.info("Updated review inquiryId={} authorId={}", inquiryId, authorId);
            return updated.get();
        }
        final Review created = reviewDao.create(inquiryId, authorId, subjectId, rating, normalizedBody);
        LOGGER.info("Created review inquiryId={} authorId={}", inquiryId, authorId);
        return created;
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean remove(final long inquiryId, final long authorId) {
        final boolean removed = reviewDao.deactivate(inquiryId, authorId);
        if (removed) {
            LOGGER.info("Removed review inquiryId={} authorId={}", inquiryId, authorId);
        }
        return removed;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Review> findActive(final long inquiryId, final long authorId) {
        return reviewDao.findByInquiryAndAuthor(inquiryId, authorId).filter(Review::isActive);
    }

    @Override
    @Transactional(readOnly = true)
    public ReviewPage findPageForUser(final long userId, final ReviewSubjectRole role, final int pageNumber) {
        final ReviewStats stats = reviewDao.statsBySubjectId(userId, role);
        final int totalPages = Pagination.pagesFor(stats.getCount(), PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, PAGE_SIZE, totalPages);
        final List<Review> reviews = reviewDao.findActiveBySubjectId(userId, role, PAGE_SIZE, offset);
        if (pageNumber > 1 && reviews.isEmpty()) {
            throw new PageNotFoundException();
        }
        return new ReviewPage(reviews, role, stats, pageNumber, totalPages);
    }
}
```
