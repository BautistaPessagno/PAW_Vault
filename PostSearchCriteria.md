---
title: "PostSearchCriteria"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java"]
---

# PostSearchCriteria

Filtros combinables del catálogo: texto, orden, género, condición, artista, año y rango de precio. Un campo nulo es un filtro que no se aplica. Ver [[Landing flow]].

## Guía de lectura

Datos y dependencias declaradas: `query`, `sort`, `genre`, `condition`, `artistId`, `releaseYear`, `minPrice`, `maxPrice`.

Operaciones para localizar en la fuente: `getQuery`, `getSort`, `getGenre`, `getCondition`, `getArtistId`, `getReleaseYear`, `getMinPrice`, `getMaxPrice`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[Genre]], [[PostSort]].

Referenciado por: [[CatalogFilterForm]], [[LandingController]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[SearchResult]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java>), líneas 1–36.

```java
package ar.edu.itba.paw.models;

// Filtros combinables del catalogo de publicaciones. Un campo en null es un filtro
// que no se aplica: el DAO lo saltea al armar el WHERE.
public final class PostSearchCriteria {
    private final String query;
    private final PostSort sort;
    private final Genre genre;
    private final Condition condition;
    private final Long artistId;
    private final Integer releaseYear;
    private final Integer minPrice;
    private final Integer maxPrice;

    public PostSearchCriteria(final String query, final PostSort sort, final Genre genre,
                              final Condition condition, final Long artistId, final Integer releaseYear,
                              final Integer minPrice, final Integer maxPrice) {
        this.query = query;
        this.sort = sort;
        this.genre = genre;
        this.condition = condition;
        this.artistId = artistId;
        this.releaseYear = releaseYear;
        this.minPrice = minPrice;
        this.maxPrice = maxPrice;
    }

    public String getQuery() { return query; }
    public PostSort getSort() { return sort; }
    public Genre getGenre() { return genre; }
    public Condition getCondition() { return condition; }
    public Long getArtistId() { return artistId; }
    public Integer getReleaseYear() { return releaseYear; }
    public Integer getMinPrice() { return minPrice; }
    public Integer getMaxPrice() { return maxPrice; }
}
```
