---
title: "Image"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Image.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>), líneas 1–28.

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
