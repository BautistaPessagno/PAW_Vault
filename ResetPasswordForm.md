---
title: "ResetPasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java"]
---

# ResetPasswordForm

Recovery form with a required token, a new password under [[ValidPassword]] and a confirmation checked by [[MatchingPasswords]]. The token arrives from the query string and is re-emitted as an escaped hidden field.

## Connections

Project types referenced: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenced by: [[AuthenticationController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.NotBlank;

@MatchingPasswords
public class ResetPasswordForm implements PasswordsMatching {

    @NotBlank(message = "{auth.resetPassword.token.required}")
    private String token;

    @ValidPassword
    private String password;

    private String passwordConfirmation;

    public String getToken() {
        return token;
    }

    public void setToken(final String token) {
        this.token = token;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }

    public String getPasswordConfirmation() {
        return passwordConfirmation;
    }

    public void setPasswordConfirmation(final String passwordConfirmation) {
        this.passwordConfirmation = passwordConfirmation;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
