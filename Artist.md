---
title: "Artist"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Artist.java"]
---

# Artist

The reusable artist identity. `id` is the generated database key; `name` is the normalized catalog name. [[ArtistServiceImpl]] trims and lowercases it before [[ArtistJdbcDao]] searches or inserts. The object itself performs no validation or normalization. Multiple [[Album]] records refer to its ID.

## Connections

Project types referenced: none.

Referenced by: [[ArtistDao]], [[ArtistJdbcDao]], [[ArtistJdbcDaoTest]], [[ArtistService]], [[ArtistServiceImpl]], [[ArtistServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

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

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
