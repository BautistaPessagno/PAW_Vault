---
title: "HelloWorldController"
categories: ["History"]
type: "historical-code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
source_commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
tags: ["codemap", "web"]
sources: []
---

# HelloWorldController

> [!note] Historical source
> This type is absent at ff96f27. The text and excerpt below describe the previous implementation at 041ce34.

Legacy scaffold routes. GET `/create` binds [[UserForm]] as `form`; POST validates then invokes [[UserService]].create with Locale and redirects to `/profile/{id}`. GET `/profile/{userId}` resolves Optional to a User, then renders `helloworld/index`. Missing users throw [[UserNotFoundException]], which has no explicit 404 mapping here. The landing does not link to these routes. See [[Legacy user flow]].

## Connections

Project types referenced: [[User]], [[UserForm]], [[UserNotFoundException]], [[UserService]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/HelloWorldController.java, lines 1–54](<https://bitbucket.org/itba/paw-2026b-14/src/041ce34404963b689d05443ca00abb7e75aa7f15/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/HelloWorldController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.exceptions.UserNotFoundException;
import ar.edu.itba.paw.webapp.form.UserForm;

import javax.validation.Valid;
import java.util.Locale;

@Controller
public class HelloWorldController {

    private final UserService us;

    @Autowired
    public HelloWorldController(UserService us) {
        this.us = us;
    }

    @RequestMapping(value = "/profile/{userId}", method = RequestMethod.GET)
    public ModelAndView profile(@PathVariable("userId") final long userId) {
        final User user = us.findById(userId).orElseThrow(UserNotFoundException::new);
        final ModelAndView mav = new ModelAndView("helloworld/index");
        mav.addObject("user", user);
        return mav;
    }

    @RequestMapping(value = "/create", method = RequestMethod.GET)
    public ModelAndView createForm(@ModelAttribute("form") final UserForm form) {
        return new ModelAndView("helloworld/create");
    }

    @RequestMapping(value = "/create", method = RequestMethod.POST)
    public ModelAndView create(@Valid @ModelAttribute("form") final UserForm form,
                               final BindingResult bindingResult,
                               final Locale locale) {
        if (bindingResult.hasErrors()) {
            return createForm(form);
        }

        final User user = us.create(form.getUsername(), form.getEmail(), locale);
        return new ModelAndView("redirect:/profile/" + user.getId());
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
