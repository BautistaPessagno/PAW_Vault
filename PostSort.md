---
title: "PostSort"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSort.java"]
---

# PostSort

Los diez órdenes del catálogo. [[PostJdbcDao]] traduce cada valor a un `ORDER BY` fijo, así al SQL nunca entra texto del usuario.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CatalogFilterForm]], [[LandingController]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostServiceImpl]], [[PostServiceImplTest]], [[SearchResult]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PostSort.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSort.java>), líneas 1–15.

```java
package ar.edu.itba.paw.models;

// Criterios de orden del listado de publicaciones. NEWEST es el default de la landing.
public enum PostSort {
    NEWEST,
    OLDEST,
    PRICE_ASC,
    PRICE_DESC,
    TITLE_ASC,
    TITLE_DESC,
    ARTIST_ASC,
    ARTIST_DESC,
    RELEASE_YEAR_DESC,
    RELEASE_YEAR_ASC
}
```
