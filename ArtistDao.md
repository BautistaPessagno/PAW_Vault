---
title: "ArtistDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java"]
---

# ArtistDao

Contrato de persistencia de artistas: buscar o crear por nombre normalizado, actualizar el nombre visible y sugerencias. Lo implementa [[ArtistJdbcDao]].

## Guía de lectura

Operaciones para localizar en la fuente: `findOrCreate`, `updateDisplayName`, `findSuggestions`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]].

Referenciado por: [[ArtistJdbcDao]], [[ArtistJdbcDaoTest]], [[ArtistServiceImpl]], [[ArtistServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>), líneas 1–15.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Artist;

import java.util.List;

public interface ArtistDao {
    Artist findOrCreate(String displayName, String normalizedName);

    Artist updateDisplayName(long id, String displayName);

    // normalizedQuery llega ya pasada por SearchText.compact: el ranking se
    // resuelve contra la columna search_phrase, sin traer la tabla entera.
    List<Artist> findSuggestions(String normalizedQuery, int limit);
}
```
