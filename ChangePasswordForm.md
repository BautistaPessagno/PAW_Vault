---
title: "ChangePasswordForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java"]
---

# ChangePasswordForm

Profile password form: a required currentPassword, a new password under [[ValidPassword]] and a confirmation checked by [[MatchingPasswords]] through [[PasswordsMatching]]. The current password is verified by the service, not by annotations.

## Connections

Project types referenced: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenced by: [[ProfileController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java, lines 1–43](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.NotBlank;

@MatchingPasswords
public class ChangePasswordForm implements PasswordsMatching {

    @NotBlank(message = "{profile.password.current.required}")
    private String currentPassword;

    @ValidPassword
    private String password;

    private String passwordConfirmation;

    public String getCurrentPassword() {
        return currentPassword;
    }

    public void setCurrentPassword(final String currentPassword) {
        this.currentPassword = currentPassword;
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
