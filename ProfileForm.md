---
title: "ProfileForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java"]
---

# ProfileForm

Edición del nombre visible: obligatorio y hasta 100 caracteres.

## Guía de lectura

Datos y dependencias declaradas: `username`.

Operaciones para localizar en la fuente: `getUsername`, `setUsername`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java>), líneas 1–19.

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class ProfileForm {

    @NotBlank(message = "{auth.register.username.required}")
    @Size(max = 100, message = "{auth.register.username.size}")
    private String username;

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }
}
```
