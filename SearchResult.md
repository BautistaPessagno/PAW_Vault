---
title: "SearchResult"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchResult.java"]
---

# SearchResult

Normalized query plus an immutable copy of the matching PostSummary list. It contains no total count, page number or normalized filter object.

## Connections

Project types referenced: [[PostSummary]].

Referenced by: [[LandingController]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/SearchResult.java, lines 1–23](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchResult.java>)

```java
package ar.edu.itba.paw.models;

import java.util.List;

// Resultado de una busqueda de publicaciones: la query ya normalizada (null si estaba vacia) y las
// publicaciones encontradas. La query sale de aca para que la vista no tenga que re-normalizarla.
public class SearchResult {
    private final String query;
    private final List<PostSummary> posts;

    public SearchResult(final String query, final List<PostSummary> posts) {
        this.query = query;
        this.posts = List.copyOf(posts);
    }

    public String getQuery() {
        return query;
    }

    public List<PostSummary> getPosts() {
        return posts;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
