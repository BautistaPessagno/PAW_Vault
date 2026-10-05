---
title: "AddressLimitExceededException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/AddressLimitExceededException.java"]
---

# AddressLimitExceededException

La Cuenta ya tiene el máximo de direcciones activas. La lanza [[AddressServiceImpl]]; el perfil, el contacto y el carrito la muestran como aviso.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AddressServiceImpl]], [[AddressServiceImplTest]], [[CartExceptionAdvice]], [[PostContactController]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/AddressLimitExceededException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressLimitExceededException.java>), líneas 1–4.

```java
package ar.edu.itba.paw.services;

public class AddressLimitExceededException extends RuntimeException {
}
```
