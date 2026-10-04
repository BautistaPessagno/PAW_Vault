---
title: "Receipt"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Receipt.java"]
---

# Receipt

El comprobante de una venta: tipo de contenido y bytes. `getFilename` le pone la extensión que corresponde al tipo para que se descargue como un archivo reconocible.

## Guía de lectura

Datos y dependencias declaradas: `contentType`, `data`.

Operaciones para localizar en la fuente: `getContentType`, `getData`, `getFilename`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ReceiptRules]].

Referenciado por: [[InquiryController]], [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Receipt.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Receipt.java>), líneas 1–25.

```java
package ar.edu.itba.paw.models;

// El comprobante que sube el comprador para una consulta en AWAITING_PAYMENT.
public final class Receipt {
    private final String contentType;
    private final byte[] data;

    public Receipt(final String contentType, final byte[] data) {
        this.contentType = contentType;
        this.data = data;
    }

    public String getContentType() {
        return contentType;
    }

    public byte[] getData() {
        return data;
    }

    // Con la extension que corresponde al tipo, para que se guarde como archivo reconocible.
    public String getFilename() {
        return "comprobante." + ReceiptRules.extensionOf(contentType);
    }
}
```
