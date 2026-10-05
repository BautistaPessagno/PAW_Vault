---
title: "PostSort"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PostSort.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSort.java>), líneas 1–15.

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
