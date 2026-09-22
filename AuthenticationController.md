---
title: "AuthenticationController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java"]
---

# AuthenticationController

GET /login renders the form; Spring Security handles POST /login. Registration takes only an email and redirects to /login?verificationSent. /verify copies the token into a form and the validated POST activates the account. POST /forgot-password always redirects to /login?resetLinkSent after a valid address, so it does not reveal which accounts exist. /reset-password keeps the token in an escaped hidden field; success redirects to /login?passwordReset, a reused password becomes a field error and an invalid or expired link a global error. Binders trim email and username.

## Connections

Project types referenced: [[DuplicateUserException]], [[ForgotPasswordForm]], [[LoginForm]], [[RegisterForm]], [[ResetPasswordForm]], [[UnchangedPasswordException]], [[UserService]], [[VerifyEmailForm]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java, lines 1–141](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.DuplicateUserException;
import ar.edu.itba.paw.services.UnchangedPasswordException;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.form.ForgotPasswordForm;
import ar.edu.itba.paw.webapp.form.LoginForm;
import ar.edu.itba.paw.webapp.form.RegisterForm;
import ar.edu.itba.paw.webapp.form.ResetPasswordForm;
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

    @InitBinder("forgotPasswordForm")
    public void initForgotPasswordBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, "email", new StringTrimmerEditor(false));
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

    @RequestMapping(value = "/forgot-password", method = RequestMethod.GET)
    public ModelAndView forgotPasswordForm(@ModelAttribute("forgotPasswordForm") final ForgotPasswordForm form) {
        return new ModelAndView("auth/forgot-password");
    }

    /*
     * Redirige igual exista o no la cuenta: si respondiera distinto, el formulario serviria
     * para averiguar que correos estan registrados. Quien decide a quien escribirle es el service.
     */
    @RequestMapping(value = "/forgot-password", method = RequestMethod.POST)
    public ModelAndView forgotPassword(@Valid @ModelAttribute("forgotPasswordForm") final ForgotPasswordForm form,
                                       final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return forgotPasswordForm(form);
        }
        userService.requestPasswordReset(form.getEmail(), locale);
        return new ModelAndView("redirect:/login?resetLinkSent");
    }

    @RequestMapping(value = "/reset-password", method = RequestMethod.GET)
    public ModelAndView resetPasswordForm(@RequestParam(name = "token", required = false) final String token,
                                          @ModelAttribute("resetPasswordForm") final ResetPasswordForm form) {
        form.setToken(token);
        return new ModelAndView("auth/reset-password");
    }

    @RequestMapping(value = "/reset-password", method = RequestMethod.POST)
    public ModelAndView resetPassword(@Valid @ModelAttribute("resetPasswordForm") final ResetPasswordForm form,
                                      final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return new ModelAndView("auth/reset-password");
        }
        try {
            if (userService.resetPassword(form.getToken(), form.getPassword(), locale).isPresent()) {
                return new ModelAndView("redirect:/login?passwordReset");
            }
        } catch (final UnchangedPasswordException e) {
            // El enlace sigue vivo: el error va en el campo para que reintente con otra clave.
            bindingResult.rejectValue("password", "auth.resetPassword.unchanged");
            return new ModelAndView("auth/reset-password");
        }
        bindingResult.reject("auth.resetPassword.invalid");
        return new ModelAndView("auth/reset-password");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
