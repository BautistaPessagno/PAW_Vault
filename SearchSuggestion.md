---
title: "SearchSuggestion"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java>), líneas 1–25.

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
