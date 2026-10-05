---
title: "VinylInputRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java"]
---

# VinylInputRules

Límites numéricos compartidos por el catálogo y la carga: años entre 1000 y 9999 y no futuros, precios entre 1 y 99.999.999, rango de precios ordenado y prensado no anterior al lanzamiento.

## Guía de lectura

Datos y dependencias declaradas: `MIN_YEAR`, `MAX_YEAR`, `MIN_PRICE`, `MAX_PRICE`.

Operaciones para localizar en la fuente: `currentYear`, `classifyYear`, `classifyPrice`, `isPriceRangeOrdered`, `isPressingYearOrdered`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CatalogFilterValidator]], [[LandingController]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]], [[PublishFormValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java>), líneas 1–54.

```java
package ar.edu.itba.paw.models;

import java.time.Year;

// Reglas numericas compartidas por el catalogo y por la carga de publicaciones.
// Los limites son defensivos; las vistas explican la causa del error sin exponerlos.
public final class VinylInputRules {

    public static final int MIN_YEAR = 1000;
    public static final int MAX_YEAR = 9999;
    public static final int MIN_PRICE = 1;
    public static final int MAX_PRICE = 99_999_999;

    public enum YearValidity {
        VALID,
        FUTURE,
        INVALID
    }

    public enum PriceValidity {
        VALID,
        NOT_POSITIVE,
        INVALID
    }

    private VinylInputRules() {
    }

    public static int currentYear() {
        return Year.now().getValue();
    }

    public static YearValidity classifyYear(final int year) {
        if (year < MIN_YEAR || year > MAX_YEAR) {
            return YearValidity.INVALID;
        }
        return year > currentYear() ? YearValidity.FUTURE : YearValidity.VALID;
    }

    public static PriceValidity classifyPrice(final int price) {
        if (price < MIN_PRICE) {
            return PriceValidity.NOT_POSITIVE;
        }
        return price > MAX_PRICE ? PriceValidity.INVALID : PriceValidity.VALID;
    }

    public static boolean isPriceRangeOrdered(final Integer minPrice, final Integer maxPrice) {
        return minPrice == null || maxPrice == null || minPrice <= maxPrice;
    }

    public static boolean isPressingYearOrdered(final Integer releaseYear, final Integer pressingYear) {
        return releaseYear == null || pressingYear == null || pressingYear >= releaseYear;
    }
}
```
