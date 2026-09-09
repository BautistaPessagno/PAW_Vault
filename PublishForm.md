---
title: "PublishForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java"]
---

# PublishForm

Mutable binding object with setters, separate from immutable domain objects. Username and publisherEmail are required with a 100-character limit; email also has Email validation. Title and artistName are required with 255-character limits. Integer releaseYear is required and between 1000 and 9999. Integer allows missing values to become null before validation. Conversion errors use `typeMismatch.publishForm.releaseYear`. Unlike [[ContactForm]], the publish controller does not trim before validation. See [[Validation and errors]].

## Connections

Project types referenced: none.

Referenced by: [[PublishController]].

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java, lines 1–73](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

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
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
