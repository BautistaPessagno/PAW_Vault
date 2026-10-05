---
title: "SearchSuggestionController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java"]
---

# SearchSuggestionController

`GET /search/suggestions`: sugerencias de álbum y artista en JSON, con la etiqueta del tipo traducida en el servidor. Ver [[Search suggestions flow]].

## Guía de lectura

Datos y dependencias declaradas: `postService`, `messageSource`.

Operaciones para localizar en la fuente: `suggestions`, `toDto`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostService]], [[SearchSuggestion]], [[SearchSuggestionDto]], [[SearchSuggestionType]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java>), líneas 1–49.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchSuggestionType;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.webapp.dto.SearchSuggestionDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

@Controller
public class SearchSuggestionController {

    private final PostService postService;
    private final MessageSource messageSource;

    @Autowired
    public SearchSuggestionController(final PostService postService, final MessageSource messageSource) {
        this.postService = postService;
        this.messageSource = messageSource;
    }

    // Devuelve datos y no HTML: el componente de autocompletado arma las opciones en el navegador.
    @RequestMapping(value = "/search/suggestions", method = RequestMethod.GET,
            produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public List<SearchSuggestionDto> suggestions(@RequestParam(value = "q", required = false) final String query,
                                                 final Locale locale) {
        return postService.findSearchSuggestions(query).stream()
                .map(suggestion -> toDto(suggestion, locale))
                .collect(Collectors.toList());
    }

    private SearchSuggestionDto toDto(final SearchSuggestion suggestion, final Locale locale) {
        final SearchSuggestionType type = suggestion.getType();
        final String typeLabel = messageSource.getMessage("search.suggestion." + type.name(), null, locale);
        final String detail = type == SearchSuggestionType.ALBUM ? suggestion.getArtistName() : null;
        return new SearchSuggestionDto(suggestion.getValue(), type.name(), typeLabel, detail);
    }
}
```
