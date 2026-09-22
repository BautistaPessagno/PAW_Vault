---
title: "PasswordsMatching"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java"]
---

# PasswordsMatching

Interface with the password and confirmation getters, implemented by [[VerifyEmailForm]], [[ResetPasswordForm]] and [[ChangePasswordForm]] so one validator serves all three.

## Connections

Project types referenced: none.

Referenced by: [[ChangePasswordForm]], [[MatchingPasswordsValidator]], [[ResetPasswordForm]], [[VerifyEmailForm]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java, lines 1–8](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java>)

```java
package ar.edu.itba.paw.webapp.validation;

public interface PasswordsMatching {

    String getPassword();

    String getPasswordConfirmation();
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
