---
title: "MatchingPasswords"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java"]
---

# MatchingPasswords

Class-level Bean Validation constraint for forms implementing [[PasswordsMatching]]. Its default message is auth.password.mismatch, and [[MatchingPasswordsValidator]] attaches the violation to the passwordConfirmation field.

## Connections

Project types referenced: [[MatchingPasswordsValidator]].

Referenced by: [[ChangePasswordForm]], [[MatchingPasswordsValidator]], [[ResetPasswordForm]], [[VerifyEmailForm]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
