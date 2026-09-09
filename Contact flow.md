---
title: "Contact flow"
categories: ["Flows"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "flows"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# Contact flow

A visitor opens /post/{id}/contact from a publication card. [[PostContactController]] loads [[PostSummary]], renders a compact card and validates the visitor’s name/email. The destination address comes from the Post’s publisher, never from visitor input.

```mermaid
sequenceDiagram
    participant B as Browser
    participant C as PostContactController
    participant S as PostServiceImpl
    participant E as EmailService async proxy
    participant W as Mail worker
    B->>C: POST name and email
    C->>C: Trim and validate; resolve Locale
    C->>S: notifyInterest(id, name, email, locale)
    S->>S: Reload Post and normalize contact email
    S->>E: sendPostInterestEmail(notification, locale)
    E-->>S: Task submitted
    C-->>B: Redirect / with contactSent
    E->>W: Render localized email and send
    W->>W: Log success or catch/log failure
```

Invalid fields redisplay the form with retained text; the Post is reloaded. A missing Post maps to 404. The service has no encompassing transaction; it reads the summary and builds [[PostInterestNotification]]. It trims the contact name and trims/lowercases contact email, then passes the request Locale to [[EmailService]].

The contact mail is now @Async, uses the caller’s Locale and includes a home link from app.base-url. Rendering or SMTP failures inside the mail method are logged and swallowed. The previous [[EmailDeliveryException]], deliveryFailed flag, 503 retry branch and view message were removed.

contactSent means the normal notification call returned, not that mail reached the publisher. The visible success copy still says the publisher was notified. There is no durable queue, contact record, automatic retry or delivery status. Under executor saturation, CallerRunsPolicy can run the mail work on the request thread, delaying the redirect. The diagram shows the normal available-capacity path.

## Controller source

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

[[Mail delivery]] · [[Validation and errors]] · [[EmailServiceImplTest]]
