---
title: "CartCountAdvice"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartCountAdvice.java"]
---

# CartCountAdvice

Deja en cada request, para Cuentas verificadas, un contador perezoso del carrito que la cabecera lee. Es atributo del request y no del modelo para no colarse como parámetro en los `redirect:`.

## Guía de lectura

Datos y dependencias declaradas: `CART_COUNT`, `cartService`, `supplier`, `value`.

Operaciones para localizar en la fuente: `cartCount`, `LazyCount`, `getValue`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[CartService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartCountAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartCountAdvice.java>), líneas 1–57.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.services.CartService;
import ar.edu.itba.paw.webapp.security.AuthenticatedUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

import javax.servlet.http.HttpServletRequest;
import java.util.function.IntSupplier;

/*
 * La cantidad del carrito que muestra la cabecera de todas las paginas. Va como atributo del
 * request y no del modelo: un atributo de modelo se sumaria como query param a cada
 * "redirect:" de la aplicacion. Solo para cuentas verificadas, que son las que tienen carrito.
 * Se cuenta recien cuando la cabecera la lee: un POST que termina en redirect no consulta nada.
 */
@ControllerAdvice(basePackageClasses = CartCountAdvice.class)
public class CartCountAdvice {

    private static final String CART_COUNT = "cartCount";

    private final CartService cartService;

    @Autowired
    public CartCountAdvice(final CartService cartService) {
        this.cartService = cartService;
    }

    @ModelAttribute
    public void cartCount(@AuthenticationPrincipal final AuthenticatedUser currentUser,
                          final HttpServletRequest request) {
        if (currentUser != null && currentUser.isVerified()) {
            final long userId = currentUser.getId();
            request.setAttribute(CART_COUNT, new LazyCount(() -> cartService.countByUser(userId)));
        }
    }

    // Consulta la primera vez que la vista pide el valor y lo recuerda para el resto del request.
    public static final class LazyCount {

        private final IntSupplier supplier;
        private Integer value;

        private LazyCount(final IntSupplier supplier) {
            this.supplier = supplier;
        }

        public int getValue() {
            if (value == null) {
                value = supplier.getAsInt();
            }
            return value;
        }
    }
}
```
