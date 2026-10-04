---
title: "PublicProfileController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java"]
---

# PublicProfileController

`GET /users/{id}`: perfil público con publicaciones a la venta y reseñas. Ver [[Public profile flow]].

## Guía de lectura

Datos y dependencias declaradas: `publicProfileService`.

Operaciones para localizar en la fuente: `show`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostOrigin]], [[PublicProfileService]], [[ReviewRules]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java>), líneas 1–31.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.ReviewRules;
import ar.edu.itba.paw.services.PublicProfileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class PublicProfileController {
    private final PublicProfileService publicProfileService;

    @Autowired
    public PublicProfileController(final PublicProfileService publicProfileService) {
        this.publicProfileService = publicProfileService;
    }

    @RequestMapping(value = "/users/{id:[0-9]+}", method = RequestMethod.GET)
    public ModelAndView show(@PathVariable("id") final long id,
                             @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final ModelAndView view = new ModelAndView("profile/public");
        view.addObject("profile", publicProfileService.findByUserId(id, pageNumber));
        view.addObject("postOrigin", PostOrigin.PUBLIC_PROFILE);
        view.addObject("maxRating", ReviewRules.MAX_RATING);
        return view;
    }
}
```
