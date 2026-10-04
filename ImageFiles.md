---
title: "ImageFiles"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java"]
---

# ImageFiles

Puente entre `MultipartFile` y [[ImageUpload]]: detecta archivo presente, valida con [[ImageRules]] mirando el tamaño antes de leer los bytes y convierte.

## Guía de lectura

Operaciones para localizar en la fuente: `isPresent`, `isValid`, `toUpload`, `toUploads`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ImageRules]], [[ImageUpload]].

Referenciado por: [[AvatarForm]], [[AvatarFormValidator]], [[PublishForm]], [[PublishFormValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java>), líneas 1–50.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.models.ImageUpload;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

// Pasa los archivos subidos a ImageUpload: los services no conocen MultipartFile. La validacion
// usa las mismas ImageRules que ImageService al guardarlas.
public final class ImageFiles {

    private ImageFiles() {
    }

    // Un input file sin elegir llega como archivo vacio, no como null.
    public static boolean isPresent(final MultipartFile file) {
        return file != null && !file.isEmpty();
    }

    // El tamanio se mira antes de leer los bytes: no hace falta cargar un archivo que ya sobra.
    public static boolean isValid(final MultipartFile file) {
        if (!isPresent(file) || file.getSize() > ImageRules.MAX_IMAGE_BYTES) {
            return false;
        }
        try {
            return ImageRules.isValid(ImageRules.normalizeContentType(file.getContentType()), file.getBytes());
        } catch (final IOException e) {
            return false;
        }
    }

    public static ImageUpload toUpload(final MultipartFile file) throws IOException {
        return new ImageUpload(file.getContentType(), file.getBytes());
    }

    public static List<ImageUpload> toUploads(final MultipartFile[] files) throws IOException {
        final List<ImageUpload> uploads = new ArrayList<>();
        if (files != null) {
            for (final MultipartFile file : files) {
                if (isPresent(file)) {
                    uploads.add(toUpload(file));
                }
            }
        }
        return uploads;
    }
}
```
