---
title: "CartController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartController.java"]
---

# CartController

Carrito: ver, agregar desde la ficha (vuelve al listado de origen), quitar y enviar. Los rechazos esperables los resuelve [[CartExceptionAdvice]]. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `cartService`.

Operaciones para localizar en la fuente: `initBinder`, `cart`, `add`, `remove`, `checkout`, `buildCartView`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressService]], [[AuthenticatedUser]], [[CartCheckout]], [[CartCheckoutResult]], [[CartService]], [[ListingQueries]], [[Province]], [[ShippingAddressForm]].

Referenciado por: [[CartExceptionAdvice]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartController.java>), líneas 1–101.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.CartCheckout;
import ar.edu.itba.paw.models.CartCheckoutResult;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.services.AddressService;
import ar.edu.itba.paw.services.CartService;
import ar.edu.itba.paw.webapp.form.ShippingAddressForm;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.StringTrimmerEditor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import javax.validation.Valid;

// Los casos en que no se puede agregar ni enviar los resuelve CartExceptionAdvice.
@Controller
public class CartController {

    private final CartService cartService;

    @Autowired
    public CartController(final CartService cartService) {
        this.cartService = cartService;
    }

    // Recorta antes de validar, para que @Size mida el valor real y no los espacios de mas.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(String.class, new StringTrimmerEditor(true));
    }

    @RequestMapping(value = "/cart", method = RequestMethod.GET)
    public ModelAndView cart(@ModelAttribute("checkoutForm") final ShippingAddressForm form,
                             @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final CartCheckout checkout = cartService.findCheckout(currentUser.getId());
        // Solo en el GET: al volver a mostrar un error se respeta lo que eligio.
        checkout.getShipping().getDefaultAddress().ifPresent(address -> form.setAddressId(address.getId()));
        return buildCartView(checkout);
    }

    // Agregar vuelve al catalogo, con la busqueda, los filtros y la pagina de donde vino, para
    // seguir eligiendo sin pasos de mas.
    @RequestMapping(value = "/cart/add/{postId:[0-9]+}", method = RequestMethod.POST)
    public ModelAndView add(@PathVariable("postId") final long postId,
                            @RequestParam(value = "from", required = false) final String returnQuery,
                            @AuthenticationPrincipal final AuthenticatedUser currentUser,
                            final RedirectAttributes redirectAttributes) {
        cartService.add(currentUser.getId(), postId);
        redirectAttributes.addFlashAttribute("cartNotice", "cart.added");
        final String listingQuery = ListingQueries.sanitize(returnQuery);
        return new ModelAndView("redirect:/" + (listingQuery.isEmpty() ? "" : "?" + listingQuery));
    }

    @RequestMapping(value = "/cart/remove/{postId:[0-9]+}", method = RequestMethod.POST)
    public ModelAndView remove(@PathVariable("postId") final long postId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        cartService.remove(currentUser.getId(), postId);
        return new ModelAndView("redirect:/cart");
    }

    @RequestMapping(value = "/cart/checkout", method = RequestMethod.POST)
    public ModelAndView checkout(@Valid @ModelAttribute("checkoutForm") final ShippingAddressForm form,
                                 final BindingResult errors,
                                 @AuthenticationPrincipal final AuthenticatedUser currentUser,
                                 final RedirectAttributes redirectAttributes) {
        if (errors.hasErrors()) {
            return buildCartView(cartService.findCheckout(currentUser.getId()));
        }
        final CartCheckoutResult result = form.isNewAddress()
                ? cartService.checkoutWithNewAddress(currentUser.getId(), form.getStreet(), form.getStreetNumber(),
                        form.getApartment(), form.getCity(), form.getProvince(), form.getPostalCode(),
                        form.getNotes())
                : cartService.checkout(currentUser.getId(), form.getAddressId());

        // El seguimiento de cada Consulta sigue en la bandeja de enviadas.
        redirectAttributes.addFlashAttribute("cartResult", result);
        return new ModelAndView("redirect:/inquiries/sent");
    }

    private static ModelAndView buildCartView(final CartCheckout checkout) {
        final ModelAndView modelAndView = new ModelAndView("cart/index");
        modelAndView.addObject("cart", checkout.getCart());
        modelAndView.addObject("addresses", checkout.getShipping().getAddresses());
        modelAndView.addObject("provinces", Province.values());
        modelAndView.addObject("canAddAddress", checkout.getShipping().isNewAddressAllowed());
        modelAndView.addObject("maxAddresses", AddressService.MAX_ACTIVE_ADDRESSES);
        return modelAndView;
    }
}
```
