---
title: "ProfileForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java>), líneas 1–19.

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
