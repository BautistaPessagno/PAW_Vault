---
title: "InquiryDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java"]
---

# InquiryDao

Contrato de consultas: crear una o varias en lote, bandejas paginadas por publicación, resumen y partes, transiciones de estado con guarda, comprobante, consultas abiertas de un comprador, rechazo de las demás pendientes y desenganche al eliminar un post.

## Guía de lectura

Operaciones para localizar en la fuente: `create`, `createAll`, `findById`, `findByIdForUpdate`, `findOpenIdByPostAndBuyer`, `findPostIdsWithOpenInquiry`, `findByBuyerId`, `findBySellerId`, `countGroupsByBuyerId`, `countGroupsBySellerId`, `updateStatus`, `saveReceipt`, `findReceipt`, `findSummaryById`, `findPartiesById`, `hasOpenSalesBySellerId`, `findPendingByPostId`, `rejectOtherPending`, `countByBuyerId`, `countBySellerId`, `detachFromPost`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Inquiry]], [[InquiryParties]], [[InquiryStatus]], [[InquirySummary]], [[Receipt]].

Referenciado por: [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java>), líneas 1–69.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.Receipt;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

public interface InquiryDao {
    // price es el del post al consultar: queda fijo aunque el post se edite despues.
    Inquiry create(long postId, long buyerId, long addressId, int price);

    /*
     * Una Consulta pendiente por Post, todas con la misma direccion, en dos sentencias fijas sea
     * cual sea la cantidad. priceByPostId lleva el precio de cada Post al consultar. Devuelve las
     * creadas por id de Post.
     */
    Map<Long, Inquiry> createAll(long buyerId, long addressId, Map<Long, Integer> priceByPostId);

    Optional<Inquiry> findById(long id);

    Optional<Inquiry> findByIdForUpdate(long id);

    // La Consulta abierta (pendiente o con la Venta en curso) del comprador sobre el post, si hay.
    Optional<Long> findOpenIdByPostAndBuyer(long postId, long buyerId);

    // De entre postIds, los Posts sobre los que el comprador tiene una Consulta abierta.
    Set<Long> findPostIdsWithOpenInquiry(long buyerId, Collection<Long> postIds);

    // Bandejas paginadas por publicacion: devuelven las consultas de una pagina de grupos,
    // ordenadas de la mas nueva a la mas vieja. El grupo es el post, o el album y el vendedor
    // cuando el post fue eliminado. groupLimit/groupOffset cuentan grupos, no consultas.
    List<InquirySummary> findByBuyerId(long buyerId, int groupLimit, int groupOffset);

    List<InquirySummary> findBySellerId(long sellerId, int groupLimit, int groupOffset);

    int countGroupsByBuyerId(long buyerId);

    int countGroupsBySellerId(long sellerId);

    boolean updateStatus(long id, InquiryStatus from, InquiryStatus to);

    boolean saveReceipt(long id, String contentType, byte[] data);

    Optional<Receipt> findReceipt(long id);

    Optional<InquirySummary> findSummaryById(long id);

    Optional<InquiryParties> findPartiesById(long id);

    // true si el vendedor tiene alguna venta esperando el pago o su revision.
    boolean hasOpenSalesBySellerId(long sellerId);

    List<InquirySummary> findPendingByPostId(long postId);

    int rejectOtherPending(long postId, long acceptedInquiryId);

    int countByBuyerId(long buyerId);

    int countBySellerId(long sellerId);

    int detachFromPost(long postId);
}
```
