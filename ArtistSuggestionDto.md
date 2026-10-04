---
title: "ArtistSuggestionDto"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
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

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java>), líneas 1–5.

```java
package ar.edu.itba.paw.webapp.dto;

// Contrato JSON de GET /artists/suggestions.
public record ArtistSuggestionDto(String value) {
}
```
