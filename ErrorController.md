---
title: "ErrorController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java"]
---

# ErrorController

Vistas de 403 y 404 a las que hacen forward Spring Security y el contenedor. Pasar por un controller hace que el error use el mismo view resolver y el mismo `Locale` que el resto.

## Guía de lectura

Operaciones para localizar en la fuente: `notFound`, `forbidden`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java>), líneas 1–38.

```java
package ar.edu.itba.paw.webapp.controller;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ErrorController {

    /*
     * El contenedor forwardea aca cuando ninguna ruta matchea (ver <error-page> en web.xml).
     * Pasar por un controller y no directo a la JSP es lo que hace que el 404 se renderice
     * con el mismo view resolver y el mismo locale que el resto de la app.
     *
     * El forward conserva el metodo original, por eso se enumeran todos los verbos que
     * puede recibir una URL inexistente en vez de limitar el handler a GET.
     */
    @RequestMapping(value = "/error/404", method = {
            RequestMethod.GET, RequestMethod.HEAD, RequestMethod.POST, RequestMethod.PUT,
            RequestMethod.PATCH, RequestMethod.DELETE, RequestMethod.OPTIONS, RequestMethod.TRACE
    })
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @RequestMapping(value = "/error/403", method = {
            RequestMethod.GET, RequestMethod.HEAD, RequestMethod.POST, RequestMethod.PUT,
            RequestMethod.PATCH, RequestMethod.DELETE, RequestMethod.OPTIONS, RequestMethod.TRACE
    })
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }
}
```
