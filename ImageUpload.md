---
title: "ImageUpload"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ImageUpload.java"]
---

# ImageUpload

Un archivo subido reducido a tipo de contenido y bytes. Existe para que los services no dependan de `MultipartFile`; lo arma [[ImageFiles]].

## Guía de lectura

Datos y dependencias declaradas: `contentType`, `data`.

Operaciones para localizar en la fuente: `getContentType`, `getData`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AvatarForm]], [[ImageFiles]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishForm]], [[UserService]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ImageUpload.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageUpload.java>), líneas 1–22.

```java
package ar.edu.itba.paw.models;

import java.util.Arrays;

public final class ImageUpload {

    private final String contentType;
    private final byte[] data;

    public ImageUpload(final String contentType, final byte[] data) {
        this.contentType = contentType;
        this.data = data == null ? null : Arrays.copyOf(data, data.length);
    }

    public String getContentType() {
        return contentType;
    }

    public byte[] getData() {
        return data == null ? null : Arrays.copyOf(data, data.length);
    }
}
```
