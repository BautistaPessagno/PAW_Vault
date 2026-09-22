---
title: "ProfileForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java"]
---

# ProfileForm

Username edit bean: required and at most 100 characters, reusing the registration messages. [[UserServiceImpl]] trims the value before saving it.

## Connections

Project types referenced: none.

Referenced by: [[ProfileController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class ProfileForm {

    @NotBlank(message = "{auth.register.username.required}")
    @Size(max = 100, message = "{auth.register.username.size}")
    private String username;

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
