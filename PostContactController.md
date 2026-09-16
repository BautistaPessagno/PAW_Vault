---
title: "PostContactController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java"]
---

# PostContactController

Authenticated GET loads a contactable post; POST submits the principal ID, display name/email and optional message through InquiryService. Normalizes CRLF to LF and trims before size validation. Success redirects home with contactSent; missing/sold/self-owned posts produce 404/409/403.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ContactForm]], [[ForbiddenOperationException]], [[InquiryService]], [[PostNotFoundException]], [[PostSummary]], [[PostUnavailableException]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java, lines 1–105](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.PostUnavailableException;
import ar.edu.itba.paw.webapp.form.ContactForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
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
import java.beans.PropertyEditorSupport;

@Controller
public class PostContactController {

    private final InquiryService inquiryService;

    @Autowired
    public PostContactController(final InquiryService inquiryService) {
        this.inquiryService = inquiryService;
    }

    // Recorta antes de validar, para que @Size mida el valor real y no los espacios de mas.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
        binder.registerCustomEditor(String.class, "contactMessage", new LineBreakNormalizingEditor());
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.GET)
    public ModelAndView contactForm(@PathVariable("postId") final long postId,
                                    @ModelAttribute("contactForm") final ContactForm form,
                                    @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final PostSummary post = inquiryService.findContactablePost(postId, currentUser.getId());
        final ModelAndView modelAndView = new ModelAndView("post/contact");
        modelAndView.addObject("post", post);
        return modelAndView;
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.POST)
    public ModelAndView contact(@PathVariable("postId") final long postId,
                                @Valid @ModelAttribute("contactForm") final ContactForm form,
                                final BindingResult errors,
                                @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                final RedirectAttributes redirectAttributes) {
        if (errors.hasErrors()) {
            return contactForm(postId, form, currentUser);
        }
        inquiryService.submit(postId, currentUser.getId(), currentUser.getDisplayName(),
                currentUser.getEmail(), form.getContactMessage());

        redirectAttributes.addFlashAttribute("contactSent", true);
        return new ModelAndView("redirect:/");
    }

    @ExceptionHandler(PostNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView postNotFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    @ExceptionHandler(PostUnavailableException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView postUnavailable() {
        return new ModelAndView("error/409");
    }

    /*
     * El browser mide el maxlength del textarea contando los saltos como LF, pero manda el
     * contenido con CRLF: sin normalizar, un mensaje que la UI dio por bueno llega con un
     * caracter de mas por salto de linea y @Size lo rechaza. Tambien recorta, porque el editor
     * por campo reemplaza al StringTrimmerEditor registrado para todos los String.
     */
    private static final class LineBreakNormalizingEditor extends PropertyEditorSupport {

        @Override
        public void setAsText(final String text) {
            final String normalized = text == null ? "" : text.replace("\r\n", "\n").trim();
            setValue(normalized.isEmpty() ? null : normalized);
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
