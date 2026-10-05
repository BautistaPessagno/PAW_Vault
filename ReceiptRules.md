---
title: "ReceiptRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java"]
---

# ReceiptRules

Qué comprobante se acepta: PDF, PNG, JPEG o WEBP de hasta 5 MiB; el PDF tiene que empezar con la firma `%PDF-`. La comparten [[ReceiptValidator]] e [[InquiryServiceImpl]].

## Guía de lectura

Datos y dependencias declaradas: `MAX_BYTES`, `PDF`, `EXTENSIONS`, `PDF_SIGNATURE`.

Operaciones para localizar en la fuente: `normalizeContentType`, `isValid`, `extensionOf`, `startsWith`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[Receipt]], [[ReceiptValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java>), líneas 1–47.

```java
package ar.edu.itba.paw.models;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Locale;
import java.util.Map;

// Que comprobante se acepta, compartido por el validador del formulario y por InquiryService.
public final class ReceiptRules {

    public static final long MAX_BYTES = 5L * 1024 * 1024;

    private static final String PDF = "application/pdf";
    // Tipo aceptado -> extension con la que se descarga.
    private static final Map<String, String> EXTENSIONS = Map.of(
            PDF, "pdf", "image/png", "png", "image/jpeg", "jpg", "image/webp", "webp");
    // El PDF se sirve sin sandbox (el visor de Chrome no lo abre con sandbox): se exige que el
    // contenido lo sea de verdad y no solo el tipo que declaro el navegador.
    private static final byte[] PDF_SIGNATURE = "%PDF-".getBytes(StandardCharsets.US_ASCII);

    private ReceiptRules() {
    }

    // Unico lugar que normaliza: lo que se guarda es igual a lo que se valido.
    public static String normalizeContentType(final String contentType) {
        return contentType == null ? null : contentType.trim().toLowerCase(Locale.ROOT);
    }

    // Espera el tipo ya normalizado.
    public static boolean isValid(final String contentType, final byte[] data) {
        if (contentType == null || !EXTENSIONS.containsKey(contentType)) {
            return false;
        }
        if (data == null || data.length == 0 || data.length > MAX_BYTES) {
            return false;
        }
        return !PDF.equals(contentType) || startsWith(data, PDF_SIGNATURE);
    }

    public static String extensionOf(final String contentType) {
        return EXTENSIONS.get(contentType);
    }

    private static boolean startsWith(final byte[] data, final byte[] prefix) {
        return data.length >= prefix.length && Arrays.equals(data, 0, prefix.length, prefix, 0, prefix.length);
    }
}
```
