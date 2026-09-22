---
title: "ValidPassword"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java"]
---

# ValidPassword

Composed field constraint: NotBlank, Size 12–72 (BCrypt's 72-byte limit expressed as characters) and two patterns requiring an ASCII letter and a digit, each with its own message. It declares no validator of its own; the composed constraints report individually.

## Connections

Project types referenced: none.

Referenced by: [[ChangePasswordForm]], [[ResetPasswordForm]], [[VerifyEmailForm]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
