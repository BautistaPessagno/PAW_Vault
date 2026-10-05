---
title: "ErrorResponseAdvice"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java"]
---

# ErrorResponseAdvice

Único lugar donde las excepciones de negocio se vuelven respuestas: no encontrado → 404, ajeno → 403, dato que saltea la validación (imagen, reseña, datos del post o de cobro) o parámetro mal tipado → 400. Ver [[Security and authorization]] y [[Validation and errors]].

## Guía de lectura

Operaciones para localizar en la fuente: `notFound`, `forbidden`, `badRequest`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressNotFoundException]], [[ForbiddenOperationException]], [[InquiryNotFoundException]], [[InvalidImageException]], [[InvalidPaymentInfoException]], [[InvalidPostDataException]], [[InvalidReviewException]], [[PageNotFoundException]], [[PostNotFoundException]], [[ReceiptNotFoundException]], [[UserNotFoundException]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>), líneas 1–52.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.AddressNotFoundException;
import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InquiryNotFoundException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.InvalidPaymentInfoException;
import ar.edu.itba.paw.services.InvalidPostDataException;
import ar.edu.itba.paw.services.InvalidReviewException;
import ar.edu.itba.paw.services.PageNotFoundException;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.ReceiptNotFoundException;
import ar.edu.itba.paw.services.UserNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.web.servlet.ModelAndView;

/*
 * Unico lugar donde las excepciones de pertenencia, de recurso inexistente y de datos que los
 * formularios ya validan se vuelven respuestas: un recurso que no existe es 404, uno que existe
 * pero es ajeno, 403, y un dato que no cumple las reglas del dominio, 400.
 */
@ControllerAdvice
public class ErrorResponseAdvice {

    @ExceptionHandler({PostNotFoundException.class, InquiryNotFoundException.class,
            UserNotFoundException.class, PageNotFoundException.class, AddressNotFoundException.class,
            ReceiptNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    // Los formularios aplican las mismas ImageRules, ReviewRules, VinylInputRules y PaymentInfoRules:
    // solo llega aca un POST que se salteo la validacion. Un parametro de la URL que no es del tipo
    // esperado (una pagina que no es un numero, un origin desconocido) tambien es un pedido mal armado.
    @ExceptionHandler({InvalidImageException.class, InvalidReviewException.class, InvalidPostDataException.class,
            InvalidPaymentInfoException.class, MethodArgumentTypeMismatchException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView badRequest() {
        return new ModelAndView("error/400");
    }
}
```
