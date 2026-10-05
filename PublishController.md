---
title: "PublishController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java"]
---

# PublishController

Publicar, editar y eliminar. Editar y eliminar exigen ser el publicante o administrador con `@PreAuthorize`, y el service lo vuelve a chequear con el id de quien actúa junto con que el post siga disponible. Ver [[Publish flow]] y [[Edit and delete flow]].

## Guía de lectura

Datos y dependencias declaradas: `CAN_MODERATE_POST`, `postService`.

Operaciones para localizar en la fuente: `publishForm`, `publishView`, `publish`, `editForm`, `edit`, `delete`, `editView`, `populate`, `unavailable`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[Genre]], [[ImageRules]], [[InvalidImageException]], [[Post]], [[PostService]], [[PostSummary]], [[PostUnavailableException]], [[PublishForm]], [[VinylInputRules]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>), líneas 1–187.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.VinylInputRules;
import ar.edu.itba.paw.services.ConcurrentPublishException;
import ar.edu.itba.paw.services.DuplicatePostException;
import ar.edu.itba.paw.services.InvalidImageException;
import ar.edu.itba.paw.services.PostService;
import ar.edu.itba.paw.services.PostUnavailableException;
import ar.edu.itba.paw.webapp.form.PublishForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
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
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.validation.Valid;
import java.io.IOException;

@Controller
public class PublishController {

    // Editar y eliminar: el Publicante o un administrador. Que el post siga a la venta lo exige el service.
    private static final String CAN_MODERATE_POST =
            "hasRole('ADMIN') or @postAccess.isPublisher(authentication, #postId)";

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
        modelAndView.addObject("minimumYear", VinylInputRules.MIN_YEAR);
        modelAndView.addObject("currentYear", VinylInputRules.currentYear());
        modelAndView.addObject("minimumPrice", VinylInputRules.MIN_PRICE);
        modelAndView.addObject("maximumPrice", VinylInputRules.MAX_PRICE);
        modelAndView.addObject("acceptedImageTypes", ImageRules.ACCEPTED_CONTENT_TYPES);
        return modelAndView;
    }

    // Las fotos ya llegan validadas por PublishFormValidator.
    @RequestMapping(value = "/publish", method = RequestMethod.POST)
    public ModelAndView publish(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                                @Valid @ModelAttribute("publishForm") final PublishForm form,
                                final BindingResult bindingResult,
                                final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return publishForm(form, null);
        }

        try {
            final Post post = postService.publish(currentUser.getId(), form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(),
                    form.getDescription(), form.getCondition(), form.getPressingYear(), form.getZone(),
                    form.toImageUploads());
            redirectAttributes.addFlashAttribute("postCreated", true);
            return new ModelAndView("redirect:/post/" + post.getId());
        } catch (final DuplicatePostException e) {
            bindingResult.reject("publish.duplicate");
            return publishForm(form, null);
        } catch (final ConcurrentPublishException e) {
            bindingResult.reject("publish.concurrent");
            return publishForm(form, null);
        }
    }

    @PreAuthorize(CAN_MODERATE_POST)
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

    /*
     * El validador revisa las fotos nuevas una por una; el tope de la galeria cuenta tambien las
     * que se conservan, y eso lo sabe recien PostService: lo informa con InvalidImageException.
     */
    @PreAuthorize(CAN_MODERATE_POST)
    @RequestMapping(value = "/post/{postId:[0-9]+}/edit", method = RequestMethod.POST)
    public ModelAndView edit(@PathVariable("postId") final long postId,
                             @AuthenticationPrincipal final AuthenticatedUser currentUser,
                             @Valid @ModelAttribute("publishForm") final PublishForm form,
                             final BindingResult bindingResult,
                             final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return editView(postId, currentUser.getId());
        }

        try {
            postService.update(postId, currentUser.getId(), form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(), form.getDescription(),
                    form.getCondition(), form.getPressingYear(), form.getZone(),
                    form.toImageUploads(), form.getRemovedImageIds());
            redirectAttributes.addFlashAttribute("postUpdated", true);
            return new ModelAndView("redirect:/post/" + postId);
        } catch (final InvalidImageException e) {
            bindingResult.rejectValue("covers", "publish.cover.invalid");
        } catch (final DuplicatePostException e) {
            bindingResult.reject("publish.duplicate");
        } catch (final ConcurrentPublishException e) {
            bindingResult.reject("publish.concurrent");
        }
        return editView(postId, currentUser.getId());
    }

    @PreAuthorize(CAN_MODERATE_POST)
    @RequestMapping(value = "/post/{postId:[0-9]+}/delete", method = RequestMethod.POST)
    public ModelAndView delete(@PathVariable("postId") final long postId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        postService.delete(postId, currentUser.getId());
        redirectAttributes.addFlashAttribute("postDeleted", true);
        return new ModelAndView(currentUser.isAdmin() ? "redirect:/" : "redirect:/profile#posts");
    }

    private ModelAndView editView(final long postId, final long actorId) {
        return editView(postId, postService.findEditableById(postId, actorId));
    }

    private ModelAndView editView(final long postId, final PostSummary post) {
        final ModelAndView modelAndView = publishView(true, postId);
        modelAndView.addObject("existingCoverImageId", post.getCoverImageId());
        modelAndView.addObject("fallbackCoverImageId", postService.findAlbumCoverImageId(postId).orElse(null));
        modelAndView.addObject("uploadedImageIds", postService.findUploadedImageIds(postId));
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

    @ExceptionHandler(PostUnavailableException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView unavailable() {
        return new ModelAndView("error/409");
    }
}
```
