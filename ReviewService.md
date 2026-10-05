---
title: "ReviewService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ReviewService.java"]
---

# ReviewService

Contrato de reseñas. `save` y `remove` son internas de la venta: solo las llama [[InquiryServiceImpl]] dentro de su transacción y no validan permisos. `findPageForUser` pagina por rol.

## Guía de lectura

Operaciones para localizar en la fuente: `save`, `remove`, `findActive`, `findPageForUser`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewPage]], [[ReviewSubjectRole]].

Referenciado por: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/ReviewService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ReviewService.java>), líneas 1–28.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewPage;
import ar.edu.itba.paw.models.ReviewSubjectRole;

import java.util.Optional;

public interface ReviewService {

    /*
     * Internas de la Venta: solo InquiryService las llama, dentro de su transaccion y despues de
     * bloquear la consulta y de chequear que el autor es una de las partes de una venta confirmada.
     * No validan permisos ni estado: llamarlas desde otro lado saltea esos chequeos. Exigen una
     * transaccion abierta (MANDATORY).
     */

    // Crea la Resena o reemplaza la anterior del mismo autor. Lanza InvalidReviewException si no
    // cumple ReviewRules.
    Review save(long inquiryId, long authorId, long subjectId, int rating, String body);

    // false si no habia una Resena vigente que quitar.
    boolean remove(long inquiryId, long authorId);

    Optional<Review> findActive(long inquiryId, long authorId);

    ReviewPage findPageForUser(long userId, ReviewSubjectRole role, int pageNumber);
}
```
