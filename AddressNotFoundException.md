---
title: "AddressNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AddressNotFoundException.java"]
---

# AddressNotFoundException

La dirección no existe, es de otra Cuenta o está archivada. [[ErrorResponseAdvice]] la convierte en 404; el contacto y el carrito la tratan como "elegí otra".

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartExceptionAdvice]], [[CartServiceImpl]], [[CartServiceImplTest]], [[ErrorResponseAdvice]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/AddressNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressNotFoundException.java>), líneas 1–4.

```java
package ar.edu.itba.paw.services;

public class AddressNotFoundException extends RuntimeException {
}
```
