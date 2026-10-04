---
title: "Artist"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Artist.java"]
---

# Artist

Artista del catálogo compartido: id y nombre visible. La identidad (nombre normalizado) y la frase de búsqueda viven en la tabla, no en el modelo. Ver [[Publish flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `name`.

Operaciones para localizar en la fuente: `getId`, `getName`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ArtistDao]], [[ArtistJdbcDao]], [[ArtistJdbcDaoTest]], [[ArtistService]], [[ArtistServiceImpl]], [[ArtistServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Artist.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Artist.java>), líneas 1–19.

```java
package ar.edu.itba.paw.models;

public class Artist {
    private final long id;
    private final String name;

    public Artist(final long id, final String name) {
        this.id = id;
        this.name = name;
    }

    public long getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
```
