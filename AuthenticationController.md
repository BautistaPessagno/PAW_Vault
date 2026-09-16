---
title: "AuthenticationController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java"]
---

# AuthenticationController

GET /login renders the login form; Spring Security handles login POST. Registration takes only email and redirects to /login?verificationSent. GET /verify copies the token into a form without activating; validated POST chooses credentials and redirects to /login?verified or renders an error. Email/username are trimmed before validation.

## Connections

Project types referenced: [[DuplicateUserException]], [[LoginForm]], [[RegisterForm]], [[UserService]], [[VerifyEmailForm]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java, lines 1–88](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.DuplicateUserException;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.form.LoginForm;
import ar.edu.itba.paw.webapp.form.RegisterForm;
import ar.edu.itba.paw.webapp.form.VerifyEmailForm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import javax.validation.Valid;
import java.util.Locale;

@Controller
public class AuthenticationController {

    private final UserService userService;

    @Autowired
    public AuthenticationController(final UserService userService) {
        this.userService = userService;
    }

    @InitBinder("registerForm")
    public void initRegisterBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, "email", new StringTrimmerEditor(false));
    }

    @InitBinder("verifyEmailForm")
    public void initVerifyBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, "username", new StringTrimmerEditor(false));
    }

    @RequestMapping(value = "/login", method = RequestMethod.GET)
    public ModelAndView login(@ModelAttribute("loginForm") final LoginForm form) {
        return new ModelAndView("auth/login");
    }

    @RequestMapping(value = "/register", method = RequestMethod.GET)
    public ModelAndView registerForm(@ModelAttribute("registerForm") final RegisterForm form) {
        return new ModelAndView("auth/register");
    }

    @RequestMapping(value = "/register", method = RequestMethod.POST)
    public ModelAndView register(@Valid @ModelAttribute("registerForm") final RegisterForm form,
                                 final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return registerForm(form);
        }

        try {
            userService.register(form.getEmail(), locale);
            return new ModelAndView("redirect:/login?verificationSent");
        } catch (final DuplicateUserException e) {
            bindingResult.rejectValue("email", "auth.register.email.duplicate");
            return registerForm(form);
        }
    }

    @RequestMapping(value = "/verify", method = RequestMethod.GET)
    public ModelAndView verifyEmailForm(@RequestParam(name = "token", required = false) final String token,
                                        @ModelAttribute("verifyEmailForm") final VerifyEmailForm form) {
        form.setToken(token);
        return new ModelAndView("auth/verify");
    }

    @RequestMapping(value = "/verify", method = RequestMethod.POST)
    public ModelAndView verifyEmail(@Valid @ModelAttribute("verifyEmailForm") final VerifyEmailForm form,
                                    final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return new ModelAndView("auth/verify");
        }
        if (userService.verifyEmail(form.getToken(), form.getUsername(), form.getPassword(), locale).isPresent()) {
            return new ModelAndView("redirect:/login?verified");
        }
        bindingResult.reject("auth.verify.invalid");
        return new ModelAndView("auth/verify");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
