---
title: "ReceiptValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java"]
---

# ReceiptValidator

Valida el comprobante con [[ReceiptRules]] mirando el tamaño antes de leer los bytes.

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ReceiptRules]], [[ValidReceipt]].

Referenciado por: [[ValidReceipt]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java>), líneas 1–29.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.models.ReceiptRules;
import org.springframework.web.multipart.MultipartFile;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import java.io.IOException;

/*
 * Segunda capa del limite: el resolver multipart corta el request entero a los 6 MB, y este
 * validador deja el comprobante en el tope de ReceiptRules con un error bajo el campo. La
 * regla es la misma que aplica InquiryService al guardarlo.
 */
public class ReceiptValidator implements ConstraintValidator<ValidReceipt, MultipartFile> {

    @Override
    public boolean isValid(final MultipartFile file, final ConstraintValidatorContext context) {
        // El tamanio se mira antes de leer los bytes: no hace falta cargar un archivo que ya sobra.
        if (file == null || file.isEmpty() || file.getSize() > ReceiptRules.MAX_BYTES) {
            return false;
        }
        try {
            return ReceiptRules.isValid(ReceiptRules.normalizeContentType(file.getContentType()), file.getBytes());
        } catch (final IOException e) {
            return false;
        }
    }
}
```
