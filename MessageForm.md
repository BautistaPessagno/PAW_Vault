---
title: "MessageForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/MessageForm.java"]
---

# MessageForm

Un Mensaje nuevo: texto obligatorio hasta 500 caracteres. [[InquiryServiceImpl]] vuelve a aplicar [[MessageRules]].

## Guía de lectura

Datos y dependencias declaradas: `body`.

Operaciones para localizar en la fuente: `getBody`, `setBody`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MessageRules]].

Referenciado por: [[InquiryController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/MessageForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/MessageForm.java>), líneas 1–22.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.MessageRules;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

// Un Mensaje nuevo en la Conversacion. InquiryService vuelve a aplicar MessageRules.
public class MessageForm {

    @NotBlank(message = "{inquiry.message.body.required}")
    @Size(max = MessageRules.MAX_LENGTH, message = "{inquiry.message.body.size}")
    private String body;

    public String getBody() {
        return body;
    }

    public void setBody(final String body) {
        this.body = body;
    }
}
```
