---
title: "NothingToSendException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/NothingToSendException.java"]
---

# NothingToSendException

Al enviar el carrito, ningún post se podía consultar. No se escribe nada y se vuelve al carrito con un aviso.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartExceptionAdvice]], [[CartServiceImpl]], [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/NothingToSendException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/NothingToSendException.java>), líneas 1–5.

```java
package ar.edu.itba.paw.services;

// Al enviar, ningun Post del carrito se podia consultar: no se escribe nada.
public class NothingToSendException extends RuntimeException {
}
```
