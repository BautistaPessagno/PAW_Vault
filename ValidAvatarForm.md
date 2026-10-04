---
title: "ValidAvatarForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidAvatarForm.java"]
---

# ValidAvatarForm

Anotación de clase que aplica [[AvatarFormValidator]].

## Guía de lectura

Operaciones para localizar en la fuente: `message`, `groups`, `payload`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AvatarFormValidator]].

Referenciado por: [[AvatarForm]], [[AvatarFormValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidAvatarForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidAvatarForm.java>), líneas 1–23.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.TYPE;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Documented
@Constraint(validatedBy = AvatarFormValidator.class)
@Target(TYPE)
@Retention(RUNTIME)
public @interface ValidAvatarForm {

    String message() default "{profile.avatar.invalid}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
}
```
