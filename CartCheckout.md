---
title: "CartCheckout"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/CartCheckout.java"]
---

# CartCheckout

Lo que necesita la pantalla del carrito: el [[Cart]] y las [[ShippingOptions]] del comprador. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `cart`, `shipping`.

Operaciones para localizar en la fuente: `getCart`, `getShipping`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Cart]], [[ShippingOptions]].

Referenciado por: [[CartController]], [[CartService]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/CartCheckout.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartCheckout.java>), líneas 1–15.

```java
package ar.edu.itba.paw.models;

// La pantalla de envio del carrito: lo que se va a consultar y a donde se puede mandar.
public final class CartCheckout {
    private final Cart cart;
    private final ShippingOptions shipping;

    public CartCheckout(final Cart cart, final ShippingOptions shipping) {
        this.cart = cart;
        this.shipping = shipping;
    }

    public Cart getCart() { return cart; }
    public ShippingOptions getShipping() { return shipping; }
}
```
