---
title: "SearchSuggestionController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java"]
---

# SearchSuggestionController

Public GET /search/suggestions?q= renders the search/suggestions fragment with up to five ARTIST or ALBUM suggestions drawn from available publications. The header search autocomplete requests it and submits the chosen value.

## Connections

Project types referenced: [[PostService]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java, lines 1–26](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class SearchSuggestionController {

    private final PostService postService;

    @Autowired
    public SearchSuggestionController(final PostService postService) {
        this.postService = postService;
    }

    @RequestMapping(value = "/search/suggestions", method = RequestMethod.GET)
    public ModelAndView suggestions(@RequestParam(value = "q", required = false) final String query) {
        return new ModelAndView("search/suggestions", "suggestions",
                postService.findSearchSuggestions(query));
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
