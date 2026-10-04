---
title: "ContactForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java"]
---

# ContactForm

Formulario de contacto: hereda la dirección de [[ShippingAddressForm]] y suma el mensaje opcional de hasta 500 caracteres.

## Guía de lectura

Datos y dependencias declaradas: `contactMessage`.

Operaciones para localizar en la fuente: `getContactMessage`, `setContactMessage`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ShippingAddressForm]].

Referenciado por: [[PostContactController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java>), líneas 1–19.

```java
package ar.edu.itba.paw.webapp.form;

import javax.validation.constraints.Size;

// La direccion y su validacion vienen de ShippingAddressForm; el contacto suma el mensaje.
public class ContactForm extends ShippingAddressForm {

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
