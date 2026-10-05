---
title: "PaymentFormValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PaymentFormValidator.java"]
---

# PaymentFormValidator

Vacío es válido. Si hay CBU o alias, normaliza y valida con [[PaymentInfoRules]], igual que el service.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PaymentForm]], [[PaymentInfoRules]], [[ValidPaymentForm]].

Referenciado por: [[ValidPaymentForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PaymentFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PaymentFormValidator.java>), líneas 1–34.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.models.PaymentInfoRules;
import ar.edu.itba.paw.webapp.form.PaymentForm;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class PaymentFormValidator implements ConstraintValidator<ValidPaymentForm, PaymentForm> {

    // Vacio es valido: el perfil permite no tener datos de cobro. Normaliza igual que UserService.
    @Override
    public boolean isValid(final PaymentForm form, final ConstraintValidatorContext context) {
        if (form == null) {
            return true;
        }

        boolean valid = true;
        context.disableDefaultConstraintViolation();
        final String cbu = PaymentInfoRules.normalizeCbu(form.getCbu());
        if (cbu != null && !PaymentInfoRules.isValidCbu(cbu)) {
            context.buildConstraintViolationWithTemplate("{payment.cbu.invalid}")
                    .addPropertyNode("cbu").addConstraintViolation();
            valid = false;
        }
        final String alias = PaymentInfoRules.normalizeAlias(form.getAlias());
        if (alias != null && !PaymentInfoRules.isValidAlias(alias)) {
            context.buildConstraintViolationWithTemplate("{payment.alias.invalid}")
                    .addPropertyNode("alias").addConstraintViolation();
            valid = false;
        }
        return valid;
    }
}
```
