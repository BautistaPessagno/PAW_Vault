---
title: "SearchSuggestionType"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java"]
---

# SearchSuggestionType

Tipo de sugerencia: `ARTIST` o `ALBUM`. [[PostJdbcDao]] lo emite como literal SQL.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImplTest]], [[SearchSuggestion]], [[SearchSuggestionController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java>), líneas 1–6.

```java
package ar.edu.itba.paw.models;

public enum SearchSuggestionType {
    ARTIST,
    ALBUM
}
```
