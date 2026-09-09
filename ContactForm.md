---
title: "ContactForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java"]
---

# ContactForm

Mutable contact binding object. Both fields are NotBlank and at most 100 characters; contactEmail also has Email validation. [[PostContactController]] trims before these constraints run, and [[PostServiceImpl]] normalizes the email before mail assembly. It contains no free-message field or publisher email.

## Connections

Project types referenced: none.

Referenced by: [[PostContactController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java, lines 1–33](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class ContactForm {

    @NotBlank(message = "{post.contact.name.required}")
    @Size(max = 100, message = "{post.contact.name.size}")
    private String contactName;

    @NotBlank(message = "{post.contact.email.required}")
    @Email(message = "{post.contact.email.invalid}")
    @Size(max = 100, message = "{post.contact.email.size}")
    private String contactEmail;

    public String getContactName() {
        return contactName;
    }

    public void setContactName(final String contactName) {
        this.contactName = contactName;
    }

    public String getContactEmail() {
        return contactEmail;
    }

    public void setContactEmail(final String contactEmail) {
        this.contactEmail = contactEmail;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
