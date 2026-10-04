---
title: "MatchingPasswords"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java"]
---

# MatchingPasswords

Restricción de clase para formularios con contraseña y confirmación ([[PasswordsMatching]]).

## Guía de lectura

Operaciones para localizar en la fuente: `message`, `groups`, `payload`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MatchingPasswordsValidator]].

Referenciado por: [[ChangePasswordForm]], [[MatchingPasswordsValidator]], [[RegisterForm]], [[ResetPasswordForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java>), líneas 1–24.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.ANNOTATION_TYPE;
import static java.lang.annotation.ElementType.TYPE;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Documented
@Constraint(validatedBy = MatchingPasswordsValidator.class)
@Target({ TYPE, ANNOTATION_TYPE })
@Retention(RUNTIME)
public @interface MatchingPasswords {

    String message() default "{auth.password.mismatch}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
}
```
