---
title: "SearchSuggestionDto"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java>), líneas 1–8.

```java
package ar.edu.itba.paw.webapp.dto;

/*
 * Contrato JSON de GET /search/suggestions. typeLabel ya viene traducido al idioma del
 * request; detail es el artista de un album y null para una sugerencia de artista.
 */
public record SearchSuggestionDto(String value, String type, String typeLabel, String detail) {
}
```
