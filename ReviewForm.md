---
title: "ReviewForm"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReviewForm.java"]
---

# ReviewForm

Reseña: puntaje obligatorio de 1 a 5 y comentario opcional hasta 500. `of` precarga la reseña vigente para editarla.

## Guía de lectura

Datos y dependencias declaradas: `rating`, `body`.

Operaciones para localizar en la fuente: `of`, `getRating`, `setRating`, `getBody`, `setBody`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Review]], [[ReviewRules]].

Referenciado por: [[InquiryController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReviewForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReviewForm.java>), líneas 1–35.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.ReviewRules;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

public class ReviewForm {
    @NotNull(message = "{review.rating.required}")
    @Min(value = ReviewRules.MIN_RATING, message = "{review.rating.invalid}")
    @Max(value = ReviewRules.MAX_RATING, message = "{review.rating.invalid}")
    private Integer rating;

    // Llega ya normalizado por LineBreakNormalizingEditor: los saltos cuentan uno, como en el textarea.
    @Size(max = ReviewRules.MAX_BODY_LENGTH, message = "{review.body.size}")
    private String body;

    // El formulario con la Resena vigente, para editarla; vacio si todavia no califico.
    public static ReviewForm of(final Review review) {
        final ReviewForm form = new ReviewForm();
        if (review != null) {
            form.setRating(review.getRating());
            form.setBody(review.getBody());
        }
        return form;
    }

    public Integer getRating() { return rating; }
    public void setRating(final Integer rating) { this.rating = rating; }
    public String getBody() { return body; }
    public void setBody(final String body) { this.body = body; }
}
```
