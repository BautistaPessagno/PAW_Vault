---
title: "CartService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/CartService.java"]
---

# CartService

Contrato del carrito: agregar, quitar, pantalla de envío, contador, la ficha de un post con lo que se le ofrece a quien mira, y enviar con una dirección guardada o nueva. `MAX_ITEMS` es 20. Ver [[Cart flow]].

## Guía de lectura

Operaciones para localizar en la fuente: `add`, `remove`, `findCheckout`, `countByUser`, `findPostView`, `checkout`, `checkoutWithNewAddress`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CartCheckout]], [[CartCheckoutResult]], [[PostSummary]], [[PostView]], [[Province]].

Referenciado por: [[CartController]], [[CartCountAdvice]], [[CartExceptionAdvice]], [[CartServiceImpl]], [[CartServiceImplTest]], [[PostController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/CartService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/CartService.java>), líneas 1–55.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.CartCheckout;
import ar.edu.itba.paw.models.CartCheckoutResult;
import ar.edu.itba.paw.models.PostView;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;

public interface CartService {

    /*
     * Tope de vinilos visibles en el carrito al agregar: add() no deja pasarlo. No es un tope
     * absoluto: un Post reservado queda guardado pero oculto, y si su Venta se cancela vuelve a
     * verse aunque el carrito ya este lleno.
     */
    int MAX_ITEMS = 20;

    // Devuelve el post agregado. Lanza PostNotFoundException si el post no existe,
    // OpenInquiryExistsException si el comprador ya lo consulto y CartAddRejectedException si
    // es propio, no esta disponible, ya estaba en el carrito o el carrito tiene MAX_ITEMS vinilos.
    PostSummary add(long userId, long postId);

    // Sacar algo que no esta no es un error.
    void remove(long userId, long postId);

    /*
     * La pantalla de envio: el carrito y las direcciones del comprador. El carrito trae solo lo
     * que todavia se puede consultar, agrupado por Publicante. Lo demas queda guardado y oculto:
     * un Post reservado vuelve a verse si su Venta se cancela.
     */
    CartCheckout findCheckout(long userId);

    int countByUser(long userId);

    /*
     * La ficha del post (PostService.findDetail, mismos parametros) con lo que le ofrece a quien
     * mira: consultarlo y agregarlo, ir a su Consulta abierta o nada. Sin sesion (viewerId null)
     * solo se puede consultar lo disponible, y nunca esta en un carrito. Lanza
     * PostNotFoundException si el post no existe.
     */
    PostView findPostView(long postId, Long viewerId, boolean moderator);

    /*
     * Crea una Consulta por cada post del carrito que sigue disponible, todas con la misma
     * direccion, y los saca del carrito. Lo que dejo de estar disponible se omite y queda.
     * Lanza NothingToSendException si no se puede enviar ninguno, sin escribir nada, y
     * AddressNotFoundException si la direccion no es del comprador o esta archivada.
     */
    CartCheckoutResult checkout(long userId, long addressId);

    // Igual que checkout, guardando antes la direccion nueva en la libreta. Si no se envia
    // ninguna Consulta, la direccion tampoco queda. Lanza AddressLimitExceededException.
    CartCheckoutResult checkoutWithNewAddress(long userId, String street, String streetNumber, String apartment,
                                              String city, Province province, String postalCode, String notes);
}
```
