---
title: "Image"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Image.java"]
---

# Image

Una imagen guardada: id, tipo de contenido y bytes. La usan fotos de publicaciones, portadas heredadas y avatares. Ver [[Cover image flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `contentType`, `data`.

Operaciones para localizar en la fuente: `getId`, `getContentType`, `getData`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ImageController]], [[ImageDao]], [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageService]], [[ImageServiceImpl]], [[ImageServiceImplTest]], [[InMemoryImageService]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Image.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>), líneas 1–28.

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
