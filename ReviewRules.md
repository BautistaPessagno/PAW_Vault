---
title: "ReviewRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ReviewRules.java"]
---

# ReviewRules

Puntaje de 1 a 5 y comentario opcional de hasta 500 caracteres, con la misma normalización que un Mensaje. La comparten el formulario, la vista y [[ReviewServiceImpl]].

## Guía de lectura

Datos y dependencias declaradas: `MIN_RATING`, `MAX_RATING`, `MAX_BODY_LENGTH`.

Operaciones para localizar en la fuente: `normalize`, `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MessageRules]].

Referenciado por: [[InquiryController]], [[PublicProfileController]], [[ReviewForm]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ReviewRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewRules.java>), líneas 1–23.

```java
package ar.edu.itba.paw.models;

// Que calificacion y texto se aceptan en una Resena, compartido por el formulario, la vista y ReviewService.
public final class ReviewRules {

    public static final int MIN_RATING = 1;
    public static final int MAX_RATING = 5;
    public static final int MAX_BODY_LENGTH = 500;

    private ReviewRules() {
    }

    // Mismo criterio que MessageRules: CRLF a LF y recorte. null si no queda texto.
    public static String normalize(final String body) {
        return MessageRules.normalize(body);
    }

    // Espera el texto ya normalizado. Sin texto tambien vale: el comentario es opcional.
    public static boolean isValid(final int rating, final String normalizedBody) {
        return rating >= MIN_RATING && rating <= MAX_RATING
                && (normalizedBody == null || normalizedBody.length() <= MAX_BODY_LENGTH);
    }
}
```
