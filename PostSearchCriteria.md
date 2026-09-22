---
title: "PostSearchCriteria"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java"]
---

# PostSearchCriteria

Criteria passed from the landing controller through the service to the DAO: query, sort, genre, condition, artist ID, release year and minimum/maximum price. A null optional filter means no restriction. [[PostServiceImpl]] normalizes input before SQL. artistId no longer has a visible control; it survives only through URLs and hidden inputs.

## Connections

Project types referenced: [[Condition]], [[Genre]], [[PostSort]].

Referenced by: [[LandingController]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
