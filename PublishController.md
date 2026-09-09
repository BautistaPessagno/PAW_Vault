---
title: "PublishController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java"]
---

# PublishController

GET `/publish` exposes a [[PublishForm]] named `publishForm`. POST binds and validates the same form, returning the JSP immediately when BindingResult has errors. Otherwise it calls [[PostService]].publish with all five fields and the request Locale. Success redirects to `/`. Duplicate and concurrent exceptions add localized field errors to `publisherEmail`, then reuse the form view. There is no automatic retry. See [[Publish flow]].

## Connections

Project types referenced: [[ConcurrentPublishException]], [[DuplicatePostException]], [[PostService]], [[PublishForm]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, lines 1–52](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ConcurrentPublishException;
import ar.edu.itba.paw.services.DuplicatePostException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.webapp.form.PublishForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import javax.validation.Valid;
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
                                final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return publishForm(form);
        }

        try {
            postService.publish(form.getUsername(), form.getPublisherEmail(), form.getTitle(),
                    form.getArtistName(), form.getReleaseYear(), locale);
            return new ModelAndView("redirect:/");
        } catch (final DuplicatePostException e) {
            bindingResult.rejectValue("publisherEmail", "publish.duplicate");
            return publishForm(form);
        } catch (final ConcurrentPublishException e) {
            bindingResult.rejectValue("publisherEmail", "publish.concurrent");
            return publishForm(form);
        }
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
