---
title: "UserNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java"]
---

# UserNotFoundException

La Cuenta no existe, o no tiene perfil público. [[ErrorResponseAdvice]] responde 404.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AuthenticationController]], [[ErrorResponseAdvice]], [[InquiryServiceImpl]], [[PostServiceImpl]], [[ProfileController]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java>), líneas 1–7.

```java
package ar.edu.itba.paw.services;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException() {
        super("User not found");
    }
}
```
