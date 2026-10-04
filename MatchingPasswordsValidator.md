---
title: "MatchingPasswordsValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java"]
---

# MatchingPasswordsValidator

Compara contraseña y confirmación y cuelga el error del campo de confirmación.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MatchingPasswords]], [[PasswordsMatching]].

Referenciado por: [[MatchingPasswords]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java>), líneas 1–20.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class MatchingPasswordsValidator implements ConstraintValidator<MatchingPasswords, PasswordsMatching> {

    @Override
    public boolean isValid(final PasswordsMatching form, final ConstraintValidatorContext context) {
        if (form == null || form.getPassword() == null
                || form.getPassword().equals(form.getPasswordConfirmation())) {
            return true;
        }
        context.disableDefaultConstraintViolation();
        context.buildConstraintViolationWithTemplate(context.getDefaultConstraintMessageTemplate())
                .addPropertyNode("passwordConfirmation")
                .addConstraintViolation();
        return false;
    }
}
```
