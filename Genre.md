---
title: "Genre"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Genre.java"]
---

# Genre

Quince géneros del catálogo, incluido `OTHER`. Se guarda en el álbum, es obligatorio al publicar y la base lo refuerza con un `CHECK`. El nombre visible sale de i18n.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[Album]], [[AlbumDao]], [[AlbumJdbcDao]], [[AlbumJdbcDaoTest]], [[AlbumService]], [[AlbumServiceImpl]], [[AlbumServiceImplTest]], [[CatalogFilterForm]], [[LandingController]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]], [[PublishController]], [[PublishForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Genre.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Genre.java>), líneas 1–19.

```java
package ar.edu.itba.paw.models;

public enum Genre {
    ROCK,
    POP,
    JAZZ,
    BLUES,
    SOUL_FUNK,
    HIP_HOP,
    ELECTRONIC,
    CLASSICAL,
    TANGO,
    FOLKLORE,
    CUMBIA,
    REGGAE,
    METAL,
    PUNK,
    OTHER
}
```
