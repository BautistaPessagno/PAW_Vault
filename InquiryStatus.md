---
title: "InquiryStatus"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java"]
---

# InquiryStatus

Estados de la Consulta: `PENDING`, `AWAITING_PAYMENT`, `PAYMENT_SUBMITTED`, `ACCEPTED` (venta confirmada), `REJECTED` y `CANCELLED`. `OPEN_STATUSES` reúne los tres primeros: un comprador tiene a lo sumo una Consulta abierta por post. Ver [[Inquiry and sale flow]].

## Guía de lectura

Datos y dependencias declaradas: `OPEN_STATUSES`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartItemDao]], [[CartItemJdbcDao]], [[CartItemJdbcDaoTest]], [[CartServiceImplTest]], [[ContactRules]], [[Inquiry]], [[InquiryDao]], [[InquiryDetail]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquiryStatusFilter]], [[InquiryStatusFilterTest]], [[InquirySummary]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java>), líneas 1–18.

```java
package ar.edu.itba.paw.models;

import java.util.List;

public enum InquiryStatus {
    PENDING,
    AWAITING_PAYMENT,
    PAYMENT_SUBMITTED,
    // ACCEPTED es la venta confirmada: el nombre se conserva para no migrar las consultas
    // aceptadas antes de la reserva.
    ACCEPTED,
    REJECTED,
    CANCELLED;

    // Consulta abierta: pendiente o con la Venta en curso. Un comprador tiene a lo sumo una
    // por post.
    public static final List<InquiryStatus> OPEN_STATUSES = List.of(PENDING, AWAITING_PAYMENT, PAYMENT_SUBMITTED);
}
```
