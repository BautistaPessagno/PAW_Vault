---
title: "PaymentForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PaymentForm.java"]
---

# PaymentForm

Datos de cobro: CBU y alias, los dos opcionales (vaciarlos borra los datos). Lo valida [[PaymentFormValidator]].

## Guía de lectura

Datos y dependencias declaradas: `cbu`, `alias`.

Operaciones para localizar en la fuente: `getCbu`, `setCbu`, `getAlias`, `setAlias`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ValidPaymentForm]].

Referenciado por: [[PaymentFormValidator]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/PaymentForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PaymentForm.java>), líneas 1–28.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.ValidPaymentForm;

// Los dos campos son opcionales: vaciarlos borra los datos de cobro.
@ValidPaymentForm
public class PaymentForm {

    private String cbu;

    private String alias;

    public String getCbu() {
        return cbu;
    }

    public void setCbu(final String cbu) {
        this.cbu = cbu;
    }

    public String getAlias() {
        return alias;
    }

    public void setAlias(final String alias) {
        this.alias = alias;
    }
}
```
