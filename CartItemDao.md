---
title: "CartItemDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/CartItemDao.java"]
---

# CartItemDao

Contrato de persistencia del carrito: agregar, quitar, quitar varios, saber si un post está, y listar o contar filtrando por estado del post y por consultas que lo ocultan. Qué combinación significa "se puede consultar" lo decide el service. Lo implementa [[CartItemJdbcDao]].

## Guía de lectura

Operaciones para localizar en la fuente: `add`, `remove`, `removeAll`, `contains`, `findByUserId`, `countByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartItem]], [[InquiryStatus]], [[PostStatus]].

Referenciado por: [[CartItemJdbcDao]], [[CartItemJdbcDaoTest]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/CartItemDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/CartItemDao.java>), líneas 1–30.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.CartItem;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.PostStatus;

import java.util.Collection;
import java.util.List;

public interface CartItemDao {

    // false si el Post ya estaba en el carrito.
    boolean add(long userId, long postId);

    boolean remove(long userId, long postId);

    int removeAll(long userId, Collection<Long> postIds);

    boolean contains(long userId, long postId);

    /*
     * Los items del carrito cuyo Post esta en postStatus y sobre el que el comprador no tiene una
     * Consulta en alguno de excludedInquiryStatuses. Que combinacion significa "se puede consultar"
     * lo decide el service; el resto queda guardado. Ordenado por Publicante y, dentro de cada
     * uno, por orden de agregado.
     */
    List<CartItem> findByUserId(long userId, PostStatus postStatus, Collection<InquiryStatus> excludedInquiryStatuses);

    int countByUserId(long userId, PostStatus postStatus, Collection<InquiryStatus> excludedInquiryStatuses);
}
```
