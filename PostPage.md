---
title: "PostPage"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostPage.java"]
---

# PostPage

Immutable page of [[PostSummary]] values. One constructor takes a known total (the profile listing) and derives hasPrevious/hasNext from it; the other has no total (catalog search looks one row ahead) and sets totalKnown=false with explicit direction flags. getTotalPages is meaningful only when isTotalKnown is true.

## Connections

Project types referenced: [[PostSummary]].

Referenced by: [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[SearchResult]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostPage.java, lines 1–59](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostPage.java>)

```java
package ar.edu.itba.paw.models;

import java.util.List;

public final class PostPage {
    private final List<PostSummary> posts;
    private final int pageNumber;
    private final int totalPages;
    private final boolean totalKnown;
    private final boolean hasPrevious;
    private final boolean hasNext;

    // Pagina con total conocido: las direcciones salen del numero de pagina.
    public PostPage(final List<PostSummary> posts, final int pageNumber, final int totalPages) {
        this(posts, pageNumber, totalPages, true, pageNumber > 1, pageNumber < totalPages);
    }

    // Pagina sin total (la busqueda del catalogo mira una fila de mas en lugar de contar):
    // totalKnown queda en false y totalPages no significa nada.
    public PostPage(final List<PostSummary> posts, final int pageNumber,
                    final boolean hasPrevious, final boolean hasNext) {
        this(posts, pageNumber, 0, false, hasPrevious, hasNext);
    }

    private PostPage(final List<PostSummary> posts, final int pageNumber, final int totalPages,
                     final boolean totalKnown, final boolean hasPrevious, final boolean hasNext) {
        this.posts = List.copyOf(posts);
        this.pageNumber = pageNumber;
        this.totalPages = totalPages;
        this.totalKnown = totalKnown;
        this.hasPrevious = hasPrevious;
        this.hasNext = hasNext;
    }

    public List<PostSummary> getPosts() {
        return posts;
    }

    public int getPageNumber() {
        return pageNumber;
    }

    // Solo tiene sentido cuando isTotalKnown(): 0 tambien es el total de un listado vacio.
    public int getTotalPages() {
        return totalPages;
    }

    public boolean isTotalKnown() {
        return totalKnown;
    }

    public boolean isHasPrevious() {
        return hasPrevious;
    }

    public boolean isHasNext() {
        return hasNext;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
