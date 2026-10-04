---
title: "ChangePasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java"]
---

# ChangePasswordForm

Cambio de contraseña desde el perfil: clave actual obligatoria, nueva con [[ValidPassword]] y confirmación con [[MatchingPasswords]].

## Guía de lectura

Datos y dependencias declaradas: `currentPassword`, `password`, `passwordConfirmation`.

Operaciones para localizar en la fuente: `getCurrentPassword`, `setCurrentPassword`, `getPassword`, `setPassword`, `getPasswordConfirmation`, `setPasswordConfirmation`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenciado por: [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java>), líneas 1–43.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.NotBlank;

@MatchingPasswords
public class ChangePasswordForm implements PasswordsMatching {

    @NotBlank(message = "{profile.password.current.required}")
    private String currentPassword;

    @ValidPassword
    private String password;

    private String passwordConfirmation;

    public String getCurrentPassword() {
        return currentPassword;
    }

    public void setCurrentPassword(final String currentPassword) {
        this.currentPassword = currentPassword;
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
