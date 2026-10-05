---
title: "Receipt"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Receipt.java"]
---

# Receipt

El comprobante de una venta: tipo de contenido y bytes. Copia el arreglo al construirse y al devolverlo, así nadie modifica el comprobante desde afuera. `getFilename` le pone la extensión que corresponde al tipo para que se descargue como un archivo reconocible.

## Guía de lectura

Datos y dependencias declaradas: `contentType`, `data`.

Operaciones para localizar en la fuente: `getContentType`, `getData`, `getFilename`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ReceiptRules]].

Referenciado por: [[InquiryController]], [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[ReceiptTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Receipt.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Receipt.java>), líneas 1–27.

```java
package ar.edu.itba.paw.models;

import java.util.Arrays;

// El comprobante que sube el comprador para una consulta en AWAITING_PAYMENT.
public final class Receipt {
    private final String contentType;
    private final byte[] data;

    public Receipt(final String contentType, final byte[] data) {
        this.contentType = contentType;
        this.data = Arrays.copyOf(data, data.length);
    }

    public String getContentType() {
        return contentType;
    }

    public byte[] getData() {
        return Arrays.copyOf(data, data.length);
    }

    // Con la extension que corresponde al tipo, para que se guarde como archivo reconocible.
    public String getFilename() {
        return "comprobante." + ReceiptRules.extensionOf(contentType);
    }
}
```
