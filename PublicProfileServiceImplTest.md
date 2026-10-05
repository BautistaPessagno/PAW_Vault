---
title: "PublicProfileServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PublicProfileServiceImplTest.java"]
---

# PublicProfileServiceImplTest

Tests de `PublicProfileServiceImpl` en `services`: 1 casos declarados. Cubre: composición del perfil público con la página de reseñas del rol pedido. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `USER_ID`, `PAGE`, `publicProfileService`.

Operaciones para localizar en la fuente: `setUp`.

Casos declarados: 1.

- `testFindByUserIdWhenUserIsNotPublicReturnsUserNotFoundException`

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostService]], [[PublicProfileService]], [[PublicProfileServiceImpl]], [[ReviewService]], [[ReviewSubjectRole]], [[UserNotFoundException]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/PublicProfileServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PublicProfileServiceImplTest.java>), líneas 1–42.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.ReviewSubjectRole;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class PublicProfileServiceImplTest {
    private static final long USER_ID = 3;
    private static final int PAGE = 2;

    @Mock private UserService userService;
    @Mock private PostService postService;
    @Mock private ReviewService reviewService;
    private PublicProfileService publicProfileService;

    @BeforeEach
    public void setUp() {
        publicProfileService = new PublicProfileServiceImpl(userService, postService, reviewService);
    }

    @Test
    public void testFindByUserIdWhenUserIsNotPublicReturnsUserNotFoundException() {
        // 1. Arrange
        Mockito.when(userService.findPublicProfileById(USER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable find = () -> publicProfileService.findByUserId(USER_ID, PAGE, ReviewSubjectRole.SELLER, 1);

        // 3. Assert
        Assertions.assertThrows(UserNotFoundException.class, find);
    }
}
```
