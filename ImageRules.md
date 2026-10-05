---
title: "ImageRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ImageRules.java"]
---

# ImageRules

Qué imagen se acepta: PNG, JPEG o WEBP cuya firma de bytes coincide con el tipo declarado, hasta 5 MiB, hasta 5 fotos por publicación, y 26 MiB por request. La usan los validadores de formulario, las vistas y [[ImageServiceImpl]]. Ver [[Cover image flow]].

## Guía de lectura

Datos y dependencias declaradas: `MAX_IMAGE_BYTES`, `MAX_GALLERY_IMAGES`, `MAX_MULTIPART_BYTES`, `contentType`, `ACCEPTED_CONTENT_TYPES`.

Operaciones para localizar en la fuente: `matches`, `normalizeContentType`, `isValid`, `startsWith`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ImageFiles]], [[ImageServiceImpl]], [[InMemoryImageService]], [[PostServiceImpl]], [[ProfileController]], [[PublishController]], [[PublishFormValidator]], [[WebConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>), líneas 1–77.

```java
package ar.edu.itba.paw.models;

import java.util.Arrays;
import java.util.Locale;
import java.util.stream.Collectors;

// Que imagen se acepta como foto de publicacion o de perfil, compartido por los validadores de
// los formularios, por la vista (accept y tope del aviso temprano) y por ImageService.
public final class ImageRules {

    public static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;
    public static final int MAX_GALLERY_IMAGES = 5;
    public static final long MAX_MULTIPART_BYTES = (long) MAX_IMAGE_BYTES * MAX_GALLERY_IMAGES + 1024 * 1024;

    // El tipo declarado tiene que coincidir con la firma del contenido: no alcanza la extension.
    private enum Format {
        PNG("image/png") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, (byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A);
            }
        },
        JPEG("image/jpeg") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, (byte) 0xFF, (byte) 0xD8, (byte) 0xFF);
            }
        },
        WEBP("image/webp") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, 'R', 'I', 'F', 'F') && startsWith(data, 8, 'W', 'E', 'B', 'P');
            }
        };

        private final String contentType;

        Format(final String contentType) {
            this.contentType = contentType;
        }

        abstract boolean matches(byte[] data);
    }

    // Lista para el atributo accept de los input file.
    public static final String ACCEPTED_CONTENT_TYPES = Arrays.stream(Format.values())
            .map(format -> format.contentType).collect(Collectors.joining(","));

    private ImageRules() {
    }

    // Unico lugar que normaliza: lo que se guarda es igual a lo que se valido.
    public static String normalizeContentType(final String contentType) {
        return contentType == null ? null : contentType.trim().toLowerCase(Locale.ROOT);
    }

    // Espera el tipo ya normalizado.
    public static boolean isValid(final String contentType, final byte[] data) {
        if (contentType == null || data == null || data.length == 0 || data.length > MAX_IMAGE_BYTES) {
            return false;
        }
        return Arrays.stream(Format.values())
                .anyMatch(format -> format.contentType.equals(contentType) && format.matches(data));
    }

    private static boolean startsWith(final byte[] data, final int offset, final int... signature) {
        if (data.length < offset + signature.length) {
            return false;
        }
        for (int index = 0; index < signature.length; index++) {
            if (data[offset + index] != (byte) signature[index]) {
                return false;
            }
        }
        return true;
    }
}
```
