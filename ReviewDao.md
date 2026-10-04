---
title: "ReviewDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java"]
---

# ReviewDao

Contrato de reseñas: buscar la de un autor en una venta, listar las activas de una Cuenta, estadísticas, crear, actualizar (reactivando) y desactivar.

## Guía de lectura

Operaciones para localizar en la fuente: `findByInquiryAndAuthor`, `findActiveBySubjectId`, `statsBySubjectId`, `create`, `update`, `deactivate`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewStats]].

Referenciado por: [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java>), líneas 1–21.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewStats;

import java.util.List;
import java.util.Optional;

public interface ReviewDao {
    Optional<Review> findByInquiryAndAuthor(long inquiryId, long authorId);

    List<Review> findActiveBySubjectId(long subjectId, int limit);

    ReviewStats statsBySubjectId(long subjectId);

    Review create(long inquiryId, long authorId, long subjectId, int rating, String body);

    Optional<Review> update(long inquiryId, long authorId, int rating, String body);

    boolean deactivate(long inquiryId, long authorId);
}
```
