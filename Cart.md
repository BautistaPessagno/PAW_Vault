---
title: "Cart"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Cart.java"]
---

# Cart

El carrito tal como se muestra: los grupos por publicante, la cantidad de vinilos y el total con los precios actuales. No es una entidad de venta; los totales llegan calculados desde [[CartServiceImpl]]. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `groups`, `itemCount`, `totalPrice`.

Operaciones para localizar en la fuente: `getGroups`, `getItemCount`, `getSellerCount`, `getTotalPrice`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartSellerGroup]].

Referenciado por: [[CartCheckout]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Cart.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Cart.java>), líneas 1–26.

```java
package ar.edu.itba.paw.models;

import java.util.List;

/*
 * El carrito de una Cuenta: los Posts que eligio para consultar juntos, agrupados por
 * Publicante. No es una entidad de venta; cada Consulta enviada sale del carrito. Los totales
 * llegan calculados desde CartService.
 */
public final class Cart {
    private final List<CartSellerGroup> groups;
    private final int itemCount;
    private final long totalPrice;

    public Cart(final List<CartSellerGroup> groups, final int itemCount, final long totalPrice) {
        this.groups = List.copyOf(groups);
        this.itemCount = itemCount;
        this.totalPrice = totalPrice;
    }

    public List<CartSellerGroup> getGroups() { return groups; }
    public int getItemCount() { return itemCount; }
    public int getSellerCount() { return groups.size(); }
    // Con los precios actuales: lo que costaria si se concretan todas las Consultas.
    public long getTotalPrice() { return totalPrice; }
}
```
