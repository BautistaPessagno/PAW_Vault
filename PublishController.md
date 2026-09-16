---
title: "PublishController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java"]
---

# PublishController

Authenticated publish uses the principal ID, validated PublishForm and optional multipart image. Re-populates Genre/Condition options when rendering errors. Invalid image, duplicate post and concurrent publication errors remain on the form; success redirects home. Oversize transport errors arrive through the dedicated filter redirect.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[Genre]], [[InvalidImageException]], [[PostService]], [[PublishForm]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, lines 1–81](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.services.ConcurrentPublishException;
import ar.edu.itba.paw.services.DuplicatePostException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.webapp.form.PublishForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.ModelAndView;

import javax.validation.Valid;
import java.io.IOException;

@Controller
public class PublishController {

    private final PostService postService;

    @Autowired
    public PublishController(final PostService postService) {
        this.postService = postService;
    }

    @RequestMapping(value = "/publish", method = RequestMethod.GET)
    public ModelAndView publishForm(@ModelAttribute("publishForm") final PublishForm form,
                                    @RequestParam(name = "coverTooLarge", required = false)
                                    final String coverTooLarge) {
        final ModelAndView modelAndView = publishView();
        modelAndView.addObject("coverTooLarge", coverTooLarge != null);
        return modelAndView;
    }

    // Las listas de los <select> van en la vista y no como @ModelAttribute de la clase:
    // el redirect post-publicacion arrastraria el modelo entero como query string.
    private static ModelAndView publishView() {
        final ModelAndView modelAndView = new ModelAndView("publish/index");
        modelAndView.addObject("genres", Genre.values());
        modelAndView.addObject("conditions", Condition.values());
        return modelAndView;
    }

    @RequestMapping(value = "/publish", method = RequestMethod.POST)
    public ModelAndView publish(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                @Valid @ModelAttribute("publishForm") final PublishForm form,
                                final BindingResult bindingResult) throws IOException {
        if (bindingResult.hasErrors()) {
            return publishForm(form, null);
        }

        final MultipartFile cover = form.getCover();
        final boolean hasCover = cover != null && !cover.isEmpty();
        try {
            postService.publish(currentUser.getId(), form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(),
                    form.getDescription(), form.getCondition(), form.getPressingYear(), form.getZone(),
                    hasCover ? cover.getContentType() : null,
                    hasCover ? cover.getBytes() : null);
            return new ModelAndView("redirect:/");
        } catch (final InvalidImageException e) {
            bindingResult.rejectValue("cover", "publish.cover.invalid");
            return publishForm(form, null);
        } catch (final DuplicatePostException e) {
            bindingResult.reject("publish.duplicate");
            return publishForm(form, null);
        } catch (final ConcurrentPublishException e) {
            bindingResult.reject("publish.concurrent");
            return publishForm(form, null);
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
