---
title: "PasswordsMatching"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java>), líneas 1–8.

```java
package ar.edu.itba.paw.webapp.validation;

public interface PasswordsMatching {

    String getPassword();

    String getPasswordConfirmation();
}
```
