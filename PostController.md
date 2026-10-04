---
title: "PostController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java"]
---

# PostController

Ficha pública `GET /post/{id}`: pide a [[CartService]] la ficha con lo que se le ofrece a quien mira y resuelve a dónde volver. Ver [[Post detail flow]].

## Guía de lectura

Datos y dependencias declaradas: `cartService`.

Operaciones para localizar en la fuente: `detail`, `returnProfilePath`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[CartService]], [[PostDetail]], [[PostOrigin]], [[PostView]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java>), líneas 1–58.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostDetail;
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
                               @RequestParam(value = "origin", required = false) final PostOrigin origin,
                               @RequestParam(value = "originPage", defaultValue = "1") final int originPage,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final ModelAndView modelAndView = new ModelAndView("post/detail");
        final PostView view = cartService.findPostView(postId, currentUser == null ? null : currentUser.getId(),
                currentUser != null && currentUser.isAdmin());
        final PostDetail detail = view.getDetail();
        modelAndView.addObject("detail", detail);
        modelAndView.addObject("contact", view.getContact());
        modelAndView.addObject("post", detail.getPost());
        final String profilePath = returnProfilePath(origin, detail);
        if (profilePath != null) {
            modelAndView.addObject("returnProfilePath", profilePath);
            modelAndView.addObject("returnProfilePage", originPage);
        }
        // Query string del listado de origen. Solo se usa detras de "/?", asi que no puede
        // sacar al usuario de la aplicacion.
        modelAndView.addObject("returnQuery", returnQuery);
        return modelAndView;
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
