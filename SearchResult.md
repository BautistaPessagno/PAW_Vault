---
title: "SearchResult"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchResult.java"]
---

# SearchResult

Resultado de una búsqueda: la query ya normalizada, los criterios tal como el service los aplicó, la página y el total de coincidencias. La vista muestra como activo solo lo que el service aplicó de verdad.

## Guía de lectura

Datos y dependencias declaradas: `query`, `criteria`, `page`, `total`.

Operaciones para localizar en la fuente: `getQuery`, `getCriteria`, `getSort`, `getPage`, `getTotal`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostPage]], [[PostSearchCriteria]], [[PostSort]].

Referenciado por: [[LandingController]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/SearchResult.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchResult.java>), líneas 1–45.

```java
package ar.edu.itba.paw.models;

import java.util.Objects;

// Resultado de una busqueda de publicaciones: la query ya normalizada (null si estaba vacia), los
// criterios tal como se aplicaron y las publicaciones paginadas. Salen de aca para que la vista
// muestre como activo solo lo que el service aplico de verdad.
public final class SearchResult {
    private final String query;
    // Los filtros ya normalizados: un valor fuera de rango queda en null y el orden nunca es
    // null (sin orden pedido, el default que eligio el service).
    private final PostSearchCriteria criteria;
    private final PostPage page;
    // Coincidencias en todas las paginas, no solo en la actual.
    private final int total;

    public SearchResult(final String query, final PostSearchCriteria criteria, final PostPage page,
                        final int total) {
        this.query = query;
        this.criteria = Objects.requireNonNull(criteria);
        Objects.requireNonNull(criteria.getSort());
        this.page = page;
        this.total = total;
    }

    public String getQuery() {
        return query;
    }

    public PostSearchCriteria getCriteria() {
        return criteria;
    }

    public PostSort getSort() {
        return criteria.getSort();
    }

    public PostPage getPage() {
        return page;
    }

    public int getTotal() {
        return total;
    }
}
```
