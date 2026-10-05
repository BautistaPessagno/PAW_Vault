---
title: "InquiryStatusFilterTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/InquiryStatusFilterTest.java"]
---

# InquiryStatusFilterTest

Tests de `InquiryStatusFilter` en `services`: 3 casos declarados. Cubre: que [[InquiryStatusFilter]] sume bien por filtro, que cada estado caiga en exactamente un filtro y que sin consultas los conteos queden vacíos. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

Casos declarados: 3.

- `testCountsFromWhenStatusesAreMixedReturnsSumPerFilter`
- `testCountsFromWhenEveryStatusHasOneReturnsEachStatusInExactlyOneFilter`
- `testCountsFromWhenThereAreNoInquiriesReturnsEmptyCounts`

## Conexiones

Referencias estáticas a tipos del proyecto: [[FilterCounts]], [[InquiryStatus]], [[InquiryStatusFilter]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/InquiryStatusFilterTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryStatusFilterTest.java>), líneas 1–57.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.FilterCounts;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquiryStatusFilter;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class InquiryStatusFilterTest {

    @Test
    public void testCountsFromWhenStatusesAreMixedReturnsSumPerFilter() {
        // 1. Arrange
        final Map<InquiryStatus, Integer> byStatus = Map.of(InquiryStatus.PENDING, 3,
                InquiryStatus.AWAITING_PAYMENT, 1, InquiryStatus.PAYMENT_SUBMITTED, 2,
                InquiryStatus.REJECTED, 4, InquiryStatus.CANCELLED, 1);

        // 2. Exercise
        final FilterCounts<InquiryStatusFilter> result = InquiryStatusFilter.countsFrom(byStatus);

        // 3. Assert
        Assertions.assertEquals(Map.of(InquiryStatusFilter.PENDING, 3, InquiryStatusFilter.IN_PROGRESS, 3,
                InquiryStatusFilter.CLOSED, 5), result.getCounts());
        Assertions.assertEquals(11, result.getTotal());
    }

    @Test
    public void testCountsFromWhenEveryStatusHasOneReturnsEachStatusInExactlyOneFilter() {
        // 1. Arrange
        final Map<InquiryStatus, Integer> oneEach = Arrays.stream(InquiryStatus.values())
                .collect(Collectors.toMap(Function.identity(), status -> 1));

        // 2. Exercise
        final FilterCounts<InquiryStatusFilter> result = InquiryStatusFilter.countsFrom(oneEach);

        // 3. Assert
        Assertions.assertEquals(InquiryStatus.values().length, result.getTotal());
    }

    @Test
    public void testCountsFromWhenThereAreNoInquiriesReturnsEmptyCounts() {
        // 1. Arrange
        final Map<InquiryStatus, Integer> none = Map.of();

        // 2. Exercise
        final FilterCounts<InquiryStatusFilter> result = InquiryStatusFilter.countsFrom(none);

        // 3. Assert
        Assertions.assertTrue(result.getCounts().isEmpty());
        Assertions.assertEquals(0, result.getTotal());
    }
}
```
