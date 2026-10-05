---
title: "InvalidCurrentPasswordException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java"]
---

# InvalidCurrentPasswordException

La contraseña actual no coincide, o cambió entre la lectura y el `UPDATE`. El perfil la muestra en el campo de clave actual.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ProfileController]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java>), líneas 1–7.

```java
package ar.edu.itba.paw.services;

public class InvalidCurrentPasswordException extends RuntimeException {
    public InvalidCurrentPasswordException() {
        super("The current password is incorrect");
    }
}
```
