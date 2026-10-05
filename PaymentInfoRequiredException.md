---
title: "PaymentInfoRequiredException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PaymentInfoRequiredException.java"]
---

# PaymentInfoRequiredException

No se pueden vaciar los datos de cobro con una venta abierta: el comprador se quedaría sin dónde transferir.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ProfileController]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PaymentInfoRequiredException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PaymentInfoRequiredException.java>), líneas 1–5.

```java
package ar.edu.itba.paw.services;

// Borrar los datos de cobro con una venta abierta dejaria al comprador sin a donde transferir.
public class PaymentInfoRequiredException extends RuntimeException {
}
```
