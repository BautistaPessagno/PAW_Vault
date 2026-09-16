---
title: "Post"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Post.java"]
---

# Post

One physical exemplar offered by an authenticated publisher. Holds album/user IDs, required integer price on new inserts, optional description, condition, pressing year, zone and image ID, plus AVAILABLE or SOLD status. Historical stock stays in SQL and new inserts set it to one; this model has no stock field.

## Connections

Project types referenced: [[Condition]], [[PostStatus]].

Referenced by: [[EmailServiceImpl]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Post.java, lines 1–69](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>)

```java
package ar.edu.itba.paw.models;

public final class Post {
    private final long id;
    private final long userId;
    private final long albumId;
    private final int price;
    private final String description;
    private final Condition condition;
    private final Integer pressingYear;
    private final String zone;
    private final Long imageId;
    private final PostStatus status;

    public Post(final long id, final long userId, final long albumId, final int price, final String description,
                final Condition condition, final Integer pressingYear, final String zone, final Long imageId,
                final PostStatus status) {
        this.id = id;
        this.userId = userId;
        this.albumId = albumId;
        this.price = price;
        this.description = description;
        this.condition = condition;
        this.pressingYear = pressingYear;
        this.zone = zone;
        this.imageId = imageId;
        this.status = status;
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

    public int getPrice() {
        return price;
    }

    public String getDescription() {
        return description;
    }

    public Condition getCondition() {
        return condition;
    }

    public Integer getPressingYear() {
        return pressingYear;
    }

    public String getZone() {
        return zone;
    }

    public Long getImageId() {
        return imageId;
    }

    public PostStatus getStatus() {
        return status;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
