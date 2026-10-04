---
title: "CartCheckoutResult"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/CartCheckoutResult.java"]
---

# CartCheckoutResult

Resultado de enviar el carrito: cuántas Consultas se crearon y cuántos vinilos se omitieron porque dejaron de estar disponibles. La bandeja de enviadas lo muestra como aviso. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `sentCount`, `skippedCount`.

Operaciones para localizar en la fuente: `getSentCount`, `getSkippedCount`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartController]], [[CartService]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/CartCheckoutResult.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartCheckoutResult.java>), líneas 1–16.

```java
package ar.edu.itba.paw.models;

// Lo que dejo el envio del carrito. Las omitidas son Posts que se reservaron, vendieron o
// consultaron entre que se abrio el carrito y se envio: no se mandan y siguen en el carrito.
public final class CartCheckoutResult {
    private final int sentCount;
    private final int skippedCount;

    public CartCheckoutResult(final int sentCount, final int skippedCount) {
        this.sentCount = sentCount;
        this.skippedCount = skippedCount;
    }

    public int getSentCount() { return sentCount; }
    public int getSkippedCount() { return skippedCount; }
}
```
