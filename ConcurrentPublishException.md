---
title: "ConcurrentPublishException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java"]
---

# ConcurrentPublishException

Otra publicación simultánea creó el mismo artista o álbum. Esa transacción ya hizo commit, así que reintentar funciona. El formulario lo muestra como error global.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostServiceImpl]], [[PublishController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java>), líneas 1–8.

```java
package ar.edu.itba.paw.services;

/**
 * Otra publicacion simultanea creo el mismo artista, album o usuario. Su transaccion
 * ya commiteo, asi que reintentar la publicacion funciona.
 */
public class ConcurrentPublishException extends RuntimeException {
}
```
