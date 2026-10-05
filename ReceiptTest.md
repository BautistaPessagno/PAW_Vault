---
title: "ReceiptTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ReceiptTest.java"]
---

# ReceiptTest

Tests de `Receipt` en `services`: 2 casos declarados. Cubre: que [[Receipt]] no comparta su arreglo de bytes: cambiar el original o el devuelto no altera el comprobante. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

Casos declarados: 2.

- `testGetDataWhenOriginalBytesChangeReturnsOriginalReceipt`
- `testGetDataWhenReturnedBytesChangeReturnsOriginalReceipt`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Receipt]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/ReceiptTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ReceiptTest.java>), líneas 1–34.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Receipt;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class ReceiptTest {

    @Test
    public void testGetDataWhenOriginalBytesChangeReturnsOriginalReceipt() {
        // 1. Arrange
        final byte[] original = {1, 2, 3};
        final Receipt receipt = new Receipt("application/pdf", original);

        // 2. Exercise
        original[0] = 9;

        // 3. Assert
        Assertions.assertArrayEquals(new byte[]{1, 2, 3}, receipt.getData());
    }

    @Test
    public void testGetDataWhenReturnedBytesChangeReturnsOriginalReceipt() {
        // 1. Arrange
        final Receipt receipt = new Receipt("application/pdf", new byte[]{1, 2, 3});

        // 2. Exercise
        final byte[] returned = receipt.getData();
        returned[1] = 9;

        // 3. Assert
        Assertions.assertArrayEquals(new byte[]{1, 2, 3}, receipt.getData());
    }
}
```
