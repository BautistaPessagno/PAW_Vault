---
title: "PostContactController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java"]
---

# PostContactController

`initBinder` trims all bound strings and turns empty strings into null before validation. GET `/post/{postId:[0-9]+}/contact` loads a summary and the `contactForm`. POST returns that view on invalid input, otherwise calls notifyInterest. [[EmailDeliveryException]] sets status 503 and adds `deliveryFailed`; success adds a one-request `contactSent` flash attribute and redirects to `/`. The local exception handler turns [[PostNotFoundException]] into 404. The numeric route regex rejects non-digits before the handler. See [[Contact flow]].

## Connections

Project types referenced: [[ContactForm]], [[EmailDeliveryException]], [[PostNotFoundException]], [[PostService]], [[PostSummary]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java, lines 1–77](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.exceptions.EmailDeliveryException;
import ar.edu.itba.paw.webapp.form.ContactForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;

@Controller
public class PostContactController {

    private final PostService postService;

    @Autowired
    public PostContactController(final PostService postService) {
        this.postService = postService;
    }

    // Recorta antes de validar, para que @Size mida el valor real y no los espacios de mas.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.GET)
    public ModelAndView contactForm(@PathVariable final long postId,
                                    @ModelAttribute("contactForm") final ContactForm form) {
        final PostSummary post = postService.findById(postId).orElseThrow(PostNotFoundException::new);
        final ModelAndView modelAndView = new ModelAndView("post/contact");
        modelAndView.addObject("post", post);
        return modelAndView;
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.POST)
    public ModelAndView contact(@PathVariable final long postId,
                                @Valid @ModelAttribute("contactForm") final ContactForm form,
                                final BindingResult bindingResult,
                                final RedirectAttributes redirectAttributes,
                                final HttpServletResponse response) {
        if (bindingResult.hasErrors()) {
            return contactForm(postId, form);
        }

        try {
            postService.notifyInterest(postId, form.getContactName(), form.getContactEmail());
        } catch (final EmailDeliveryException e) {
            response.setStatus(HttpServletResponse.SC_SERVICE_UNAVAILABLE);
            return contactForm(postId, form).addObject("deliveryFailed", true);
        }

        redirectAttributes.addFlashAttribute("contactSent", true);
        return new ModelAndView("redirect:/");
    }

    @ExceptionHandler(PostNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public void postNotFound() {
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
