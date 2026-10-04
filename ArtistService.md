---
title: "ArtistService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java"]
---

# ArtistService

Contrato del catálogo de artistas: buscar o crear por identidad normalizada, resolver al editar y sugerencias para el autocompletado.

## Guía de lectura

Operaciones para localizar en la fuente: `findOrCreate`, `resolveForEdit`, `findSuggestions`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]].

Referenciado por: [[ArtistServiceImpl]], [[ArtistSuggestionController]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>), líneas 1–13.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistService {
    Artist findOrCreate(String name);

    Artist resolveForEdit(String name);

    List<Artist> findSuggestions(String query);
}
```
