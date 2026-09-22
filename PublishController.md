---
title: "PublishController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java"]
---

# PublishController

Authenticated publishing and editing share the publish/index view. POST /publish creates the post and redirects to /post/{id} with postCreated. GET and POST /post/{id}/edit load the owner's AVAILABLE post, prefill the form and show the existing cover; success redirects with postUpdated. POST /post/{id}/delete removes the post and redirects to /profile#posts. Image, duplicate and concurrent errors stay on the form; missing, foreign and sold posts map to 404, 403 and 409.

## Connections

Project types referenced: [[AuthenticatedUser]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[ForbiddenOperationException]], [[Genre]], [[InvalidImageException]], [[Post]], [[PostNotFoundException]], [[PostService]], [[PostSummary]], [[PostUnavailableException]], [[PublishForm]].

Referenced by: none.

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, lines 1–189](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>)

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.services.ConcurrentPublishException;
import ar.edu.itba.paw.services.DuplicatePostException;
import ar.edu.itba.paw.services.ForbiddenOperationException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.PostNotFoundException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.PostUnavailableException;
import ar.edu.itba.paw.webapp.form.PublishForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

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
        final ModelAndView modelAndView = publishView(false, null);
        modelAndView.addObject("coverTooLarge", coverTooLarge != null);
        return modelAndView;
    }

    // Las listas de los <select> van en la vista y no como @ModelAttribute de la clase:
    // el redirect post-publicacion arrastraria el modelo entero como query string.
    private ModelAndView publishView(final boolean editing, final Long postId) {
        final ModelAndView modelAndView = new ModelAndView("publish/index");
        modelAndView.addObject("genres", Genre.values());
        modelAndView.addObject("conditions", Condition.values());
        modelAndView.addObject("editing", editing);
        modelAndView.addObject("postId", postId);
        modelAndView.addObject("formAction", editing ? "/post/" + postId + "/edit" : "/publish");
        modelAndView.addObject("cancelHref", editing ? "/post/" + postId : "/");
        return modelAndView;
    }

    @RequestMapping(value = "/publish", method = RequestMethod.POST)
    public ModelAndView publish(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                @Valid @ModelAttribute("publishForm") final PublishForm form,
                                final BindingResult bindingResult,
                                final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return publishForm(form, null);
        }

        final MultipartFile cover = form.getCover();
        final String coverContentType = cover == null ? null : cover.getContentType();
        final byte[] coverData = cover == null ? null : cover.getBytes();
        try {
            final Post post = postService.publish(currentUser.getId(), form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(),
                    form.getDescription(), form.getCondition(), form.getPressingYear(), form.getZone(),
                    coverContentType, coverData);
            redirectAttributes.addFlashAttribute("postCreated", true);
            return new ModelAndView("redirect:/post/" + post.getId());
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

    @RequestMapping(value = "/post/{postId:[0-9]+}/edit", method = RequestMethod.GET)
    public ModelAndView editForm(@PathVariable("postId") final long postId,
                                 @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                 @ModelAttribute("publishForm") final PublishForm form,
                                 @RequestParam(name = "coverTooLarge", required = false)
                                 final String coverTooLarge) {
        final PostSummary post = postService.findEditableById(postId, currentUser.getId());
        populate(form, post);
        final ModelAndView modelAndView = editView(postId, post);
        modelAndView.addObject("coverTooLarge", coverTooLarge != null);
        return modelAndView;
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/edit", method = RequestMethod.POST)
    public ModelAndView edit(@PathVariable("postId") final long postId,
                             @AuthenticationPrincipal final AuthenticatedUser currentUser,
                             @Valid @ModelAttribute("publishForm") final PublishForm form,
                             final BindingResult bindingResult,
                             final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return editView(postId, currentUser.getId());
        }

        final MultipartFile cover = form.getCover();
        final String coverContentType = cover == null ? null : cover.getContentType();
        final byte[] coverData = cover == null ? null : cover.getBytes();
        try {
            postService.update(postId, currentUser.getId(), form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(), form.getDescription(),
                    form.getCondition(), form.getPressingYear(), form.getZone(),
                    coverContentType, coverData);
            redirectAttributes.addFlashAttribute("postUpdated", true);
            return new ModelAndView("redirect:/post/" + postId);
        } catch (final InvalidImageException e) {
            bindingResult.rejectValue("cover", "publish.cover.invalid");
        } catch (final DuplicatePostException e) {
            bindingResult.reject("publish.duplicate");
        } catch (final ConcurrentPublishException e) {
            bindingResult.reject("publish.concurrent");
        }
        return editView(postId, currentUser.getId());
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/delete", method = RequestMethod.POST)
    public ModelAndView delete(@PathVariable("postId") final long postId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        postService.delete(postId, currentUser.getId());
        redirectAttributes.addFlashAttribute("postDeleted", true);
        return new ModelAndView("redirect:/profile#posts");
    }

    private ModelAndView editView(final long postId, final long publisherId) {
        return editView(postId, postService.findEditableById(postId, publisherId));
    }

    private ModelAndView editView(final long postId, final PostSummary post) {
        final ModelAndView modelAndView = publishView(true, postId);
        modelAndView.addObject("existingCoverImageId", post.getCoverImageId());
        return modelAndView;
    }

    private static void populate(final PublishForm form, final PostSummary post) {
        form.setTitle(post.getTitle());
        form.setArtistName(post.getArtistName());
        form.setReleaseYear(post.getReleaseYear());
        form.setGenre(post.getGenre());
        form.setPrice(post.getPrice());
        form.setCondition(post.getCondition());
        form.setZone(post.getZone());
        form.setPressingYear(post.getPressingYear());
        form.setDescription(post.getDescription());
    }

    @ExceptionHandler(PostNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    @ExceptionHandler(PostUnavailableException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView unavailable() {
        return new ModelAndView("error/409");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
