---
title: "CartItem"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/CartItem.java"]
---

# CartItem

Un vinilo dentro del carrito, con lo que muestra la pantalla: post, publicante, título, artista, año, imagen opcional y precio actual. Solo llegan los que todavía se pueden consultar. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `postId`, `sellerId`, `sellerUsername`, `title`, `artistName`, `releaseYear`, `coverImageId`, `price`.

Operaciones para localizar en la fuente: `getPostId`, `getSellerId`, `getSellerUsername`, `getTitle`, `getArtistName`, `getReleaseYear`, `getCoverImageId`, `getPrice`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartItemDao]], [[CartItemJdbcDao]], [[CartItemJdbcDaoTest]], [[CartSellerGroup]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/CartItem.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartItem.java>), líneas 1–41.

```java
package ar.edu.itba.paw.models;

import java.util.Optional;

/*
 * Un Post en el carrito de una Cuenta, con lo que muestra la pantalla de envio. Solo llegan
 * los que todavia se pueden consultar: disponibles, ajenos y sin una Consulta abierta del comprador.
 * El precio es el actual del Post; la Consulta lo congela recien al enviarse.
 */
public final class CartItem {
    private final long postId;
    private final long sellerId;
    private final String sellerUsername;
    private final String title;
    private final String artistName;
    private final int releaseYear;
    private final Long coverImageId;
    private final int price;

    public CartItem(final long postId, final long sellerId, final String sellerUsername, final String title,
                    final String artistName, final int releaseYear, final Long coverImageId, final int price) {
        this.postId = postId;
        this.sellerId = sellerId;
        this.sellerUsername = sellerUsername;
        this.title = title;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
        this.coverImageId = coverImageId;
        this.price = price;
    }

    public long getPostId() { return postId; }
    public long getSellerId() { return sellerId; }
    public String getSellerUsername() { return sellerUsername; }
    public String getTitle() { return title; }
    public String getArtistName() { return artistName; }
    public int getReleaseYear() { return releaseYear; }
    // Vacio si ni el Post ni su album tienen imagen.
    public Optional<Long> getCoverImageId() { return Optional.ofNullable(coverImageId); }
    public int getPrice() { return price; }
}
```
