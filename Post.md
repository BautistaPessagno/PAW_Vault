---
title: "Post"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "domain"]
sources: ["models/src/main/java/ar/edu/itba/paw/models/Post.java"]
---

# Post

A publication is the pair of a user and an album, plus its own generated ID. `userId` connects to [[User]], and `albumId` connects to [[Album]]. It has no price, physical condition, timestamps, status or inventory quantity. [[PostJdbcDao]] enforces pair uniqueness through the SQL constraint. A Post is a domain noun, distinct from the HTTP POST method.

## Connections

Project types referenced: none.

Referenced by: [[EmailServiceImpl]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Stored values

| Field | Java type |
|---|---|
| `id` | `long` |
| `userId` | `long` |
| `albumId` | `long` |

Constructors assign these values directly. Getters return them. There are no setters, persistence annotations, custom equality methods or constructor-level validation.

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Post.java, lines 1–25](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>)

```java
package ar.edu.itba.paw.models;

public class Post {
    private final long id;
    private final long userId;
    private final long albumId;

    public Post(final long id, final long userId, final long albumId) {
        this.id = id;
        this.userId = userId;
        this.albumId = albumId;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public long getAlbumId() {
        return albumId;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
