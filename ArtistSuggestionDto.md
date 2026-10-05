---
title: "ArtistSuggestionDto"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java"]
---

# ArtistSuggestionDto

Forma JSON de una sugerencia de artista: solo `value`.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ArtistSuggestionController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java>), líneas 1–5.

```java
package ar.edu.itba.paw.webapp.dto;

// Contrato JSON de GET /artists/suggestions.
public record ArtistSuggestionDto(String value) {
}
```
