---
title: "InquiryStatusFilter"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryStatusFilter.java"]
---

# InquiryStatusFilter

Los cuatro filtros de las bandejas, agrupando estados como los lee una persona: `PENDING`, `IN_PROGRESS` (espera de pago y pago informado), `CONFIRMED` (`ACCEPTED`) y `CLOSED` (rechazada o cancelada). Cada estado cae en un solo filtro. `countsFrom` pasa conteos por estado a [[FilterCounts]] por filtro. Ver [[Status filters flow]].

## Guía de lectura

Datos y dependencias declaradas: `statuses`.

Operaciones para localizar en la fuente: `getStatuses`, `countsFrom`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[FilterCounts]], [[InquiryStatus]].

Referenciado por: [[InquiryController]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquiryStatusFilterTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/InquiryStatusFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryStatusFilter.java>), líneas 1–36.

```java
package ar.edu.itba.paw.models;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;

// Filtro de las bandejas de Consultas: agrupa los estados como los lee una persona. Cada estado
// cae en exactamente un filtro; un estado nuevo tiene que sumarse aca.
public enum InquiryStatusFilter {
    PENDING(InquiryStatus.PENDING),
    IN_PROGRESS(InquiryStatus.AWAITING_PAYMENT, InquiryStatus.PAYMENT_SUBMITTED),
    CONFIRMED(InquiryStatus.ACCEPTED),
    CLOSED(InquiryStatus.REJECTED, InquiryStatus.CANCELLED);

    private final List<InquiryStatus> statuses;

    InquiryStatusFilter(final InquiryStatus... statuses) {
        this.statuses = List.of(statuses);
    }

    public List<InquiryStatus> getStatuses() { return statuses; }

    // Pasa los conteos por estado a conteos por filtro. Un filtro sin Consultas no aparece.
    public static FilterCounts<InquiryStatusFilter> countsFrom(final Map<InquiryStatus, Integer> byStatus) {
        final Map<InquiryStatusFilter, Integer> byFilter = new EnumMap<>(InquiryStatusFilter.class);
        for (final InquiryStatusFilter filter : values()) {
            for (final InquiryStatus status : filter.statuses) {
                final Integer count = byStatus.get(status);
                if (count != null) {
                    byFilter.merge(filter, count, Integer::sum);
                }
            }
        }
        return new FilterCounts<>(byFilter);
    }
}
```
