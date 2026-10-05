---
title: "CartSellerGroup"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/CartSellerGroup.java"]
---

# CartSellerGroup

Los vinilos del carrito que son de un mismo publicante. Al enviar, a ese publicante le llega un solo correo. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `sellerId`, `sellerUsername`, `items`.

Operaciones para localizar en la fuente: `getSellerId`, `getSellerUsername`, `getItems`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartItem]].

Referenciado por: [[Cart]], [[CartServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/CartSellerGroup.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartSellerGroup.java>), líneas 1–20.

```java
package ar.edu.itba.paw.models;

import java.util.List;

// Los vinilos del carrito que son de un mismo Publicante: al enviar, le llega un solo correo.
public final class CartSellerGroup {
    private final long sellerId;
    private final String sellerUsername;
    private final List<CartItem> items;

    public CartSellerGroup(final long sellerId, final String sellerUsername, final List<CartItem> items) {
        this.sellerId = sellerId;
        this.sellerUsername = sellerUsername;
        this.items = List.copyOf(items);
    }

    public long getSellerId() { return sellerId; }
    public String getSellerUsername() { return sellerUsername; }
    public List<CartItem> getItems() { return items; }
}
```
