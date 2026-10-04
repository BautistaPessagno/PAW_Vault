---
title: "UserRole"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/UserRole.java"]
---

# UserRole

Roles de una Cuenta: `USER` y `ADMIN`. El administrador conserva lo de una Cuenta común y además puede editar y eliminar publicaciones disponibles ajenas.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AuthenticatedUser]], [[EmailServiceImplTest]], [[InquiryServiceImplTest]], [[PostServiceImplTest]], [[User]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/UserRole.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/UserRole.java>), líneas 1–6.

```java
package ar.edu.itba.paw.models;

public enum UserRole {
    USER,
    ADMIN
}
```
