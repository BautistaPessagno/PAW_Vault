---
title: "PaginationTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java"]
---

# PaginationTest

Plain JUnit tests for [[Pagination]]: page counts for empty, exact and overflowing totals, offsets inside a total, and PageNotFoundException for pages past the total, below one or overflowing an int. No Spring context or mock is involved. Source evidence only; no new Maven execution is claimed.

Test methods in this revision:

- `testPagesForWhenTotalIsZeroReturnsZero`
- `testPagesForWhenTotalIsAMultipleOfThePageSizeReturnsExactPages`
- `testPagesForWhenTotalOverflowsAPageReturnsOneMorePage`
- `testOffsetForWhenPageIsWithinTheTotalReturnsOffset`
- `testOffsetForWhenPageIsPastTheTotalReturnsPageNotFoundException`
- `testOffsetForWhenFirstPageOfAnEmptyTotalReturnsZero`
- `testOffsetForWhenPageIsBelowOneReturnsPageNotFoundException`
- `testOffsetForWhenOffsetOverflowsAnIntReturnsPageNotFoundException`

## Connections

Project types referenced: [[PageNotFoundException]], [[Pagination]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java, lines 1–109](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
