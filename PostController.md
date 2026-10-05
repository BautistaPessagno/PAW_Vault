---
title: "PostController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java"]
---

# PostController

Ficha pública `GET /post/{id}`: pide a [[CartService]] la ficha con lo que se le ofrece a quien mira y resuelve a dónde volver. `origin`, `originPage` y `postStatus` llegan como texto y un valor inválido solo pierde el regreso o el filtro. Ver [[Post detail flow]].

## Guía de lectura

Datos y dependencias declaradas: `cartService`.

Operaciones para localizar en la fuente: `detail`, `returnPage`, `returnStatus`, `returnProfilePath`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[CartService]], [[PostDetail]], [[PostOrigin]], [[PostStatus]], [[PostView]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java>), líneas 1–83.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostView;
import ar.edu.itba.paw.services.CartService;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

// La ficha de la publicacion es publica: el contacto sigue pidiendo sesion en su propio controller.
@Controller
public class PostController {

    private final CartService cartService;

    @Autowired
    public PostController(final CartService cartService) {
        this.cartService = cartService;
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}", method = RequestMethod.GET)
    public ModelAndView detail(@PathVariable("postId") final long postId,
                               @RequestParam(value = "from", required = false) final String returnQuery,
                               @RequestParam(value = "origin", required = false) final String origin,
                               @RequestParam(value = "originPage", defaultValue = "1") final String originPage,
                               @RequestParam(value = "postStatus", required = false) final String originStatus,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final ModelAndView modelAndView = new ModelAndView("post/detail");
        final PostView view = cartService.findPostView(postId, currentUser == null ? null : currentUser.getId(),
                currentUser != null && currentUser.isAdmin());
        final PostDetail detail = view.getDetail();
        modelAndView.addObject("detail", detail);
        modelAndView.addObject("contact", view.getContact());
        modelAndView.addObject("post", detail.getPost());
        final String profilePath = returnProfilePath(PostOrigin.fromParameter(origin), detail);
        if (profilePath != null) {
            modelAndView.addObject("returnProfilePath", profilePath);
            modelAndView.addObject("returnProfilePage", returnPage(originPage));
            modelAndView.addObject("returnPostStatus", returnStatus(originStatus));
        }
        // Query string del listado de origen. Solo se usa detras de "/?", asi que no puede
        // sacar al usuario de la aplicacion.
        modelAndView.addObject("returnQuery", returnQuery);
        return modelAndView;
    }

    // Es contexto de navegacion opcional, no el parametro page del listado: un valor
    // viejo o mal formado no debe impedir abrir una publicacion valida.
    private static int returnPage(final String value) {
        try {
            return Math.max(1, Integer.parseInt(value));
        } catch (final NumberFormatException e) {
            return 1;
        }
    }

    // Mismo criterio que returnPage: un filtro desconocido vuelve al listado sin filtrar.
    private static PostStatus returnStatus(final String value) {
        if (value == null) {
            return null;
        }
        try {
            return PostStatus.valueOf(value);
        } catch (final IllegalArgumentException e) {
            return null;
        }
    }

    // Solo se vuelve a un perfil conocido: el publico del Publicante, o el propio si el mismo Publicante abre su Post.
    private static String returnProfilePath(final PostOrigin origin, final PostDetail detail) {
        if (origin == PostOrigin.PUBLIC_PROFILE) {
            return "/users/" + detail.getPost().getUserId();
        }
        return origin == PostOrigin.PRIVATE_PROFILE && detail.isOwnedByViewer() ? "/profile" : null;
    }
}
```
