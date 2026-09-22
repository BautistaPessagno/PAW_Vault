---
title: "RegisterForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java"]
---

# RegisterForm

Email-only registration bean with required, email-format and 100-character maximum validation. Username/password are chosen later through VerifyEmailForm.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticationController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java, lines 1–22](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class RegisterForm {

    @NotBlank(message = "{auth.register.email.required}")
    @Email(message = "{auth.register.email.invalid}")
    @Size(max = 100, message = "{auth.register.email.size}")
    private String email;

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
