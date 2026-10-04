---
title: "ForgotPasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
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

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java>), líneas 1–22.

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
