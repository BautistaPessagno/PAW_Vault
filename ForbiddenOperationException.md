---
title: "ForbiddenOperationException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java"]
---

# ForbiddenOperationException

La operación existe pero no le corresponde a quien la pide: consultar un post propio, operar una consulta o una dirección ajena. [[ErrorResponseAdvice]] la convierte en 403.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AddressServiceImpl]], [[AddressServiceImplTest]], [[ErrorResponseAdvice]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java>), líneas 1–7.

```java
package ar.edu.itba.paw.services;

public class ForbiddenOperationException extends RuntimeException {
    public ForbiddenOperationException() {
        super("The authenticated user cannot perform this operation");
    }
}
```
