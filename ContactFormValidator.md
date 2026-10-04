---
title: "ContactFormValidator"
categories: ["History"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "41c32af61ff7926fd4e3b07446c84837851a063f"
status: "historical"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ContactFormValidator.java"]
---

# ContactFormValidator

> Histórico. Este archivo ya no existe con ese nombre en `8929aea`. El código inferior conserva su revisión en `41c32af`. Fue renombrado a [[ShippingAddressValidator]] cuando el carrito empezó a compartir el formulario de dirección.

## Fuente completa

Fuente exacta en `41c32af`: `webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ContactFormValidator.java`, líneas 1–48.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.webapp.form.ContactForm;
import org.springframework.util.StringUtils;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class ContactFormValidator implements ConstraintValidator<ValidContactForm, ContactForm> {

    // Con direccion guardada elegida los campos de direccion no se completan: no hay nada
    // que validar. Sin ella, se esta cargando una nueva y sus campos obligatorios rigen.
    @Override
    public boolean isValid(final ContactForm form, final ConstraintValidatorContext context) {
        if (form == null || !form.isNewAddress()) {
            return true;
        }

        boolean valid = true;
        context.disableDefaultConstraintViolation();
        if (!StringUtils.hasText(form.getStreet())) {
            reject(context, "street");
            valid = false;
        }
        if (!StringUtils.hasText(form.getStreetNumber())) {
            reject(context, "streetNumber");
            valid = false;
        }
        if (!StringUtils.hasText(form.getCity())) {
            reject(context, "city");
            valid = false;
        }
        if (!StringUtils.hasText(form.getPostalCode())) {
            reject(context, "postalCode");
            valid = false;
        }
        if (form.getProvince() == null) {
            reject(context, "province");
            valid = false;
        }
        return valid;
    }

    private static void reject(final ConstraintValidatorContext context, final String field) {
        context.buildConstraintViolationWithTemplate("{address.required}")
                .addPropertyNode(field).addConstraintViolation();
    }
}
```
