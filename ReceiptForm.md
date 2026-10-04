---
title: "ReceiptForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReceiptForm.java"]
---

# ReceiptForm

Formulario del comprobante: un archivo validado con [[ValidReceipt]].

## Guía de lectura

Datos y dependencias declaradas: `receipt`.

Operaciones para localizar en la fuente: `getReceipt`, `setReceipt`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ValidReceipt]].

Referenciado por: [[InquiryController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReceiptForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReceiptForm.java>), líneas 1–18.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.webapp.validation.ValidReceipt;
import org.springframework.web.multipart.MultipartFile;

public class ReceiptForm {

    @ValidReceipt
    private MultipartFile receipt;

    public MultipartFile getReceipt() {
        return receipt;
    }

    public void setReceipt(final MultipartFile receipt) {
        this.receipt = receipt;
    }
}
```
