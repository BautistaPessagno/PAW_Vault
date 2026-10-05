---
title: "PostOrigin"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java"]
---

# PostOrigin

De dónde se llegó a una ficha: perfil público o perfil propio. `fromParameter` acepta el nombre del enum o su forma en minúsculas con guion y devuelve `null` ante cualquier otro valor, así la ruta de regreso no se arma con texto libre.

## Guía de lectura

Operaciones para localizar en la fuente: `fromParameter`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostController]], [[ProfileController]], [[PublicProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java>), líneas 1–19.

```java
package ar.edu.itba.paw.webapp.controller;

// Desde que perfil se abrio una publicacion: a donde vuelve el link de la ficha. Viaja como
// parametro origin en los links de los listados de perfil.
public enum PostOrigin {
    PUBLIC_PROFILE,
    PRIVATE_PROFILE;

    public static PostOrigin fromParameter(final String value) {
        if (value == null) {
            return null;
        }
        return switch (value) {
            case "PUBLIC_PROFILE", "public-profile" -> PUBLIC_PROFILE;
            case "PRIVATE_PROFILE", "private-profile" -> PRIVATE_PROFILE;
            default -> null;
        };
    }
}
```
