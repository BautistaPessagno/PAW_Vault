---
title: "Image"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Image.java"]
---

# Image

Stored image value with long id, String contentType and byte[] data. [[ImageJdbcDao]] reads and writes the bytes; [[ImageController]] serves them. Fields are final, but the constructor and getData expose the original mutable byte array without defensive copies. There is no image validation in this model.

## Connections

Project types referenced: none.

Referenced by: [[AlbumServiceImplTest]], [[ImageController]], [[ImageDao]], [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageService]], [[ImageServiceImpl]], [[ImageServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Image.java, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>)

```java
package ar.edu.itba.paw.models;

public class Image {

    private final long id;
    private final String contentType;
    private final byte[] data;

    public Image(final long id, final String contentType, final byte[] data) {
        this.id = id;
        this.contentType = contentType;
        this.data = data;
    }

    public long getId() {
        return id;
    }

    public String getContentType() {
        return contentType;
    }

    public byte[] getData() {
        return data;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
