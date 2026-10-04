---
title: "ArtistSuggestionController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java"]
---

# ArtistSuggestionController

`GET /artists/suggestions`: devuelve en JSON hasta cinco artistas para el autocompletado del formulario de publicar. Ver [[Search suggestions flow]].

## Guía de lectura

Datos y dependencias declaradas: `artistService`.

Operaciones para localizar en la fuente: `suggestions`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ArtistService]], [[ArtistSuggestionDto]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java>), líneas 1–34.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ArtistService;
import ar.edu.itba.paw.webapp.dto.ArtistSuggestionDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;
import java.util.stream.Collectors;

@Controller
public class ArtistSuggestionController {

    private final ArtistService artistService;

    @Autowired
    public ArtistSuggestionController(final ArtistService artistService) {
        this.artistService = artistService;
    }

    @RequestMapping(value = "/artists/suggestions", method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public List<ArtistSuggestionDto> suggestions(@RequestParam(value = "q", required = false) final String query) {
        return artistService.findSuggestions(query).stream()
                .map(artist -> new ArtistSuggestionDto(artist.getName()))
                .collect(Collectors.toList());
    }
}
```
