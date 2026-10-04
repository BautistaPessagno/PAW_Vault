---
title: "ResetPasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java"]
---

# ResetPasswordForm

Recuperación: token oculto obligatorio, contraseña nueva con [[ValidPassword]] y confirmación.

## Guía de lectura

Datos y dependencias declaradas: `token`, `password`, `passwordConfirmation`.

Operaciones para localizar en la fuente: `getToken`, `setToken`, `getPassword`, `setPassword`, `getPasswordConfirmation`, `setPasswordConfirmation`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenciado por: [[AuthenticationController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java>), líneas 1–43.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.NotBlank;

@MatchingPasswords
public class ResetPasswordForm implements PasswordsMatching {

    @NotBlank(message = "{auth.resetPassword.token.required}")
    private String token;

    @ValidPassword
    private String password;

    private String passwordConfirmation;

    public String getToken() {
        return token;
    }

    public void setToken(final String token) {
        this.token = token;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }

    public String getPasswordConfirmation() {
        return passwordConfirmation;
    }

    public void setPasswordConfirmation(final String passwordConfirmation) {
        this.passwordConfirmation = passwordConfirmation;
    }
}
```
