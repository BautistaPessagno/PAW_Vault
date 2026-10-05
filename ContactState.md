---
title: "ContactState"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ContactState.java"]
---

# ContactState

Qué puede hacer una Cuenta con un post: `CONTACTABLE`, `OPEN_INQUIRY`, `UNAVAILABLE` u `OWN_POST`. Lo calcula [[ContactRules]] y lo usan el contacto, el carrito y la ficha.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartServiceImpl]], [[CartServiceImplTest]], [[ContactRules]], [[ContactRulesTest]], [[PostContactOptions]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ContactState.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ContactState.java>), líneas 1–9.

```java
package ar.edu.itba.paw.models;

// Que puede hacer una Cuenta con un Post: consultarlo, seguir en su Consulta abierta o nada.
public enum ContactState {
    CONTACTABLE,
    OPEN_INQUIRY,
    UNAVAILABLE,
    OWN_POST
}
```
