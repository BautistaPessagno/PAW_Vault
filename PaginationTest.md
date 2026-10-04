---
title: "PaginationTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java"]
---

# PaginationTest

Tests de `Pagination` en `services`: 8 casos declarados. Cubre: páginas para totales vacíos, exactos y con resto; offsets y páginas fuera de rango. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `PAGE_SIZE`.

Casos declarados: 8.

- `testPagesForWhenTotalIsZeroReturnsZero`
- `testPagesForWhenTotalIsAMultipleOfThePageSizeReturnsExactPages`
- `testPagesForWhenTotalOverflowsAPageReturnsOneMorePage`
- `testOffsetForWhenPageIsWithinTheTotalReturnsOffset`
- `testOffsetForWhenPageIsPastTheTotalReturnsPageNotFoundException`
- `testOffsetForWhenFirstPageOfAnEmptyTotalReturnsZero`
- `testOffsetForWhenPageIsBelowOneReturnsPageNotFoundException`
- `testOffsetForWhenOffsetOverflowsAnIntReturnsPageNotFoundException`

## Conexiones

Referencias estáticas a tipos del proyecto: [[PageNotFoundException]], [[Pagination]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java>), líneas 1–109.

```java
package ar.edu.itba.paw.services;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;

public class PaginationTest {

    private static final int PAGE_SIZE = 12;

    @Test
    public void testPagesForWhenTotalIsZeroReturnsZero() {
        // 1. Arrange
        final int total = 0;

        // 2. Exercise
        final int result = Pagination.pagesFor(total, PAGE_SIZE);

        // 3. Assert
        Assertions.assertEquals(0, result);
    }

    @Test
    public void testPagesForWhenTotalIsAMultipleOfThePageSizeReturnsExactPages() {
        // 1. Arrange
        final int total = 24;

        // 2. Exercise
        final int result = Pagination.pagesFor(total, PAGE_SIZE);

        // 3. Assert
        Assertions.assertEquals(2, result);
    }

    @Test
    public void testPagesForWhenTotalOverflowsAPageReturnsOneMorePage() {
        // 1. Arrange
        final int total = 25;

        // 2. Exercise
        final int result = Pagination.pagesFor(total, PAGE_SIZE);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testOffsetForWhenPageIsWithinTheTotalReturnsOffset() {
        // 1. Arrange
        final int pageNumber = 2;
        final int totalPages = 3;

        // 2. Exercise
        final int result = Pagination.offsetFor(pageNumber, PAGE_SIZE, totalPages);

        // 3. Assert
        Assertions.assertEquals(12, result);
    }

    @Test
    public void testOffsetForWhenPageIsPastTheTotalReturnsPageNotFoundException() {
        // 1. Arrange
        final int pageNumber = 4;
        final int totalPages = 3;

        // 2. Exercise
        final Executable offset = () -> Pagination.offsetFor(pageNumber, PAGE_SIZE, totalPages);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, offset);
    }

    @Test
    public void testOffsetForWhenFirstPageOfAnEmptyTotalReturnsZero() {
        // 1. Arrange
        final int pageNumber = 1;
        final int totalPages = 0;

        // 2. Exercise
        final int result = Pagination.offsetFor(pageNumber, PAGE_SIZE, totalPages);

        // 3. Assert
        Assertions.assertEquals(0, result);
    }

    @Test
    public void testOffsetForWhenPageIsBelowOneReturnsPageNotFoundException() {
        // 1. Arrange
        final int pageNumber = 0;

        // 2. Exercise
        final Executable offset = () -> Pagination.offsetFor(pageNumber, PAGE_SIZE);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, offset);
    }

    @Test
    public void testOffsetForWhenOffsetOverflowsAnIntReturnsPageNotFoundException() {
        // 1. Arrange
        final int pageNumber = Integer.MAX_VALUE;

        // 2. Exercise
        final Executable offset = () -> Pagination.offsetFor(pageNumber, PAGE_SIZE);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, offset);
    }
}
```
