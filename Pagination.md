---
title: "Pagination"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/Pagination.java"]
---

# Pagination

Package-private page arithmetic shared by the services. pagesFor rounds up. offsetFor with a known total rejects pages past it, while page one always exists; offsetFor without a total rejects pages below one and offsets beyond Integer.MAX_VALUE. Violations raise [[PageNotFoundException]].

## Connections

Project types referenced: [[PageNotFoundException]].

Referenced by: [[InquiryServiceImpl]], [[PaginationTest]], [[PostServiceImpl]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/Pagination.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>)

```java
package ar.edu.itba.paw.services;

// Aritmetica de paginado compartida por los services que listan de a paginas. Una sola
// regla para "pagina fuera de rango": la pagina 1 siempre existe, aunque este vacia; con el
// total conocido, cualquier otra tiene que caer dentro de el.
final class Pagination {

    private Pagination() {
    }

    // Paginas necesarias para un total; 0 cuando no hay filas.
    static int pagesFor(final int total, final int pageSize) {
        return (total + pageSize - 1) / pageSize;
    }

    // Offset de una pagina cuando el total es conocido.
    static int offsetFor(final int pageNumber, final int pageSize, final int totalPages) {
        if (pageNumber > 1 && pageNumber > totalPages) {
            throw new PageNotFoundException();
        }
        return offsetFor(pageNumber, pageSize);
    }

    // Offset de una pagina cuando el total no se conoce (la busqueda del catalogo mira una
    // fila de mas en lugar de contar).
    static int offsetFor(final int pageNumber, final int pageSize) {
        if (pageNumber < 1) {
            throw new PageNotFoundException();
        }
        final long offset = ((long) pageNumber - 1L) * pageSize;
        if (offset > Integer.MAX_VALUE) {
            throw new PageNotFoundException();
        }
        return (int) offset;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
