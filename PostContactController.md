---
title: "PostContactController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java"]
---

# PostContactController

GET /post/{id}/contact loads PostSummary. POST trims strings before validation; invalid fields redisplay the same form and reload the post. Valid input calls notifyInterest with the request Locale, sets contactSent=true and redirects to /. Missing posts map to 404. The synchronous mail-failure catch, 503 response and deliveryFailed model flag were removed. See [[Contact flow]].

## Connections

Project types referenced: [[ContactForm]], [[PostNotFoundException]], [[PostService]], [[PostSummary]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java, lines 1–73](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.PostService;
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

import javax.validation.Valid;
import java.util.Locale;

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
                                final Locale locale) {
        if (bindingResult.hasErrors()) {
            return contactForm(postId, form);
        }

        // El locale se resuelve aca, en el hilo del request, porque el envio es @Async
        // y del otro lado ya no hay request del que sacarlo.
        postService.notifyInterest(postId, form.getContactName(), form.getContactEmail(), locale);

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

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
