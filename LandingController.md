---
title: "LandingController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java"]
---

# LandingController

Public GET / binds q, sort, genre, condition, artistId, year, minPrice, maxPrice and page. Custom editors turn malformed enum/numeric filters into null. It calls the paged search and renders filters, results and the [[PostPage]]; the artist list is no longer loaded, so artistId only arrives through URLs. A too-long query returns 400 and an out-of-range page 404. The model retains parsed filters even when service normalization ignores them.

## Connections

Project types referenced: [[Condition]], [[Genre]], [[InvalidSearchQueryException]], [[PageNotFoundException]], [[PostSearchCriteria]], [[PostService]], [[PostSort]], [[SearchResult]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java, lines 1–113](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.services.InvalidSearchQueryException;
import ar.edu.itba.paw.services.PageNotFoundException;
import ar.edu.itba.paw.services.PostService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;

import java.beans.PropertyEditorSupport;
import java.util.Locale;
import java.util.function.Function;

@Controller
public class LandingController {

    private final PostService postService;

    @Autowired
    public LandingController(final PostService postService) {
        this.postService = postService;
    }

    // Sin estos editores Spring corta con un 400 cuando no puede convertir un parametro.
    // Un orden o un filtro que no se entiende no merece un error: llega al service como
    // null y el catalogo se explora como si no se hubiera pedido.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(PostSort.class, new IgnoreInvalidEditor(text -> PostSort.valueOf(upperCase(text))));
        binder.registerCustomEditor(Genre.class, new IgnoreInvalidEditor(text -> Genre.valueOf(upperCase(text))));
        binder.registerCustomEditor(Condition.class, new IgnoreInvalidEditor(text -> Condition.valueOf(upperCase(text))));
        binder.registerCustomEditor(Long.class, new IgnoreInvalidEditor(Long::valueOf));
        binder.registerCustomEditor(Integer.class, new IgnoreInvalidEditor(Integer::valueOf));
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
    public ModelAndView landing(@RequestParam(value = "q", required = false) final String query,
                                @RequestParam(value = "sort", required = false) final PostSort sort,
                                @RequestParam(value = "genre", required = false) final Genre genre,
                                @RequestParam(value = "condition", required = false) final Condition condition,
                                @RequestParam(value = "artistId", required = false) final Long artistId,
                                @RequestParam(value = "year", required = false) final Integer releaseYear,
                                @RequestParam(value = "minPrice", required = false) final Integer minPrice,
                                @RequestParam(value = "maxPrice", required = false) final Integer maxPrice,
                                @RequestParam(value = "page", defaultValue = "1") final int pageNumber) {
        final SearchResult result = postService.search(new PostSearchCriteria(query, sort, genre, condition,
                artistId, releaseYear, minPrice, maxPrice), pageNumber);
        final ModelAndView mav = new ModelAndView("landing/index");
        mav.addObject("query", result.getQuery());
        mav.addObject("sort", sort == null ? PostSort.NEWEST : sort);
        mav.addObject("sorts", PostSort.values());
        mav.addObject("genres", Genre.values());
        mav.addObject("conditions", Condition.values());
        mav.addObject("selectedGenre", genre);
        mav.addObject("selectedCondition", condition);
        mav.addObject("selectedArtistId", artistId);
        mav.addObject("selectedYear", releaseYear);
        mav.addObject("minPrice", minPrice);
        mav.addObject("maxPrice", maxPrice);
        mav.addObject("posts", result.getPage().getPosts());
        mav.addObject("postPage", result.getPage());
        return mav;
    }

    @ExceptionHandler(InvalidSearchQueryException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView invalidSearchQuery() {
        return new ModelAndView("error/400");
    }

    @ExceptionHandler(PageNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView pageNotFound() {
        return new ModelAndView("error/404");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
