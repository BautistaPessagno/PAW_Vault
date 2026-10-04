---
title: "PostOrigin"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java"]
---

# PostOrigin

De dónde se llegó a una ficha: perfil público o perfil propio. Al ser un enum, la ruta de regreso no se arma con texto libre.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostController]], [[ProfileController]], [[PublicProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java>), líneas 1–8.

```java
package ar.edu.itba.paw.webapp.controller;

// Desde que perfil se abrio una publicacion: a donde vuelve el link de la ficha. Viaja como
// parametro origin en los links de los listados de perfil.
public enum PostOrigin {
    PUBLIC_PROFILE,
    PRIVATE_PROFILE
}
```
