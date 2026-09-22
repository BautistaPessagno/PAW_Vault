---
title: "ProfileController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java"]
---

# ProfileController

Authenticated /profile. GET fills the username form from the principal and renders account data plus the owner's posts paged by twelve. POST validates and updates the username, replaces the session principal and redirects with a flash. POST /profile/password changes the password: a wrong current or unchanged password becomes a field error, and success logs out this session and redirects to /login?passwordChanged. Validation errors reopen the edited row at the same listing page.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ChangePasswordForm]], [[InvalidCurrentPasswordException]], [[PageNotFoundException]], [[PostService]], [[ProfileForm]], [[UnchangedPasswordException]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java, lines 1–129](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.services.InvalidCurrentPasswordException;
import ar.edu.itba.paw.services.PageNotFoundException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.UnchangedPasswordException;
import ar.edu.itba.paw.services.UserNotFoundException;
import ar.edu.itba.paw.services.UserService;
import ar.edu.itba.paw.webapp.form.ChangePasswordForm;
import ar.edu.itba.paw.webapp.form.ProfileForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import java.util.Locale;

@Controller
@RequestMapping("/profile")
public class ProfileController {

    private static final SecurityContextLogoutHandler LOGOUT_HANDLER = new SecurityContextLogoutHandler();

    private final UserService userService;
    private final PostService postService;

    @Autowired
    public ProfileController(final UserService userService, final PostService postService) {
        this.userService = userService;
        this.postService = postService;
    }

    @RequestMapping(method = RequestMethod.GET)
    public ModelAndView profile(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                @ModelAttribute("profileForm") final ProfileForm form,
                                @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                                @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        form.setUsername(currentUser.getDisplayName());
        return profileView(currentUser.getId(), OpenSection.NONE, pageNumber);
    }

    @RequestMapping(method = RequestMethod.POST)
    public ModelAndView update(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                               @Valid @ModelAttribute("profileForm") final ProfileForm form,
                               final BindingResult bindingResult,
                               @ModelAttribute("changePasswordForm") final ChangePasswordForm changePasswordForm,
                               final RedirectAttributes redirectAttributes,
                               @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.USERNAME, pageNumber);
        }

        final User updatedUser = userService.updateUsername(currentUser.getId(), form.getUsername());
        refreshAuthentication(updatedUser);
        redirectAttributes.addFlashAttribute("profileUpdated", true);
        return new ModelAndView("redirect:/profile");
    }

    @RequestMapping(value = "/password", method = RequestMethod.POST)
    public ModelAndView changePassword(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                       @Valid @ModelAttribute("changePasswordForm") final ChangePasswordForm form,
                                       final BindingResult bindingResult,
                                       @ModelAttribute("profileForm") final ProfileForm profileForm,
                                       final HttpServletRequest request, final HttpServletResponse response,
                                       final Locale locale,
                                       @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        profileForm.setUsername(currentUser.getDisplayName());
        if (bindingResult.hasErrors()) {
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber);
        }
        try {
            userService.changePassword(currentUser.getId(), form.getCurrentPassword(),
                    form.getPassword(), locale);
        } catch (final InvalidCurrentPasswordException e) {
            bindingResult.rejectValue("currentPassword", "profile.password.current.invalid");
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber);
        } catch (final UnchangedPasswordException e) {
            bindingResult.rejectValue("password", "profile.password.unchanged");
            return profileView(currentUser.getId(), OpenSection.PASSWORD, pageNumber);
        }
        LOGOUT_HANDLER.logout(request, response, SecurityContextHolder.getContext().getAuthentication());
        return new ModelAndView("redirect:/login?passwordChanged");
    }

    private ModelAndView profileView(final long userId, final OpenSection openSection, final int pageNumber) {
        final User user = userService.findById(userId).orElseThrow(UserNotFoundException::new);
        final ModelAndView modelAndView = new ModelAndView("profile/index");
        modelAndView.addObject("profileUser", user);
        modelAndView.addObject("postPage", postService.findByPublisherId(userId, pageNumber));
        modelAndView.addObject("profileEditOpen", openSection == OpenSection.USERNAME);
        modelAndView.addObject("passwordEditOpen", openSection == OpenSection.PASSWORD);
        return modelAndView;
    }

    private static void refreshAuthentication(final User updatedUser) {
        final Authentication current = SecurityContextHolder.getContext().getAuthentication();
        final AuthenticatedUser principal = new AuthenticatedUser(updatedUser);
        final UsernamePasswordAuthenticationToken refreshed = new UsernamePasswordAuthenticationToken(
                principal, null, principal.getAuthorities());
        refreshed.setDetails(current.getDetails());
        SecurityContextHolder.getContext().setAuthentication(refreshed);
    }

    private enum OpenSection { NONE, USERNAME, PASSWORD }

    @ExceptionHandler({UserNotFoundException.class, PageNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
