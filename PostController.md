---
title: "PostController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java"]
---

# PostController

Public GET /post/{id} renders post/detail for any existing publication, including sold ones. The JSP shows edit/delete actions only to the owner of an AVAILABLE post, and a contact button to everyone else while it is available. PostNotFoundException maps to 404.

## Connections

Project types referenced: [[PostNotFoundException]], [[PostService]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java, lines 1–38](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;

// La ficha de la publicacion es publica: el contacto sigue pidiendo sesion en su propio controller.
@Controller
public class PostController {

    private final PostService postService;

    @Autowired
    public PostController(final PostService postService) {
        this.postService = postService;
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}", method = RequestMethod.GET)
    public ModelAndView detail(@PathVariable("postId") final long postId) {
        final ModelAndView modelAndView = new ModelAndView("post/detail");
        modelAndView.addObject("post", postService.findById(postId));
        return modelAndView;
    }

    @ExceptionHandler(PostNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView postNotFound() {
        return new ModelAndView("error/404");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
