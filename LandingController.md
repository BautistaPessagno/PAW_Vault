---
title: "LandingController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java"]
---

# LandingController

Handles only GET `/`. It calls [[PostService]].getFeatured, adds the result under the exact model key `posts`, and returns logical view `landing/index`. [[WebConfig]] resolves that to `/WEB-INF/views/landing/index.jsp`. The JSP iterates [[PostSummary]] rows and links each Post ID to contact. See [[Landing flow]].

## Connections

Project types referenced: [[PostService]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class LandingController {

    private final PostService postService;

    @Autowired
    public LandingController(final PostService postService) {
        this.postService = postService;
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public ModelAndView landing() {
        final ModelAndView mav = new ModelAndView("landing/index");
        mav.addObject("posts", postService.getFeatured());
        return mav;
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
