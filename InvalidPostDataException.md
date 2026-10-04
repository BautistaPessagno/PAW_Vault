---
title: "InvalidPostDataException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java"]
---

# InvalidPostDataException

Defensa del contrato de [[PostServiceImpl]]: año o precio fuera de rango. La validación web debería impedir que llegue en un pedido normal.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java>), líneas 1–6.

```java
package ar.edu.itba.paw.services;

// Defensa del contrato del service: la validacion web deberia impedir que esta
// excepcion llegue a una solicitud normal.
public class InvalidPostDataException extends RuntimeException {
}
```
