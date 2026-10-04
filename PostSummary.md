---
title: "PostSummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSummary.java"]
---

# PostSummary

La publicación unida a su publicante, álbum y artista en una sola fila: lo que muestran las tarjetas y la ficha. Trae también el correo y el idioma del publicante para no volver a buscarlo al mandar un aviso. Evita el N+1 del listado.

## Guía de lectura

Datos y dependencias declaradas: `id`, `userId`, `publisherEmail`, `publisherLocale`, `albumId`, `title`, `artistName`, `releaseYear`, `genre`, `coverImageId`, `price`, `description`, `condition`, `pressingYear`, `zone`, `status`.

Operaciones para localizar en la fuente: `getId`, `getUserId`, `getPublisherEmail`, `getPublisherLocale`, `getAlbumId`, `getTitle`, `getArtistName`, `getReleaseYear`, `getGenre`, `getCoverImageId`, `getPrice`, `getDescription`, `getCondition`, `getPressingYear`, `getZone`, `getStatus`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[Genre]], [[PostStatus]].

Referenciado por: [[CartService]], [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[PostDao]], [[PostDetail]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostPage]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PostSummary.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSummary.java>), líneas 1–109.

```java
package ar.edu.itba.paw.models;

public final class PostSummary {
    private final long id;
    private final long userId;
    private final String publisherEmail;
    // Idioma en el que el publicante quiere recibir los avisos de su publicacion.
    private final String publisherLocale;
    private final long albumId;
    private final String title;
    private final String artistName;
    private final int releaseYear;
    private final Genre genre;
    private final Long coverImageId;
    private final int price;
    private final String description;
    private final Condition condition;
    private final Integer pressingYear;
    private final String zone;
    private final PostStatus status;

    public PostSummary(final long id, final long userId, final String publisherEmail,
                       final String publisherLocale, final long albumId,
                       final String title, final String artistName, final int releaseYear, final Genre genre,
                       final Long coverImageId, final int price, final String description,
                       final Condition condition, final Integer pressingYear, final String zone,
                       final PostStatus status) {
        this.id = id;
        this.userId = userId;
        this.publisherEmail = publisherEmail;
        this.publisherLocale = publisherLocale;
        this.albumId = albumId;
        this.title = title;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
        this.genre = genre;
        this.coverImageId = coverImageId;
        this.price = price;
        this.description = description;
        this.condition = condition;
        this.pressingYear = pressingYear;
        this.zone = zone;
        this.status = status;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getPublisherEmail() {
        return publisherEmail;
    }

    public String getPublisherLocale() {
        return publisherLocale;
    }

    public long getAlbumId() {
        return albumId;
    }

    public String getTitle() {
        return title;
    }

    public String getArtistName() {
        return artistName;
    }

    public int getReleaseYear() {
        return releaseYear;
    }

    public Genre getGenre() {
        return genre;
    }

    public Long getCoverImageId() {
        return coverImageId;
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

    public PostStatus getStatus() {
        return status;
    }
}
```
