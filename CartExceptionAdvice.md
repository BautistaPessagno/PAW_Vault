---
title: "CartExceptionAdvice"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java"]
---

# CartExceptionAdvice

Solo para [[CartController]] y con prioridad sobre [[ErrorResponseAdvice]]: convierte los motivos por los que el carrito no puede agregar o enviar en una redirección a la pantalla de origen con su aviso.

## Guía de lectura

Operaciones para localizar en la fuente: `openInquiryExists`, `addRejected`, `addressNotFound`, `addressLimitExceeded`, `nothingToSend`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressLimitExceededException]], [[AddressNotFoundException]], [[CartAddRejectedException]], [[CartController]], [[CartService]], [[ListingQueries]], [[NothingToSendException]], [[OpenInquiryExistsException]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java>), líneas 1–74.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.AddressLimitExceededException;
import ar.edu.itba.paw.services.AddressNotFoundException;
import ar.edu.itba.paw.services.CartAddRejectedException;
import ar.edu.itba.paw.services.CartService;
import ar.edu.itba.paw.services.NothingToSendException;
import ar.edu.itba.paw.services.OpenInquiryExistsException;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.servlet.http.HttpServletRequest;

/*
 * Los motivos por los que el carrito no puede agregar o enviar son casos esperables (otra
 * pestania, una reserva justo en ese momento), no paginas de error: cada uno vuelve a la
 * pantalla de donde vino con su aviso. Solo para CartController, y antes que ErrorResponseAdvice,
 * que para el resto de la aplicacion sigue respondiendo 403 y 404.
 */
@Order(Ordered.HIGHEST_PRECEDENCE)
@ControllerAdvice(assignableTypes = CartController.class)
public class CartExceptionAdvice {

    // Si ya lo consulto, va a esa Conversacion, como el contacto.
    @ExceptionHandler(OpenInquiryExistsException.class)
    public ModelAndView openInquiryExists(final OpenInquiryExistsException exception,
                                          final RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("saleNotice", "inquiry.alreadyOpen");
        redirectAttributes.addAttribute("inquiryId", exception.getInquiryId());
        return new ModelAndView("redirect:/inquiries/{inquiryId}#conversation");
    }

    // Vuelve a la ficha del post, con el listado de donde vino, a mostrar por que no se agrego.
    @ExceptionHandler(CartAddRejectedException.class)
    public ModelAndView addRejected(final CartAddRejectedException exception, final HttpServletRequest request,
                                    final RedirectAttributes redirectAttributes) {
        switch (exception.getReason()) {
            case OWN_POST -> redirectAttributes.addFlashAttribute("cartWarning", "cart.error.ownPost");
            case UNAVAILABLE -> redirectAttributes.addFlashAttribute("cartWarning", "cart.error.unavailable");
            case ALREADY_IN_CART -> redirectAttributes.addFlashAttribute("cartWarning", "cart.error.alreadyInCart");
            // Aparte de cartWarning porque lleva el tope como argumento.
            case CART_FULL -> redirectAttributes.addFlashAttribute("cartFullLimit", CartService.MAX_ITEMS);
        }
        redirectAttributes.addAttribute("postId", exception.getPostId());
        final String listingQuery = ListingQueries.sanitize(request.getParameter("from"));
        if (!listingQuery.isEmpty()) {
            redirectAttributes.addAttribute("from", listingQuery);
        }
        return new ModelAndView("redirect:/post/{postId}");
    }

    // La eligio y despues la archivo en otra pestania: vuelve al carrito a elegir otra.
    @ExceptionHandler(AddressNotFoundException.class)
    public ModelAndView addressNotFound(final RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("cartWarning", "post.contact.address.unavailable");
        return new ModelAndView("redirect:/cart");
    }

    @ExceptionHandler(AddressLimitExceededException.class)
    public ModelAndView addressLimitExceeded(final RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("addressLimitReached", true);
        return new ModelAndView("redirect:/cart");
    }

    @ExceptionHandler(NothingToSendException.class)
    public ModelAndView nothingToSend(final RedirectAttributes redirectAttributes) {
        redirectAttributes.addFlashAttribute("cartWarning", "cart.nothingToSend");
        return new ModelAndView("redirect:/cart");
    }
}
```
