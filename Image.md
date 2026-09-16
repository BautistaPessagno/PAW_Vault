---
title: "Image"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Image.java"]
---

# Image

Stored MIME label and binary content. The constructor and getData both copy the byte array, so callers cannot mutate the stored model through their array references. [[ImageServiceImpl]] validates MIME labels and size before persistence.

## Connections

Project types referenced: none.

Referenced by: [[ImageController]], [[ImageDao]], [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageService]], [[ImageServiceImpl]], [[ImageServiceImplTest]], [[PostServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Image.java, lines 1–28](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>)

```java
package ar.edu.itba.paw.models;

import java.util.Arrays;

public class Image {

    private final long id;
    private final String contentType;
    private final byte[] data;

    public Image(final long id, final String contentType, final byte[] data) {
        this.id = id;
        this.contentType = contentType;
        this.data = Arrays.copyOf(data, data.length);
    }

    public long getId() {
        return id;
    }

    public String getContentType() {
        return contentType;
    }

    public byte[] getData() {
        return Arrays.copyOf(data, data.length);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
