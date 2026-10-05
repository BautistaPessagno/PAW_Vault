---
title: "FilterCounts"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/FilterCounts.java"]
---

# FilterCounts

Los números de los chips de filtro de un listado: un mapa valor → cantidad y el total. Existe porque EL no llama métodos con argumentos: la vista lee `counts[valor]`, y un valor ausente se muestra como 0. Lo usan las bandejas y "Mis publicaciones". Ver [[Status filters flow]].

## Guía de lectura

Datos y dependencias declaradas: `counts`, `total`.

Operaciones para localizar en la fuente: `getCounts`, `getTotal`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryController]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryStatusFilter]], [[InquiryStatusFilterTest]], [[PostService]], [[PostServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/FilterCounts.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/FilterCounts.java>), líneas 1–18.

```java
package ar.edu.itba.paw.models;

import java.util.Map;

// Conteos de los chips de filtro de un listado. EL no llama metodos con argumentos: la vista
// lee counts[valor]. Un valor sin elementos no esta en el mapa y la vista lo muestra como 0.
public final class FilterCounts<K> {
    private final Map<K, Integer> counts;
    private final int total;

    public FilterCounts(final Map<K, Integer> counts) {
        this.counts = Map.copyOf(counts);
        this.total = counts.values().stream().mapToInt(Integer::intValue).sum();
    }

    public Map<K, Integer> getCounts() { return counts; }
    public int getTotal() { return total; }
}
```
