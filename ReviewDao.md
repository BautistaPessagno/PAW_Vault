---
title: "ReviewDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java"]
---

# ReviewDao

Contrato de reseñas: buscar la de un autor en una venta, listar las activas de una Cuenta por rol y con `LIMIT`/`OFFSET`, estadísticas por rol, crear, actualizar (reactivando) y desactivar.

## Guía de lectura

Operaciones para localizar en la fuente: `findByInquiryAndAuthor`, `findActiveBySubjectId`, `statsBySubjectId`, `create`, `update`, `deactivate`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewStats]], [[ReviewSubjectRole]].

Referenciado por: [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java>), líneas 1–22.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewStats;
import ar.edu.itba.paw.models.ReviewSubjectRole;

import java.util.List;
import java.util.Optional;

public interface ReviewDao {
    Optional<Review> findByInquiryAndAuthor(long inquiryId, long authorId);

    List<Review> findActiveBySubjectId(long subjectId, ReviewSubjectRole role, int limit, int offset);

    ReviewStats statsBySubjectId(long subjectId, ReviewSubjectRole role);

    Review create(long inquiryId, long authorId, long subjectId, int rating, String body);

    Optional<Review> update(long inquiryId, long authorId, int rating, String body);

    boolean deactivate(long inquiryId, long authorId);
}
```
