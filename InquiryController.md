---
title: "InquiryController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java"]
---

# InquiryController

Authenticated GET /inquiries loads sent and received lists for the principal ID. POST /inquiries/{id}/accept or /reject delegates owner checks to the service, sets a flash and redirects to the inbox. Missing rows map to 404, wrong owner to 403 and closed-state conflicts to 409.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ForbiddenOperationException]], [[InquiryNotFoundException]], [[InquiryService]], [[InvalidInquiryStateException]], [[PostNotFoundException]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java, lines 1–77](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InquiryNotFoundException;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.InvalidInquiryStateException;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

// La bandeja es de cualquier usuario autenticado: la pertenencia de la publicacion que se
// acepta o se rechaza la verifica el service.
@Controller
@RequestMapping("/inquiries")
public class InquiryController {

    private final InquiryService inquiryService;

    @Autowired
    public InquiryController(final InquiryService inquiryService) {
        this.inquiryService = inquiryService;
    }

    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView list(@AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final ModelAndView modelAndView = new ModelAndView("inquiry/index");
        modelAndView.addObject("sentInquiries", inquiryService.findSentBy(currentUser.getId()));
        modelAndView.addObject("receivedInquiries", inquiryService.findReceivedBy(currentUser.getId()));
        return modelAndView;
    }

    @RequestMapping(value = "/{inquiryId:[0-9]+}/accept", method = RequestMethod.POST)
    public ModelAndView accept(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        inquiryService.accept(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("inquiryAccepted", true);
        return new ModelAndView("redirect:/inquiries");
    }

    @RequestMapping(value = "/{inquiryId:[0-9]+}/reject", method = RequestMethod.POST)
    public ModelAndView reject(@PathVariable("inquiryId") final long inquiryId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        inquiryService.reject(inquiryId, currentUser.getId());
        redirectAttributes.addFlashAttribute("inquiryRejected", true);
        return new ModelAndView("redirect:/inquiries");
    }

    @ExceptionHandler({InquiryNotFoundException.class, PostNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    @ExceptionHandler(InvalidInquiryStateException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView invalidState() {
        return new ModelAndView("error/409");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
