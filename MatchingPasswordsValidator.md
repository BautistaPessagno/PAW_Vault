---
title: "MatchingPasswordsValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java"]
---

# MatchingPasswordsValidator

Returns true when the form or password is null, or when password and confirmation are equal. Otherwise it replaces the default class-level violation with one on passwordConfirmation, so ui:text-input shows it under that field.

## Connections

Project types referenced: [[MatchingPasswords]], [[PasswordsMatching]].

Referenced by: [[MatchingPasswords]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java, lines 1–20](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
