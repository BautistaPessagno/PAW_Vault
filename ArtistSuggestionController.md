---
title: "ArtistSuggestionController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java"]
---

# ArtistSuggestionController

Public GET /artists/suggestions?q= renders the artist/suggestions fragment: up to five artist names as listbox options for the publish-form autocomplete. Blank or oversized queries yield an empty fragment.

## Connections

Project types referenced: [[ArtistService]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java, lines 1–25](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ArtistService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ArtistSuggestionController {

    private final ArtistService artistService;

    @Autowired
    public ArtistSuggestionController(final ArtistService artistService) {
        this.artistService = artistService;
    }

    @RequestMapping(value = "/artists/suggestions", method = RequestMethod.GET)
    public ModelAndView suggestions(@RequestParam(value = "q", required = false) final String query) {
        return new ModelAndView("artist/suggestions", "artists", artistService.findSuggestions(query));
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
