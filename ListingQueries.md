---
title: "ListingQueries"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java"]
---

# ListingQueries

Sanea el parámetro `from` (la query del listado de origen): solo acepta caracteres de una query ya codificada. Cualquier otra cosa se descarta.

## Guía de lectura

Datos y dependencias declaradas: `LISTING_QUERY`.

Operaciones para localizar en la fuente: `sanitize`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartController]], [[CartExceptionAdvice]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java>), líneas 1–21.

```java
package ar.edu.itba.paw.webapp.controller;

import java.util.regex.Pattern;

/*
 * La query string del listado de origen que viaja en el parametro "from", tal como la armo
 * LandingController: solo caracteres de una query ya codificada. Cualquier otra cosa se descarta
 * y se vuelve a "/".
 */
public final class ListingQueries {

    private static final Pattern LISTING_QUERY = Pattern.compile("[A-Za-z0-9._~%+=&-]{1,2000}");

    private ListingQueries() {
    }

    // La query si tiene la forma esperada, o vacia.
    public static String sanitize(final String returnQuery) {
        return returnQuery != null && LISTING_QUERY.matcher(returnQuery).matches() ? returnQuery : "";
    }
}
```
