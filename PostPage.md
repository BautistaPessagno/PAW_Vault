---
title: "PostPage"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostPage.java"]
---

# PostPage

Una página de publicaciones con su número, el total de páginas y si hay anterior y siguiente. Ver [[Paginated listings]].

## Guía de lectura

Datos y dependencias declaradas: `posts`, `pageNumber`, `totalPages`, `hasPrevious`, `hasNext`.

Operaciones para localizar en la fuente: `getPosts`, `getPageNumber`, `getTotalPages`, `isHasPrevious`, `isHasNext`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostSummary]].

Referenciado por: [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublicProfile]], [[SearchResult]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PostPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostPage.java>), líneas 1–41.

```java
package ar.edu.itba.paw.models;

import java.util.List;

public final class PostPage {
    private final List<PostSummary> posts;
    private final int pageNumber;
    private final int totalPages;
    private final boolean hasPrevious;
    private final boolean hasNext;

    // Las direcciones salen del numero de pagina y del total.
    public PostPage(final List<PostSummary> posts, final int pageNumber, final int totalPages) {
        this.posts = List.copyOf(posts);
        this.pageNumber = pageNumber;
        this.totalPages = totalPages;
        this.hasPrevious = pageNumber > 1;
        this.hasNext = pageNumber < totalPages;
    }

    public List<PostSummary> getPosts() {
        return posts;
    }

    public int getPageNumber() {
        return pageNumber;
    }

    // 0 cuando el listado esta vacio.
    public int getTotalPages() {
        return totalPages;
    }

    public boolean isHasPrevious() {
        return hasPrevious;
    }

    public boolean isHasNext() {
        return hasNext;
    }
}
```
