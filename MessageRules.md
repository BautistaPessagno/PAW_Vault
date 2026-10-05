---
title: "MessageRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/MessageRules.java"]
---

# MessageRules

Qué texto se acepta como Mensaje: normaliza CRLF a LF, recorta y exige hasta 500 caracteres. La comparten el formulario y [[InquiryServiceImpl]].

## Guía de lectura

Datos y dependencias declaradas: `MAX_LENGTH`.

Operaciones para localizar en la fuente: `normalize`, `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[LineBreakNormalizingEditor]], [[MessageForm]], [[ReviewRules]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/MessageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/MessageRules.java>), líneas 1–24.

```java
package ar.edu.itba.paw.models;

// Que texto se acepta como Mensaje, compartido por el formulario y por InquiryService.
public final class MessageRules {

    public static final int MAX_LENGTH = 500;

    private MessageRules() {
    }

    // Unico lugar que normaliza: CRLF a LF y recorte. null si no queda texto.
    public static String normalize(final String body) {
        if (body == null) {
            return null;
        }
        final String normalized = body.replace("\r\n", "\n").trim();
        return normalized.isEmpty() ? null : normalized;
    }

    // Espera el texto ya normalizado.
    public static boolean isValid(final String normalized) {
        return normalized != null && normalized.length() <= MAX_LENGTH;
    }
}
```
