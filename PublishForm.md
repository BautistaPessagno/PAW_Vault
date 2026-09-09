---
title: "PublishForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java"]
---

# PublishForm

Mutable Spring form containing username and publisherEmail with 100-character limits, title and artistName with 255-character limits, required Integer releaseYear in 1000–9999, and optional MultipartFile cover. Text/email/year annotations remain unchanged. cover has no Bean Validation annotation; multipart transport limits and [[ImageServiceImpl]] validate that input later. See [[Validation and errors]].

## Connections

Project types referenced: none.

Referenced by: [[PublishController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java, lines 1–85](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import org.springframework.web.multipart.MultipartFile;

import javax.validation.constraints.Email;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

public class PublishForm {

    @NotBlank(message = "{publish.username.required}")
    @Size(max = 100, message = "{publish.username.size}")
    private String username;

    @NotBlank(message = "{publish.publisherEmail.required}")
    @Email(message = "{publish.publisherEmail.invalid}")
    @Size(max = 100, message = "{publish.publisherEmail.size}")
    private String publisherEmail;

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

    private MultipartFile cover;

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }

    public String getPublisherEmail() {
        return publisherEmail;
    }

    public void setPublisherEmail(final String publisherEmail) {
        this.publisherEmail = publisherEmail;
    }

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
