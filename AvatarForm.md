---
title: "AvatarForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/AvatarForm.java"]
---

# AvatarForm

Formulario de la foto de perfil: un archivo o la marca `remove`. Lo valida [[AvatarFormValidator]].

## Guía de lectura

Datos y dependencias declaradas: `avatar`, `remove`.

Operaciones para localizar en la fuente: `getAvatar`, `setAvatar`, `isRemove`, `setRemove`, `toImageUpload`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ImageFiles]], [[ImageUpload]], [[ValidAvatarForm]].

Referenciado por: [[AvatarFormValidator]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/AvatarForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/AvatarForm.java>), líneas 1–37.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.webapp.validation.ValidAvatarForm;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

// La foto de perfil nueva, o remove para quitar la actual.
@ValidAvatarForm
public class AvatarForm {

    private MultipartFile avatar;

    private boolean remove;

    public MultipartFile getAvatar() {
        return avatar;
    }

    public void setAvatar(final MultipartFile avatar) {
        this.avatar = avatar;
    }

    public boolean isRemove() {
        return remove;
    }

    public void setRemove(final boolean remove) {
        this.remove = remove;
    }

    // null cuando se quita la foto.
    public ImageUpload toImageUpload() throws IOException {
        return remove ? null : ImageFiles.toUpload(avatar);
    }
}
```
