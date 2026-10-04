---
title: "SearchSuggestion"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java"]
---

# SearchSuggestion

Una sugerencia del buscador: tipo, valor y, para un álbum, el artista.

## Guía de lectura

Datos y dependencias declaradas: `type`, `value`, `artistName`.

Operaciones para localizar en la fuente: `getType`, `getValue`, `getArtistName`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[SearchSuggestionType]].

Referenciado por: [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[SearchSuggestionController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java>), líneas 1–25.

```java
package ar.edu.itba.paw.models;

public class SearchSuggestion {
    private final SearchSuggestionType type;
    private final String value;
    private final String artistName;

    public SearchSuggestion(final SearchSuggestionType type, final String value, final String artistName) {
        this.type = type;
        this.value = value;
        this.artistName = artistName;
    }

    public SearchSuggestionType getType() {
        return type;
    }

    public String getValue() {
        return value;
    }

    public String getArtistName() {
        return artistName;
    }
}
```
