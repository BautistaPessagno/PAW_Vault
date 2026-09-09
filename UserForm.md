---
title: "UserForm"
categories: ["History"]
type: "historical-code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
source_commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
tags: ["codemap", "web"]
sources: []
---

# UserForm

> [!note] Historical source
> This type is absent at ff96f27. The text and excerpt below describe the previous implementation at 041ce34.

Legacy mutable form. Username has Size 8–100 and regex `^[a-z][a-zA-Z0-9]*$`; email has NotBlank and Email but no maximum length. Username lacks NotNull or NotBlank, so null is not rejected by those two constraints alone. Constraints use default validation messages rather than the project-specific publish/contact message keys. See [[Legacy user flow]] for differences from publishing.

## Connections

Project types referenced: none.

Referenced by: [[HelloWorldController]].

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/UserForm.java, lines 1–33](<https://bitbucket.org/itba/paw-2026b-14/src/041ce34404963b689d05443ca00abb7e75aa7f15/webapp/src/main/java/ar/edu/itba/paw/webapp/form/UserForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

public class UserForm {

    @Size(min = 8, max = 100)
    @Pattern(regexp = "^[a-z][a-zA-Z0-9]*$")
    private String username;

    @NotBlank
    @Email
    private String email;

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(final String email) {
        this.email = email;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
