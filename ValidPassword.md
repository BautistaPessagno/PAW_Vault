---
title: "ValidPassword"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java"]
---

# ValidPassword

Restricción compuesta de contraseña: obligatoria, de 12 a 72 caracteres (el tope de BCrypt), con al menos una letra y un número.

## Guía de lectura

Operaciones para localizar en la fuente: `message`, `groups`, `payload`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ChangePasswordForm]], [[RegisterForm]], [[ResetPasswordForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java>), líneas 1–32.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.ANNOTATION_TYPE;
import static java.lang.annotation.ElementType.FIELD;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Documented
@Constraint(validatedBy = { })
@Target({ FIELD, ANNOTATION_TYPE })
@Retention(RUNTIME)
@NotBlank(message = "{auth.password.required}")
// El maximo es el tope de BCrypt, que ignora lo que pase de 72 bytes.
@Size(min = 12, max = 72, message = "{auth.password.size}")
@Pattern(regexp = ".*[A-Za-z].*", message = "{auth.password.letter}")
@Pattern(regexp = ".*[0-9].*", message = "{auth.password.number}")
public @interface ValidPassword {

    String message() default "{auth.password.invalid}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
}
```
