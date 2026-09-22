---
title: "LoginForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java"]
---

# LoginForm

Mutable email/password bean for rendering the login JSP. Authentication of POST /login belongs to Spring Security, rather than MVC @Valid handling.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticationController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java, lines 1–22](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

public class LoginForm {
    private String email;
    private String password;

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
