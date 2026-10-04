---
title: "InquiryParties"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryParties.java"]
---

# InquiryParties

Comprador y publicante de una Consulta, sin el resto del resumen. Alcanza para decidir pertenencia; lo usa [[InquiryAccessHandler]].

## Guía de lectura

Datos y dependencias declaradas: `buyerId`, `sellerId`.

Operaciones para localizar en la fuente: `getBuyerId`, `getSellerId`, `isBuyer`, `isSeller`, `isParty`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryAccessHandler]], [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/InquiryParties.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryParties.java>), líneas 1–21.

```java
package ar.edu.itba.paw.models;

// Las dos partes de una consulta, sin el resto del summary: alcanza para decidir quien puede
// operar sobre ella. El vendedor es el publicante, o el que la consulta guardo si el post se borro.
public final class InquiryParties {

    private final long buyerId;
    private final long sellerId;

    public InquiryParties(final long buyerId, final long sellerId) {
        this.buyerId = buyerId;
        this.sellerId = sellerId;
    }

    public long getBuyerId() { return buyerId; }
    public long getSellerId() { return sellerId; }

    public boolean isBuyer(final long userId) { return buyerId == userId; }
    public boolean isSeller(final long userId) { return sellerId == userId; }
    public boolean isParty(final long userId) { return isBuyer(userId) || isSeller(userId); }
}
```
