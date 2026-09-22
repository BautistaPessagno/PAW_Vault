---
title: "VerifyEmailForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java"]
---

# VerifyEmailForm

Requires token and a username up to 100 characters. The password uses the shared [[ValidPassword]] constraint (12–72 characters with an ASCII letter and a digit), and [[MatchingPasswords]] reports a mismatch on passwordConfirmation. @Size counts characters, not UTF-8 bytes, and passwords are not trimmed.

## Connections

Project types referenced: [[MatchingPasswords]], [[PasswordsMatching]], [[ValidPassword]].

Referenced by: [[AuthenticationController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java, lines 1–56](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.MatchingPasswords;
import ar.edu.itba.paw.webapp.validation.PasswordsMatching;
import ar.edu.itba.paw.webapp.validation.ValidPassword;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

@MatchingPasswords
public class VerifyEmailForm implements PasswordsMatching {

    @NotBlank(message = "{auth.verify.token.required}")
    private String token;

    @NotBlank(message = "{auth.register.username.required}")
    @Size(max = 100, message = "{auth.register.username.size}")
    private String username;

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

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
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
