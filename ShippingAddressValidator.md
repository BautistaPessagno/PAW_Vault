---
title: "ShippingAddressValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ShippingAddressValidator.java"]
---

# ShippingAddressValidator

Con dirección guardada elegida no valida nada; al cargar una nueva exige calle, altura, ciudad, código postal y provincia.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`, `reject`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ShippingAddressForm]], [[ValidShippingAddress]].

Referenciado por: [[ValidShippingAddress]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ShippingAddressValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ShippingAddressValidator.java>), líneas 1–48.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.webapp.form.ShippingAddressForm;
import org.springframework.util.StringUtils;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class ShippingAddressValidator implements ConstraintValidator<ValidShippingAddress, ShippingAddressForm> {

    // Con direccion guardada elegida los campos de direccion no se completan: no hay nada
    // que validar. Sin ella, se esta cargando una nueva y sus campos obligatorios rigen.
    @Override
    public boolean isValid(final ShippingAddressForm form, final ConstraintValidatorContext context) {
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
