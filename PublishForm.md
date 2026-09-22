---
title: "PublishForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java"]
---

# PublishForm

Required title/artist up to 255 characters, release year 1000–9999, genre, price 1–99,999,999 and condition. Optional zone up to 100, pressing year 1000–9999, description up to 1000 and MultipartFile cover. The same bean backs publishing and editing; no publisher identity or stock field remains.

## Connections

Project types referenced: [[Condition]], [[Genre]].

Referenced by: [[PublishController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java, lines 1–130](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

public class PublishForm {

    @NotBlank(message = "{publish.title.required}")
    @Size(max = 255, message = "{publish.title.size}")
    private String title;

    @NotBlank(message = "{publish.artistName.required}")
    @Size(max = 255, message = "{publish.artistName.size}")
    private String artistName;

    @NotNull(message = "{publish.releaseYear.required}")
    @Min(value = 1000, message = "{publish.releaseYear.range}")
    @Max(value = 9999, message = "{publish.releaseYear.range}")
    private Integer releaseYear;

    @NotNull(message = "{publish.genre.required}")
    private Genre genre;

    @NotNull(message = "{publish.price.required}")
    @Min(value = 1, message = "{publish.price.range}")
    @Max(value = 99999999, message = "{publish.price.range}")
    private Integer price;

    @NotNull(message = "{publish.condition.required}")
    private Condition condition;

    @Size(max = 100, message = "{publish.zone.size}")
    private String zone;

    @Min(value = 1000, message = "{publish.pressingYear.range}")
    @Max(value = 9999, message = "{publish.pressingYear.range}")
    private Integer pressingYear;

    @Size(max = 1000, message = "{publish.description.size}")
    private String description;

    private MultipartFile cover;

    public String getTitle() {
        return title;
    }

    public void setTitle(final String title) {
        this.title = title;
    }

    public String getArtistName() {
        return artistName;
    }

    public void setArtistName(final String artistName) {
        this.artistName = artistName;
    }

    public Integer getReleaseYear() {
        return releaseYear;
    }

    public void setReleaseYear(final Integer releaseYear) {
        this.releaseYear = releaseYear;
    }

    public Genre getGenre() {
        return genre;
    }

    public void setGenre(final Genre genre) {
        this.genre = genre;
    }

    public Integer getPrice() {
        return price;
    }

    public void setPrice(final Integer price) {
        this.price = price;
    }

    public Condition getCondition() {
        return condition;
    }

    public void setCondition(final Condition condition) {
        this.condition = condition;
    }

    public String getZone() {
        return zone;
    }

    public void setZone(final String zone) {
        this.zone = zone;
    }

    public Integer getPressingYear() {
        return pressingYear;
    }

    public void setPressingYear(final Integer pressingYear) {
        this.pressingYear = pressingYear;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(final String description) {
        this.description = description;
    }

    public MultipartFile getCover() {
        return cover;
    }

    public void setCover(final MultipartFile cover) {
        this.cover = cover;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
