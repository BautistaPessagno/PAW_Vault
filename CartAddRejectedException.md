---
title: "CartAddRejectedException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/CartAddRejectedException.java"]
---

# CartAddRejectedException

El post no se pudo agregar al carrito. Lleva el post y el motivo (`OWN_POST`, `UNAVAILABLE`, `ALREADY_IN_CART`, `CART_FULL`) para volver a su ficha con el aviso.

## Guía de lectura

Datos y dependencias declaradas: `postId`, `reason`.

Operaciones para localizar en la fuente: `getPostId`, `getReason`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartExceptionAdvice]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/CartAddRejectedException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/CartAddRejectedException.java>), líneas 1–29.

```java
package ar.edu.itba.paw.services;

// El Post no se pudo agregar al carrito. Lleva el post para volver a su ficha con el motivo.
public class CartAddRejectedException extends RuntimeException {

    public enum Reason {
        OWN_POST,
        UNAVAILABLE,
        ALREADY_IN_CART,
        // El carrito ya tiene CartService.MAX_ITEMS vinilos que se pueden consultar.
        CART_FULL
    }

    private final long postId;
    private final Reason reason;

    public CartAddRejectedException(final long postId, final Reason reason) {
        this.postId = postId;
        this.reason = reason;
    }

    public long getPostId() {
        return postId;
    }

    public Reason getReason() {
        return reason;
    }
}
```
