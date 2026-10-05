---
title: "PublishForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java"]
---

# PublishForm

Formulario de publicar y editar: título, artista, año, género, precio, condición, zona, prensado, descripción, fotos nuevas y fotos a retirar. Reglas cruzadas en [[PublishFormValidator]].

## Guía de lectura

Datos y dependencias declaradas: `title`, `artistName`, `releaseYear`, `genre`, `price`, `condition`, `zone`, `pressingYear`, `description`, `covers`, `removedImageIds`.

Operaciones para localizar en la fuente: `getTitle`, `setTitle`, `getArtistName`, `setArtistName`, `getReleaseYear`, `setReleaseYear`, `getGenre`, `setGenre`, `getPrice`, `setPrice`, `getCondition`, `setCondition`, `getZone`, `setZone`, `getPressingYear`, `setPressingYear`, `getDescription`, `setDescription`, `getCovers`, `setCovers`, `toImageUploads`, `getRemovedImageIds`, `setRemovedImageIds`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[Genre]], [[ImageFiles]], [[ImageUpload]], [[ValidPublishForm]].

Referenciado por: [[PublishController]], [[PublishFormValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>), líneas 1–143.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.webapp.validation.ValidPublishForm;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@ValidPublishForm
public class PublishForm {

    @NotBlank(message = "{publish.title.required}")
    @Size(max = 255, message = "{publish.title.size}")
    private String title;

    @NotBlank(message = "{publish.artistName.required}")
    @Size(max = 255, message = "{publish.artistName.size}")
    private String artistName;

    @NotNull(message = "{publish.releaseYear.required}")
    private Integer releaseYear;

    @NotNull(message = "{publish.genre.required}")
    private Genre genre;

    @NotNull(message = "{publish.price.required}")
    private Integer price;

    @NotNull(message = "{publish.condition.required}")
    private Condition condition;

    @Size(max = 100, message = "{publish.zone.size}")
    private String zone;

    private Integer pressingYear;

    @Size(max = 1000, message = "{publish.description.size}")
    private String description;

    private MultipartFile[] covers;

    private List<Long> removedImageIds = new ArrayList<>();

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

    public MultipartFile[] getCovers() {
        return covers;
    }

    public void setCovers(final MultipartFile[] covers) {
        this.covers = covers;
    }

    // Las fotos elegidas, en el orden del input: la primera es la principal.
    public List<ImageUpload> toImageUploads() throws IOException {
        return ImageFiles.toUploads(covers);
    }

    public List<Long> getRemovedImageIds() {
        return removedImageIds;
    }

    public void setRemovedImageIds(final List<Long> removedImageIds) {
        this.removedImageIds = removedImageIds;
    }
}
```
