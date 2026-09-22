---
title: "SearchResult"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchResult.java"]
---

# SearchResult

Normalized query (null when blank) plus a [[PostPage]] of results. The query travels here so the view does not re-normalize it. The page carries direction flags for catalog pagination but no total count.

## Connections

Project types referenced: [[PostPage]].

Referenced by: [[LandingController]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/SearchResult.java, lines 1–21](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchResult.java>)

```java
package ar.edu.itba.paw.models;

// Resultado de una busqueda de publicaciones: la query ya normalizada (null si estaba vacia) y las
// publicaciones paginadas. La query sale de aca para que la vista no tenga que re-normalizarla.
public final class SearchResult {
    private final String query;
    private final PostPage page;

    public SearchResult(final String query, final PostPage page) {
        this.query = query;
        this.page = page;
    }

    public String getQuery() {
        return query;
    }

    public PostPage getPage() {
        return page;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
