---
title: "ContactForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java"]
---

# ContactForm

Only an optional contactMessage with a 500-character maximum. Buyer name/email are no longer editable form fields; the controller gets them from the authenticated principal.

## Connections

Project types referenced: none.

Referenced by: [[PostContactController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java>)

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Size;

public class ContactForm {

    // Opcional: sirve para preguntar algo o negociar el precio. Viaja en el mail al publicante.
    @Size(max = 500, message = "{post.contact.message.size}")
    private String contactMessage;

    public String getContactMessage() {
        return contactMessage;
    }

    public void setContactMessage(final String contactMessage) {
        this.contactMessage = contactMessage;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
