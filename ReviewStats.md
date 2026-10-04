---
title: "ReviewStats"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java"]
---

# ReviewStats

Cantidad y promedio de las reseñas activas de una Cuenta. El promedio llega sin redondear: lo formatea la vista.

## Guía de lectura

Datos y dependencias declaradas: `count`, `average`.

Operaciones para localizar en la fuente: `getCount`, `getAverage`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PublicProfile]], [[ReviewDao]], [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewService]], [[ReviewServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java>), líneas 1–15.

```java
package ar.edu.itba.paw.models;

public final class ReviewStats {
    private final int count;
    private final double average;

    // El promedio llega sin redondear: lo formatea la vista.
    public ReviewStats(final int count, final double average) {
        this.count = count;
        this.average = average;
    }

    public int getCount() { return count; }
    public double getAverage() { return average; }
}
```
