---
title: "Pagination"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/Pagination.java"]
---

# Pagination

Aritmética de páginas compartida: páginas para un total y offset de una página. Una sola regla para "fuera de rango": la página 1 siempre existe; cualquier otra tiene que caer dentro del total. Ver [[Paginated listings]].

## Guía de lectura

Operaciones para localizar en la fuente: `pagesFor`, `offsetFor`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PageNotFoundException]].

Referenciado por: [[InquiryServiceImpl]], [[PaginationTest]], [[PostServiceImpl]], [[ReviewServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/Pagination.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>), líneas 1–35.

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

    // Offset de una pagina sin mirar el total: solo descarta numeros que no dan un offset valido.
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
