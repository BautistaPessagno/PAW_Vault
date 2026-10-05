---
title: "LoginForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java"]
---

# LoginForm

Bean con correo y contraseña para dibujar el formulario de login. La autenticación la hace Spring Security, no un controller.

## Guía de lectura

Datos y dependencias declaradas: `email`, `password`.

Operaciones para localizar en la fuente: `getEmail`, `setEmail`, `getPassword`, `setPassword`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AuthenticationController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java>), líneas 1–22.

```java
package ar.edu.itba.paw.webapp.form;

public class LoginForm {
    private String email;
    private String password;

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }
}
```
