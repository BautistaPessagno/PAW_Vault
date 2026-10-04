---
title: "OpenInquiryExistsException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/OpenInquiryExistsException.java"]
---

# OpenInquiryExistsException

El comprador ya tiene una Consulta abierta sobre ese post. Lleva su id para redirigirlo a esa conversación.

## Guía de lectura

Datos y dependencias declaradas: `inquiryId`.

Operaciones para localizar en la fuente: `getInquiryId`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartExceptionAdvice]], [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/OpenInquiryExistsException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/OpenInquiryExistsException.java>), líneas 1–15.

```java
package ar.edu.itba.paw.services;

// El comprador ya tiene una Consulta abierta sobre el post: lleva su id para mandarlo a esa Conversacion.
public class OpenInquiryExistsException extends RuntimeException {

    private final long inquiryId;

    public OpenInquiryExistsException(final long inquiryId) {
        this.inquiryId = inquiryId;
    }

    public long getInquiryId() {
        return inquiryId;
    }
}
```
