---
title: "PostContactController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java"]
---

# PostContactController

Formulario de contacto de una publicación: carga el post contactable y las opciones de envío, y envía la consulta con dirección guardada o nueva. Ver [[Contact flow]].

## Guía de lectura

Datos y dependencias declaradas: `inquiryService`, `addressService`.

Operaciones para localizar en la fuente: `initBinder`, `contactForm`, `contact`, `buildContactView`, `postUnavailable`, `openInquiryExists`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressLimitExceededException]], [[AddressNotFoundException]], [[AddressService]], [[AuthenticatedUser]], [[ContactForm]], [[InquiryService]], [[LineBreakNormalizingEditor]], [[OpenInquiryExistsException]], [[PostSummary]], [[PostUnavailableException]], [[Province]], [[ShippingOptions]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>), líneas 1–126.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;
import ar.edu.itba.paw.services.AddressLimitExceededException;
import ar.edu.itba.paw.services.AddressNotFoundException;
import ar.edu.itba.paw.services.AddressService;
import ar.edu.itba.paw.services.InquiryService;
import ar.edu.itba.paw.services.OpenInquiryExistsException;
import ar.edu.itba.paw.services.PostUnavailableException;
import ar.edu.itba.paw.webapp.form.ContactForm;
import ar.edu.itba.paw.webapp.form.LineBreakNormalizingEditor;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
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

@Controller
public class PostContactController {

    private final InquiryService inquiryService;
    private final AddressService addressService;

    @Autowired
    public PostContactController(final InquiryService inquiryService, final AddressService addressService) {
        this.inquiryService = inquiryService;
        this.addressService = addressService;
    }

    // Recorta antes de validar, para que @Size mida el valor real y no los espacios de mas.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
        binder.registerCustomEditor(String.class, "contactMessage", new LineBreakNormalizingEditor());
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.GET)
    public ModelAndView contactForm(@PathVariable("postId") final long postId,
                                    @ModelAttribute("contactForm") final ContactForm form,
                                    @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final ShippingOptions shipping = addressService.findShippingOptions(currentUser.getId());
        // Solo en el GET inicial: al volver a mostrar un error se respeta lo que eligio.
        shipping.getDefaultAddress().ifPresent(address -> form.setAddressId(address.getId()));
        return buildContactView(postId, currentUser, shipping);
    }

    @RequestMapping(value = "/post/{postId:[0-9]+}/contact", method = RequestMethod.POST)
    public ModelAndView contact(@PathVariable("postId") final long postId,
                                @Valid @ModelAttribute("contactForm") final ContactForm form,
                                final BindingResult errors,
                                @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                final RedirectAttributes redirectAttributes) {
        if (errors.hasErrors()) {
            return buildContactView(postId, currentUser);
        }
        try {
            if (form.isNewAddress()) {
                inquiryService.submitWithNewAddress(postId, currentUser.getId(), form.getContactMessage(),
                        form.getStreet(), form.getStreetNumber(), form.getApartment(), form.getCity(),
                        form.getProvince(), form.getPostalCode(), form.getNotes());
            } else {
                inquiryService.submit(postId, currentUser.getId(), form.getContactMessage(), form.getAddressId());
            }
        } catch (final AddressNotFoundException e) {
            // La eligio y despues la archivo en otra pestania: se vuelve a elegir sin perder el mensaje.
            errors.rejectValue("addressId", "post.contact.address.unavailable");
            return buildContactView(postId, currentUser);
        } catch (final AddressLimitExceededException e) {
            // Llego al tope desde otra pestania: se vuelve a mostrar el form sin perder el mensaje.
            final ModelAndView modelAndView = buildContactView(postId, currentUser);
            modelAndView.addObject("addressLimitReached", true);
            return modelAndView;
        }

        // El aviso es para el comprador: vuelve a su propia bandeja, la de enviadas.
        redirectAttributes.addFlashAttribute("inquirySubmitted", true);
        return new ModelAndView("redirect:/inquiries/sent");
    }

    private ModelAndView buildContactView(final long postId, final AuthenticatedUser currentUser) {
        return buildContactView(postId, currentUser, addressService.findShippingOptions(currentUser.getId()));
    }

    private ModelAndView buildContactView(final long postId, final AuthenticatedUser currentUser,
                                          final ShippingOptions shipping) {
        final PostSummary post = inquiryService.findContactablePost(postId, currentUser.getId());
        final ModelAndView modelAndView = new ModelAndView("post/contact");
        modelAndView.addObject("post", post);
        modelAndView.addObject("addresses", shipping.getAddresses());
        modelAndView.addObject("provinces", Province.values());
        modelAndView.addObject("canAddAddress", shipping.isNewAddressAllowed());
        modelAndView.addObject("maxAddresses", AddressService.MAX_ACTIVE_ADDRESSES);
        return modelAndView;
    }

    @ExceptionHandler(PostUnavailableException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ModelAndView postUnavailable() {
        return new ModelAndView("error/409");
    }

    // Ya tiene una Consulta abierta por este vinilo: sigue en esa Conversacion, tanto al abrir
    // el formulario como al enviarlo.
    @ExceptionHandler(OpenInquiryExistsException.class)
    public ModelAndView openInquiryExists(final OpenInquiryExistsException exception,
                                          final RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.alreadyOpen");
        return new ModelAndView("redirect:/inquiries/" + exception.getInquiryId() + "#conversation");
    }
}
```
