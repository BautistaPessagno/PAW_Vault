---
title: "AdminController"
categories: ["History"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "historical"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AdminController.java"]
---

# AdminController

> Histórico. Este archivo ya no existe con ese nombre en `41c32af`. El código inferior conserva su revisión original. El panel vacío fue retirado; ADMIN modera desde las publicaciones.

GET /admin renders admin/index. SecurityConfig enforces ADMIN access; the view currently contains navigation and an informational message, with no management operations.

## Connections

Project types referenced: none.

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AdminController.java, lines 1–15](<file:///Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AdminController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class AdminController {

    @RequestMapping(value = "/admin", method = RequestMethod.GET)
    public ModelAndView admin() {
        return new ModelAndView("admin/index");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
