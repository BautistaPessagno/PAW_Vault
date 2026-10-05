---
title: "ReviewSubjectRole"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/ReviewSubjectRole.java"]
---

# ReviewSubjectRole

Rol que tenía la persona calificada en la venta: `SELLER` o `BUYER`. No es un permiso de la Cuenta: separa la reputación como vendedor de la reputación como comprador. Ver [[Reviews flow]].

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PublicProfileController]], [[PublicProfileService]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]], [[ReviewDao]], [[ReviewJdbcDao]], [[ReviewJdbcDaoTest]], [[ReviewPage]], [[ReviewService]], [[ReviewServiceImpl]], [[ReviewServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ReviewSubjectRole.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewSubjectRole.java>), líneas 1–6.

```java
package ar.edu.itba.paw.models;

// Rol de la persona reseñada en la venta, no un permiso de la cuenta.
public enum ReviewSubjectRole {
    SELLER, BUYER
}
```
