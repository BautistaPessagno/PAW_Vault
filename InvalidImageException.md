---
title: "InvalidImageException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java"]
---

# InvalidImageException

La imagen no cumple [[ImageRules]], o al editar se intenta retirar una foto ajena o superar el tope. Los formularios la muestran junto al campo; fuera de ellos, [[ErrorResponseAdvice]] responde 400.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ErrorResponseAdvice]], [[ImageServiceImpl]], [[ImageServiceImplTest]], [[InMemoryImageService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java>), líneas 1–4.

```java
package ar.edu.itba.paw.services;

public class InvalidImageException extends RuntimeException {
}
```
