---
title: "ForgotPasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java"]
---

# ForgotPasswordForm

Pedido de recuperación: solo el correo, obligatorio, con formato y hasta 100 caracteres.

## Guía de lectura

Datos y dependencias declaradas: `email`.

Operaciones para localizar en la fuente: `getEmail`, `setEmail`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AuthenticationController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java>), líneas 1–22.

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class ForgotPasswordForm {

    @NotBlank(message = "{auth.register.email.required}")
    @Email(message = "{auth.register.email.invalid}")
    @Size(max = 100, message = "{auth.register.email.size}")
    private String email;

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

}
```
