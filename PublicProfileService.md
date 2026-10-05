---
title: "PublicProfileService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java"]
---

# PublicProfileService

Contrato del perfil público: una operación que compone Cuenta, publicaciones y una página de reseñas del rol pedido.

## Guía de lectura

Operaciones para localizar en la fuente: `findByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PublicProfile]], [[ReviewSubjectRole]].

Referenciado por: [[PublicProfileController]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java>), líneas 1–11.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.PublicProfile;
import ar.edu.itba.paw.models.ReviewSubjectRole;

public interface PublicProfileService {

    // Lanza UserNotFoundException si la Cuenta no existe o no esta verificada, y
    // PageNotFoundException si la pagina de publicaciones o de reseñas no existe.
    PublicProfile findByUserId(long userId, int pageNumber, ReviewSubjectRole reviewRole, int reviewPageNumber);
}
```
