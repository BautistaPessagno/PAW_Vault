---
title: "InquiryController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java"]
---

# InquiryController

Authenticated GET /inquiries renders received inquiries and GET /inquiries/sent renders sent ones, each paged by publication with both totals for the sub-navigation. POST /inquiries/{id}/accept and /reject delegate owner checks to the service, set a flash and redirect to /inquiries. Missing inquiry, post or page maps to 404, a wrong owner to 403, and closed or deleted-post states to 409.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ForbiddenOperationException]], [[InquiryNotFoundException]], [[InquiryService]], [[InvalidInquiryStateException]], [[PageNotFoundException]], [[PostNotFoundException]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java, lines 1–94](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InquiryNotFoundException;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.InvalidInquiryStateException;
import ar.edu.itba.paw.services.PageNotFoundException;
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
import org.springframework.web.bind.annotation.RequestParam;
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

    // Cada vista trae su propia pagina, y los dos totales de la sub-nav salen del service.
    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView received(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                 @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final long userId = currentUser.getId();
        final ModelAndView modelAndView = new ModelAndView("inquiry/received");
        modelAndView.addObject("receivedPage", inquiryService.findReceivedGroupedByPost(userId, pageNumber));
        modelAndView.addObject("receivedCount", inquiryService.countReceivedBy(userId));
        modelAndView.addObject("sentCount", inquiryService.countSentBy(userId));
        return modelAndView;
    }

    @RequestMapping(value = "/sent", method = RequestMethod.GET)
    public ModelAndView sent(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                             @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final long userId = currentUser.getId();
        final ModelAndView modelAndView = new ModelAndView("inquiry/sent");
        modelAndView.addObject("sentPage", inquiryService.findSentGroupedByPost(userId, pageNumber));
        modelAndView.addObject("sentCount", inquiryService.countSentBy(userId));
        modelAndView.addObject("receivedCount", inquiryService.countReceivedBy(userId));
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

    @ExceptionHandler({InquiryNotFoundException.class, PostNotFoundException.class, PageNotFoundException.class})
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
