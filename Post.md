---
title: "Post"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Post.java"]
---

# Post

La publicación guardada: publicante, álbum, precio, descripción, [[Condition]], año de prensado, zona, foto principal y [[PostStatus]]. Representa un ejemplar único. Ver [[Publish flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `userId`, `albumId`, `price`, `description`, `condition`, `pressingYear`, `zone`, `imageId`, `status`.

Operaciones para localizar en la fuente: `getId`, `getUserId`, `getAlbumId`, `getPrice`, `getDescription`, `getCondition`, `getPressingYear`, `getZone`, `getImageId`, `getStatus`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[PostStatus]].

Referenciado por: [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Post.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>), líneas 1–69.

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
