---
title: "InquiryPage"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java"]
---

# InquiryPage

Una página de la bandeja: grupos, número de página y total de páginas. Se pagina por publicación para que un grupo no quede partido. Ver [[Paginated listings]].

## Guía de lectura

Datos y dependencias declaradas: `groups`, `pageNumber`, `totalPages`.

Operaciones para localizar en la fuente: `getGroups`, `getPageNumber`, `getTotalPages`, `isHasPrevious`, `isHasNext`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquiryGroup]].

Referenciado por: [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java>), líneas 1–37.

```java
package ar.edu.itba.paw.models;

import java.util.List;

// Pagina de la bandeja de consultas: se pagina por publicacion, no por consulta, para que
// un grupo nunca quede partido entre dos paginas.
public final class InquiryPage {
    private final List<InquiryGroup> groups;
    private final int pageNumber;
    private final int totalPages;

    public InquiryPage(final List<InquiryGroup> groups, final int pageNumber, final int totalPages) {
        this.groups = List.copyOf(groups);
        this.pageNumber = pageNumber;
        this.totalPages = totalPages;
    }

    public List<InquiryGroup> getGroups() {
        return groups;
    }

    public int getPageNumber() {
        return pageNumber;
    }

    public int getTotalPages() {
        return totalPages;
    }

    public boolean isHasPrevious() {
        return pageNumber > 1;
    }

    public boolean isHasNext() {
        return pageNumber < totalPages;
    }
}
```
