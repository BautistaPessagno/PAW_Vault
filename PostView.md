---
title: "PostView"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostView.java"]
---

# PostView

La pantalla de un post: su [[PostDetail]] y las [[PostContactOptions]] de quien mira. Lo devuelve `CartService.findPostView`.

## Guía de lectura

Datos y dependencias declaradas: `detail`, `contact`.

Operaciones para localizar en la fuente: `getDetail`, `getContact`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostContactOptions]], [[PostDetail]].

Referenciado por: [[CartService]], [[CartServiceImpl]], [[CartServiceImplTest]], [[PostController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PostView.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostView.java>), líneas 1–15.

```java
package ar.edu.itba.paw.models;

// La pantalla de un Post: su ficha y lo que le ofrece a quien la mira para consultarlo.
public final class PostView {
    private final PostDetail detail;
    private final PostContactOptions contact;

    public PostView(final PostDetail detail, final PostContactOptions contact) {
        this.detail = detail;
        this.contact = contact;
    }

    public PostDetail getDetail() { return detail; }
    public PostContactOptions getContact() { return contact; }
}
```
