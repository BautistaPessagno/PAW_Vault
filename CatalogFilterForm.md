---
title: "CatalogFilterForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java"]
---

# CatalogFilterForm

Filtros del catálogo ligados desde la URL: texto, orden, género, condición, artista, año y precios. `toCriteria` los pasa a [[PostSearchCriteria]].

## Guía de lectura

Datos y dependencias declaradas: `q`, `sort`, `genre`, `condition`, `artistId`, `year`, `minPrice`, `maxPrice`.

Operaciones para localizar en la fuente: `toCriteria`, `getQ`, `setQ`, `getSort`, `setSort`, `getGenre`, `setGenre`, `getCondition`, `setCondition`, `getArtistId`, `setArtistId`, `getYear`, `setYear`, `getMinPrice`, `setMinPrice`, `getMaxPrice`, `setMaxPrice`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[Genre]], [[PostSearchCriteria]], [[PostSort]], [[ValidCatalogFilters]].

Referenciado por: [[CatalogFilterValidator]], [[LandingController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java>), líneas 1–88.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.webapp.validation.ValidCatalogFilters;

@ValidCatalogFilters
public class CatalogFilterForm {

    private String q;
    private PostSort sort;
    private Genre genre;
    private Condition condition;
    private Long artistId;
    private Integer year;
    private Integer minPrice;
    private Integer maxPrice;

    public PostSearchCriteria toCriteria() {
        return new PostSearchCriteria(q, sort, genre, condition, artistId, year, minPrice, maxPrice);
    }

    public String getQ() {
        return q;
    }

    public void setQ(final String q) {
        this.q = q;
    }

    public PostSort getSort() {
        return sort;
    }

    public void setSort(final PostSort sort) {
        this.sort = sort;
    }

    public Genre getGenre() {
        return genre;
    }

    public void setGenre(final Genre genre) {
        this.genre = genre;
    }

    public Condition getCondition() {
        return condition;
    }

    public void setCondition(final Condition condition) {
        this.condition = condition;
    }

    public Long getArtistId() {
        return artistId;
    }

    public void setArtistId(final Long artistId) {
        this.artistId = artistId;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(final Integer year) {
        this.year = year;
    }

    public Integer getMinPrice() {
        return minPrice;
    }

    public void setMinPrice(final Integer minPrice) {
        this.minPrice = minPrice;
    }

    public Integer getMaxPrice() {
        return maxPrice;
    }

    public void setMaxPrice(final Integer maxPrice) {
        this.maxPrice = maxPrice;
    }
}
```
