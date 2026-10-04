---
title: "AuthenticationController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java"]
---

# AuthenticationController

Login (solo la vista), registro con inicio de sesión automático, verificación por enlace, página de aviso, reenvío con espera y recuperación de contraseña en dos pasos. Ver [[Authentication flow]] y [[Password recovery flow]].

## Guía de lectura

Datos y dependencias declaradas: `userService`, `sessionRegistry`.

Operaciones para localizar en la fuente: `initRegisterBinder`, `initForgotPasswordBinder`, `login`, `registerForm`, `register`, `verifyEmail`, `verificationRequired`, `resendVerification`, `forgotPasswordForm`, `forgotPassword`, `resetPasswordForm`, `resetPassword`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[AuthenticationSessions]], [[DuplicateUserException]], [[ForgotPasswordForm]], [[LoginForm]], [[RegisterForm]], [[ResetPasswordForm]], [[SameSiteRedirects]], [[UnchangedPasswordException]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>), líneas 1–172.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.DuplicateUserException;
import ar.edu.itba.paw.services.UnchangedPasswordException;
import ar.edu.itba.paw.services.UserNotFoundException;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.form.ForgotPasswordForm;
import ar.edu.itba.paw.webapp.form.LoginForm;
import ar.edu.itba.paw.webapp.form.RegisterForm;
import ar.edu.itba.paw.webapp.form.ResetPasswordForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import ar.edu.itba.paw.webapp.security.AuthenticationSessions;
import ar.edu.itba.paw.webapp.security.SameSiteRedirects;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import java.util.Locale;
import java.util.Optional;

@Controller
public class AuthenticationController {

    private final UserService userService;
    private final SessionRegistry sessionRegistry;

    @Autowired
    public AuthenticationController(final UserService userService, final SessionRegistry sessionRegistry) {
        this.userService = userService;
        this.sessionRegistry = sessionRegistry;
    }

    @InitBinder("registerForm")
    public void initRegisterBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, "email", new StringTrimmerEditor(false));
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
                                 final BindingResult bindingResult, final Locale locale,
                                 final HttpServletRequest request, final HttpServletResponse response) {
        if (bindingResult.hasErrors()) {
            return registerForm(form);
        }

        final User user;
        try {
            user = userService.register(form.getEmail(), form.getUsername(), form.getPassword(), locale);
        } catch (final DuplicateUserException e) {
            bindingResult.rejectValue("email", "auth.register.email.duplicate");
            // Si el correo es suyo, lo que le sirve es recuperar la cuenta y no crear otra.
            return registerForm(form).addObject("duplicateEmail", true);
        }
        AuthenticationSessions.login(user, request, response, sessionRegistry);
        return new ModelAndView("redirect:/");
    }

    /*
     * Abrir el enlace verifica la cuenta pero no inicia sesion: quien vea un correo reenviado
     * no entra a la cuenta ajena. Si el navegador ya tiene la sesion de esa cuenta, el
     * principal se reemplaza para que pueda publicar sin volver a iniciar sesion.
     */
    @RequestMapping(value = "/verify", method = RequestMethod.GET)
    public ModelAndView verifyEmail(@RequestParam(name = "token", required = false) final String token,
                                    final Locale locale) {
        final Optional<User> verified = userService.verifyEmail(token, locale);
        verified.ifPresent(AuthenticationSessions::refreshIfCurrent);
        return new ModelAndView("auth/verify", "verified", verified.isPresent());
    }

    @RequestMapping(value = "/verify/required", method = RequestMethod.GET)
    public ModelAndView verificationRequired(@AuthenticationPrincipal final AuthenticatedUser currentUser) {
        // La cuenta pudo verificarse en otro navegador: se refresca la sesion antes de mostrar el aviso.
        final User user = userService.findById(currentUser.getId()).orElseThrow(UserNotFoundException::new);
        if (user.isVerified()) {
            AuthenticationSessions.refreshIfCurrent(user);
            return new ModelAndView("redirect:/");
        }
        return new ModelAndView("auth/verify-required");
    }

    @RequestMapping(value = "/verify/resend", method = RequestMethod.POST)
    public ModelAndView resendVerification(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                           @RequestHeader(name = "Referer", required = false) final String referer,
                                           final HttpServletRequest request, final Locale locale,
                                           final RedirectAttributes redirectAttributes) {
        // Si el ultimo enlace es muy reciente no se manda otro: se avisa que espere.
        redirectAttributes.addFlashAttribute(userService.resendVerification(currentUser.getId(), locale)
                ? "verificationResent" : "verificationThrottled", true);
        return new ModelAndView("redirect:" + SameSiteRedirects.pathOf(referer, request));
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
                                      final BindingResult bindingResult, final Locale locale,
                                      final HttpServletRequest request, final HttpServletResponse response) {
        if (bindingResult.hasErrors()) {
            return new ModelAndView("auth/reset-password");
        }
        try {
            final Optional<User> reset = userService.resetPassword(form.getToken(), form.getPassword(), locale);
            if (reset.isPresent()) {
                AuthenticationSessions.logoutEverywhere(reset.get(), request, response, sessionRegistry);
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
