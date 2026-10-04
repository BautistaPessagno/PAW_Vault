---
title: "LandingController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java"]
---

# LandingController

Catálogo en `GET /`: liga los filtros de la URL ignorando valores de enum inválidos y delega todo en [[PostService]]; muestra como activo lo que el service aplicó. Ver [[Landing flow]].

## Guía de lectura

Datos y dependencias declaradas: `postService`, `parser`.

Operaciones para localizar en la fuente: `initBinder`, `upperCase`, `IgnoreInvalidEditor`, `setAsText`, `landing`, `invalidSearchQuery`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CatalogFilterForm]], [[Condition]], [[Genre]], [[InvalidSearchQueryException]], [[PostSearchCriteria]], [[PostService]], [[PostSort]], [[SearchResult]], [[VinylInputRules]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>), líneas 1–120.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.VinylInputRules;
import ar.edu.itba.paw.services.InvalidSearchQueryException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.webapp.form.CatalogFilterForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import java.beans.PropertyEditorSupport;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.function.Function;

@Controller
public class LandingController {

    private final PostService postService;

    @Autowired
    public LandingController(final PostService postService) {
        this.postService = postService;
    }

    // Los valores cerrados o legacy que no se entienden se ignoran. Los Integer no usan
    // este editor: Spring conserva el valor rechazado para mostrar un error junto al campo.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(PostSort.class, new IgnoreInvalidEditor(text -> PostSort.valueOf(upperCase(text))));
        binder.registerCustomEditor(Genre.class, new IgnoreInvalidEditor(text -> Genre.valueOf(upperCase(text))));
        binder.registerCustomEditor(Condition.class, new IgnoreInvalidEditor(text -> Condition.valueOf(upperCase(text))));
        binder.registerCustomEditor(Long.class, new IgnoreInvalidEditor(Long::valueOf));
    }

    private static String upperCase(final String text) {
        return text.toUpperCase(Locale.ROOT);
    }

    private static final class IgnoreInvalidEditor extends PropertyEditorSupport {

        private final Function<String, Object> parser;

        private IgnoreInvalidEditor(final Function<String, Object> parser) {
            this.parser = parser;
        }

        // valueOf tira IllegalArgumentException cuando el texto no es un valor valido,
        // y NumberFormatException la extiende: en los dos casos el filtro queda sin pedir.
        @Override
        public void setAsText(final String text) {
            try {
                setValue(parser.apply(text.trim()));
            } catch (final IllegalArgumentException e) {
                setValue(null);
            }
        }
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public ModelAndView landing(@Valid @ModelAttribute("catalogFilterForm") final CatalogFilterForm form,
                                final BindingResult bindingResult,
                                @RequestParam(value = "page", defaultValue = "1") final int pageNumber,
                                final HttpServletRequest request) {
        // Un filtro invalido no corta la busqueda: el service lo ignora y aplica el resto, incluida
        // la pagina. Lo que se muestra como activo es lo que el service aplico, no lo que llego.
        final SearchResult result = postService.search(form.toCriteria(), pageNumber);
        final PostSearchCriteria applied = result.getCriteria();
        final ModelAndView mav = new ModelAndView("landing/index");
        mav.addObject("query", result.getQuery());
        mav.addObject("total", result.getTotal());
        mav.addObject("sort", applied.getSort());
        mav.addObject("sorts", PostSort.values());
        mav.addObject("genres", Genre.values());
        mav.addObject("conditions", Condition.values());
        mav.addObject("selectedGenre", applied.getGenre());
        mav.addObject("selectedCondition", applied.getCondition());
        mav.addObject("selectedArtistId", applied.getArtistId());
        mav.addObject("selectedYear", applied.getReleaseYear());
        mav.addObject("minPrice", applied.getMinPrice());
        mav.addObject("maxPrice", applied.getMaxPrice());
        mav.addObject("catalogFilterErrors", bindingResult.hasErrors());
        mav.addObject("minimumYear", VinylInputRules.MIN_YEAR);
        mav.addObject("currentYear", VinylInputRules.currentYear());
        mav.addObject("minimumPrice", VinylInputRules.MIN_PRICE);
        mav.addObject("maximumPrice", VinylInputRules.MAX_PRICE);
        mav.addObject("posts", result.getPage().getPosts());
        mav.addObject("postPage", result.getPage());
        // Cada tarjeta lleva el listado de origen para que la ficha pueda volver a el
        // con la misma busqueda, filtros y pagina.
        final String listingQuery = request.getQueryString();
        mav.addObject("returnQuery", listingQuery == null ? null
                : URLEncoder.encode(listingQuery, StandardCharsets.UTF_8));
        return mav;
    }

    @ExceptionHandler(InvalidSearchQueryException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView invalidSearchQuery() {
        return new ModelAndView("error/400");
    }
}
```
