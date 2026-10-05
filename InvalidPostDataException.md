---
title: "InvalidPostDataException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java"]
---

# InvalidPostDataException

Defensa del contrato de [[PostServiceImpl]]: año o precio fuera de rango. La validación web debería impedir que llegue en un pedido normal.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ErrorResponseAdvice]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java>), líneas 1–6.

```java
package ar.edu.itba.paw.services;

// Defensa del contrato del service: la validacion web deberia impedir que esta
// excepcion llegue a una solicitud normal.
public class InvalidPostDataException extends RuntimeException {
}
```
