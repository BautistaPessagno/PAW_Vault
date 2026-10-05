---
title: "ContactRulesTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ContactRulesTest.java"]
---

# ContactRulesTest

Tests de `ContactRules` en `services`: 6 casos declarados. Cubre: las combinaciones de estado del post, dueño y consulta abierta, con y sin sesión. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `BUYER_ID`, `SELLER_ID`.

Casos declarados: 6.

- `testStateOfWhenPostIsAvailableAndForeignReturnsContactable`
- `testStateOfWhenBuyerHasOpenInquiryOnReservedPostReturnsOpenInquiry`
- `testStateOfWhenPostIsSoldReturnsUnavailable`
- `testStateOfWhenBuyerOwnsAvailablePostReturnsOwnPost`
- `testStateForAnonymousWhenPostIsAvailableReturnsContactable`
- `testStateForAnonymousWhenPostIsReservedReturnsUnavailable`

## Conexiones

Referencias estáticas a tipos del proyecto: [[ContactRules]], [[ContactState]], [[PostStatus]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/ContactRulesTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ContactRulesTest.java>), líneas 1–84.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.ContactState;
import ar.edu.itba.paw.models.PostStatus;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class ContactRulesTest {

    private static final long BUYER_ID = 2;
    private static final long SELLER_ID = 1;

    @Test
    public void testStateOfWhenPostIsAvailableAndForeignReturnsContactable() {
        // 1. Arrange
        final PostStatus status = PostStatus.AVAILABLE;

        // 2. Exercise
        final ContactState result = ContactRules.stateOf(status, SELLER_ID, BUYER_ID, false);

        // 3. Assert
        Assertions.assertEquals(ContactState.CONTACTABLE, result);
    }

    @Test
    public void testStateOfWhenBuyerHasOpenInquiryOnReservedPostReturnsOpenInquiry() {
        // 1. Arrange
        final PostStatus status = PostStatus.RESERVED;

        // 2. Exercise
        final ContactState result = ContactRules.stateOf(status, SELLER_ID, BUYER_ID, true);

        // 3. Assert
        Assertions.assertEquals(ContactState.OPEN_INQUIRY, result);
    }

    @Test
    public void testStateOfWhenPostIsSoldReturnsUnavailable() {
        // 1. Arrange
        final PostStatus status = PostStatus.SOLD;

        // 2. Exercise
        final ContactState result = ContactRules.stateOf(status, SELLER_ID, BUYER_ID, false);

        // 3. Assert
        Assertions.assertEquals(ContactState.UNAVAILABLE, result);
    }

    @Test
    public void testStateOfWhenBuyerOwnsAvailablePostReturnsOwnPost() {
        // 1. Arrange
        final PostStatus status = PostStatus.AVAILABLE;

        // 2. Exercise
        final ContactState result = ContactRules.stateOf(status, BUYER_ID, BUYER_ID, false);

        // 3. Assert
        Assertions.assertEquals(ContactState.OWN_POST, result);
    }

    @Test
    public void testStateForAnonymousWhenPostIsAvailableReturnsContactable() {
        // 1. Arrange
        final PostStatus status = PostStatus.AVAILABLE;

        // 2. Exercise
        final ContactState result = ContactRules.stateForAnonymous(status);

        // 3. Assert
        Assertions.assertEquals(ContactState.CONTACTABLE, result);
    }

    @Test
    public void testStateForAnonymousWhenPostIsReservedReturnsUnavailable() {
        // 1. Arrange
        final PostStatus status = PostStatus.RESERVED;

        // 2. Exercise
        final ContactState result = ContactRules.stateForAnonymous(status);

        // 3. Assert
        Assertions.assertEquals(ContactState.UNAVAILABLE, result);
    }
}
```
