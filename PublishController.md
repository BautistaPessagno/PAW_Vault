---
title: "PublishController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java"]
---

# PublishController

GET /publish returns the form. POST validates the five ordinary fields, then reads optional MultipartFile content type and bytes and invokes PostService.publish with Locale. InvalidImageException maps to cover; duplicate/concurrent exceptions map to publisherEmail. Success redirects to /. MaxUploadSizeExceededException returns a new empty PublishForm with coverTooLarge=true. IOException from getBytes is declared and has no dedicated recovery branch. See [[Publish flow]].

## Connections

Project types referenced: [[ConcurrentPublishException]], [[DuplicatePostException]], [[InvalidImageException]], [[PostService]], [[PublishForm]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, lines 1–74](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ConcurrentPublishException;
import ar.edu.itba.paw.services.DuplicatePostException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.webapp.form.PublishForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.multipart.MaxUploadSizeExceededException;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.ModelAndView;

import javax.validation.Valid;
import java.io.IOException;
import java.util.Locale;

@Controller
public class PublishController {

    private final PostService postService;

    @Autowired
    public PublishController(final PostService postService) {
        this.postService = postService;
    }

    @RequestMapping(value = "/publish", method = RequestMethod.GET)
    public ModelAndView publishForm(@ModelAttribute("publishForm") final PublishForm form) {
        return new ModelAndView("publish/index");
    }

    @RequestMapping(value = "/publish", method = RequestMethod.POST)
    public ModelAndView publish(@Valid @ModelAttribute("publishForm") final PublishForm form,
                                final BindingResult bindingResult, final Locale locale) throws IOException {
        if (bindingResult.hasErrors()) {
            return publishForm(form);
        }

        final MultipartFile cover = form.getCover();
        final boolean hasCover = cover != null && !cover.isEmpty();
        try {
            postService.publish(form.getUsername(), form.getPublisherEmail(), form.getTitle(),
                    form.getArtistName(), form.getReleaseYear(),
                    hasCover ? cover.getContentType() : null,
                    hasCover ? cover.getBytes() : null,
                    locale);
            return new ModelAndView("redirect:/");
        } catch (final InvalidImageException e) {
            bindingResult.rejectValue("cover", "publish.cover.invalid");
            return publishForm(form);
        } catch (final DuplicatePostException e) {
            bindingResult.rejectValue("publisherEmail", "publish.duplicate");
            return publishForm(form);
        } catch (final ConcurrentPublishException e) {
            bindingResult.rejectValue("publisherEmail", "publish.concurrent");
            return publishForm(form);
        }
    }

    // El resolver corta el request antes del binding, asi que el form llega vacio.
    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ModelAndView coverTooLarge() {
        final ModelAndView modelAndView = new ModelAndView("publish/index");
        modelAndView.addObject("publishForm", new PublishForm());
        modelAndView.addObject("coverTooLarge", true);
        return modelAndView;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
