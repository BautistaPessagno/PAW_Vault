---
title: "Artist"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Artist.java"]
---

# Artist

The reusable artist identity. `id` is the generated database key and `name` is the display name as typed, trimmed but with its original casing. Identity lives in the persisted artists.normalized_name column (lowercase letters and digits only), which [[ArtistServiceImpl]] computes and this model does not carry. [[ArtistJdbcDao]] also stores a search_phrase for suggestions. An owner's edit can overwrite the shared display name. Multiple [[Album]] records refer to its ID.

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
