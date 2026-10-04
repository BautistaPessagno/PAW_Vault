---
title: "ValidContactForm"
categories: ["History"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "41c32af61ff7926fd4e3b07446c84837851a063f"
status: "historical"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidContactForm.java"]
---

# ValidContactForm

> Histórico. Este archivo ya no existe con ese nombre en `8929aea`. El código inferior conserva su revisión en `41c32af`. Fue renombrada a [[ValidShippingAddress]] cuando el carrito empezó a compartir el formulario de dirección.

## Fuente completa

Fuente exacta en `41c32af`: `webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidContactForm.java`, líneas 1–23.

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
@Constraint(validatedBy = ContactFormValidator.class)
@Target(TYPE)
@Retention(RUNTIME)
public @interface ValidContactForm {

    String message() default "{validation.form.invalid}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
}
```
