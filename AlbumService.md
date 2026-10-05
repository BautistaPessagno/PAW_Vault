---
title: "AlbumService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java"]
---

# AlbumService

Contrato del catálogo de álbumes: buscar o crear por identidad, y resolver al editar actualizando título y género.

## Guía de lectura

Operaciones para localizar en la fuente: `findOrCreate`, `resolveForEdit`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[Genre]].

Referenciado por: [[AlbumServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>), líneas 1–10.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;

public interface AlbumService {
    Album findOrCreate(String title, long artistId, int releaseYear, Genre genre);

    Album resolveForEdit(String title, long artistId, int releaseYear, Genre genre);
}
```
