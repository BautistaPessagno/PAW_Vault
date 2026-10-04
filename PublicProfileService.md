---
title: "PublicProfileService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java"]
---

# PublicProfileService

Contrato del perfil público: una operación que compone Cuenta, publicaciones y reseñas.

## Guía de lectura

Operaciones para localizar en la fuente: `findByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PublicProfile]].

Referenciado por: [[PublicProfileController]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java>), líneas 1–10.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.PublicProfile;

public interface PublicProfileService {

    // Lanza UserNotFoundException si la Cuenta no existe o no esta verificada, y
    // PageNotFoundException si la pagina de publicaciones no existe.
    PublicProfile findByUserId(long userId, int pageNumber);
}
```
