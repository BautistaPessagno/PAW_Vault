---
title: "Artist"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Artist.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Artist.java>), líneas 1–19.

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
