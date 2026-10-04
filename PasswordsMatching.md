---
title: "PasswordsMatching"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java"]
---

# PasswordsMatching

Interfaz con los dos getters que necesita [[MatchingPasswordsValidator]]; la implementan los tres formularios con contraseña.

## Guía de lectura

Operaciones para localizar en la fuente: `getPassword`, `getPasswordConfirmation`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ChangePasswordForm]], [[MatchingPasswordsValidator]], [[RegisterForm]], [[ResetPasswordForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java>), líneas 1–8.

```java
package ar.edu.itba.paw.webapp.validation;

public interface PasswordsMatching {

    String getPassword();

    String getPasswordConfirmation();
}
```
