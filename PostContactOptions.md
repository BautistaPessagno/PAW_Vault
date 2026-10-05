---
title: "PostContactOptions"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostContactOptions.java"]
---

# PostContactOptions

Lo que la ficha de un post le ofrece a quien la mira: el [[ContactState]], la Consulta abierta si la hay y si ya está en su carrito. Lo arma [[CartServiceImpl]]. Ver [[Post detail flow]].

## Guía de lectura

Datos y dependencias declaradas: `state`, `openInquiryId`, `inCart`.

Operaciones para localizar en la fuente: `getState`, `isContactable`, `isOwnPost`, `getOpenInquiryId`, `isInCart`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ContactState]].

Referenciado por: [[CartServiceImpl]], [[CartServiceImplTest]], [[PostView]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PostContactOptions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostContactOptions.java>), líneas 1–23.

```java
package ar.edu.itba.paw.models;

import java.util.Optional;

// Lo que la ficha de un Post le ofrece a quien la mira, ya resuelto por CartService.
public final class PostContactOptions {
    private final ContactState state;
    private final Long openInquiryId;
    private final boolean inCart;

    public PostContactOptions(final ContactState state, final Long openInquiryId, final boolean inCart) {
        this.state = state;
        this.openInquiryId = openInquiryId;
        this.inCart = inCart;
    }

    public ContactState getState() { return state; }
    public boolean isContactable() { return state == ContactState.CONTACTABLE; }
    public boolean isOwnPost() { return state == ContactState.OWN_POST; }
    // Solo presente con OPEN_INQUIRY.
    public Optional<Long> getOpenInquiryId() { return Optional.ofNullable(openInquiryId); }
    public boolean isInCart() { return inCart; }
}
```
