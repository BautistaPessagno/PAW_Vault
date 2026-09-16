---
title: "VerifyEmailForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java"]
---

# VerifyEmailForm

Requires token, username up to 100 characters and a confirmed password of 12–72 characters with an ASCII letter and a digit. @Size counts characters; it is not a UTF-8 byte-length check. Password values are not trimmed by the controller.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticationController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java, lines 1–62](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.AssertTrue;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

public class VerifyEmailForm {

    @NotBlank(message = "{auth.verify.token.required}")
    private String token;

    @NotBlank(message = "{auth.register.username.required}")
    @Size(max = 100, message = "{auth.register.username.size}")
    private String username;

    @NotBlank(message = "{auth.register.password.required}")
    // El maximo es el tope de BCrypt, que ignora lo que pase de 72 bytes.
    @Size(min = 12, max = 72, message = "{auth.register.password.size}")
    @Pattern(regexp = ".*[A-Za-z].*", message = "{auth.register.password.letter}")
    @Pattern(regexp = ".*[0-9].*", message = "{auth.register.password.number}")
    private String password;

    private String passwordConfirmation;

    @AssertTrue(message = "{auth.register.password.mismatch}")
    public boolean isPasswordConfirmed() {
        return password != null && password.equals(passwordConfirmation);
    }

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
