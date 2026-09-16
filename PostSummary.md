---
title: "PostSummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostSummary.java"]
---

# PostSummary

Joined publication projection for cards and contact checks. Includes seller identity and preferred locale, album metadata, nullable legacy price/details, and publication status. coverImageId resolves posts.image_id first, falling back to albums.cover_image_id in [[PostJdbcDao]].

## Connections

Project types referenced: [[Condition]], [[Genre]], [[PostStatus]].

Referenced by: [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImplTest]], [[SearchResult]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostSummary.java, lines 1–110](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSummary.java>)

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
    // Los posts anteriores a estas columnas no tienen precio: por eso es Integer y no int.
    private final Integer price;
    private final String description;
    private final Condition condition;
    private final Integer pressingYear;
    private final String zone;
    private final PostStatus status;

    public PostSummary(final long id, final long userId, final String publisherEmail,
                       final String publisherLocale, final long albumId,
                       final String title, final String artistName, final int releaseYear, final Genre genre,
                       final Long coverImageId, final Integer price, final String description,
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

    public Integer getPrice() {
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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
