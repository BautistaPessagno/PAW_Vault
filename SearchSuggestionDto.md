---
title: "SearchSuggestionDto"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java"]
---

# SearchSuggestionDto

Forma JSON de una sugerencia del buscador: `value`, `type`, `typeLabel` y `detail`. Separa el contrato JSON del modelo de dominio.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[SearchSuggestionController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java>), líneas 1–8.

```java
package ar.edu.itba.paw.webapp.dto;

/*
 * Contrato JSON de GET /search/suggestions. typeLabel ya viene traducido al idioma del
 * request; detail es el artista de un album y null para una sugerencia de artista.
 */
public record SearchSuggestionDto(String value, String type, String typeLabel, String detail) {
}
```
