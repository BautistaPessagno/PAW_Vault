---
title: "RegisterForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java"]
---

# RegisterForm

Registro: correo, nombre, contraseña con [[ValidPassword]] y confirmación con [[MatchingPasswords]].

## Guía de lectura

Datos y dependencias declaradas: `email`, `username`, `password`, `passwordConfirmation`.

Operaciones para localizar en la fuente: `getEmail`, `setEmail`, `getUsername`, `setUsername`, `getPassword`, `setPassword`, `getPasswordConfirmation`, `setPasswordConfirmation`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenciado por: [[AuthenticationController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java>), líneas 1–61.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

@MatchingPasswords
public class RegisterForm implements PasswordsMatching {

    @NotBlank(message = "{auth.register.email.required}")
    @Email(message = "{auth.register.email.invalid}")
    @Size(max = 100, message = "{auth.register.email.size}")
    private String email;

    @NotBlank(message = "{auth.register.username.required}")
    @Size(max = 100, message = "{auth.register.username.size}")
    private String username;

    @ValidPassword
    private String password;

    private String passwordConfirmation;

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }

    @Override
    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }

    @Override
    public String getPasswordConfirmation() {
        return passwordConfirmation;
    }

    public void setPasswordConfirmation(final String passwordConfirmation) {
        this.passwordConfirmation = passwordConfirmation;
    }
}
```
