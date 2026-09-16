---
title: "ErrorController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java"]
---

# ErrorController

Renders HTTP 403 and 404 pages for all enumerated request verbs. web.xml forwards unmatched-route 404s here so MVC supplies view and locale resolution. Search/contact/inquiry handlers return their own 400/409 views.

## Connections

Project types referenced: none.

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java, lines 1–38](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
