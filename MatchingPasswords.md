---
title: "MatchingPasswords"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
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

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java>), líneas 1–24.

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
