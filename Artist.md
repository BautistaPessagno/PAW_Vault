---
title: "Artist"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/Artist.java"]
---

# Artist

The reusable artist identity. `id` is the generated database key; `name` is the normalized catalog name. [[ArtistServiceImpl]] trims and lowercases it before [[ArtistJdbcDao]] searches or inserts. The object itself performs no validation or normalization. Multiple [[Album]] records refer to its ID.

## Connections

Project types referenced: none.

Referenced by: [[ArtistDao]], [[ArtistJdbcDao]], [[ArtistService]], [[ArtistServiceImpl]], [[PostServiceImpl]].

Tests: [[ArtistJdbcDaoTest]], [[ArtistServiceImplTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `name` | `String` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Artist.java, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Artist.java>)

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

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
