---
title: "PublicProfileServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java"]
---

# PublicProfileServiceImpl

Compone el perfil público con la Cuenta verificada, sus publicaciones disponibles y sus reseñas. Vive aparte porque [[PostService]] ya depende de [[UserService]]. Ver [[Public profile flow]].

## Guía de lectura

Datos y dependencias declaradas: `userService`, `postService`, `reviewService`.

Operaciones para localizar en la fuente: `findByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostService]], [[PublicProfile]], [[PublicProfileService]], [[PublicUserProfile]], [[ReviewService]], [[UserNotFoundException]], [[UserService]].

Referenciado por: [[PublicProfileServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java>), líneas 1–36.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.PublicProfile;
import ar.edu.itba.paw.models.PublicUserProfile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/*
 * Arma el perfil publico con lo de cada dominio: la Cuenta, sus publicaciones a la venta y sus
 * Resenas. Vive aparte porque PostService ya depende de UserService.
 */
@Service
public class PublicProfileServiceImpl implements PublicProfileService {

    private final UserService userService;
    private final PostService postService;
    private final ReviewService reviewService;

    @Autowired
    public PublicProfileServiceImpl(final UserService userService, final PostService postService,
                                    final ReviewService reviewService) {
        this.userService = userService;
        this.postService = postService;
        this.reviewService = reviewService;
    }

    @Override
    @Transactional(readOnly = true)
    public PublicProfile findByUserId(final long userId, final int pageNumber) {
        final PublicUserProfile user = userService.findPublicProfileById(userId)
                .orElseThrow(UserNotFoundException::new);
        return new PublicProfile(user, postService.findAvailableByPublisherId(userId, pageNumber),
                reviewService.statsForUser(userId), reviewService.findRecentForUser(userId));
    }
}
```
