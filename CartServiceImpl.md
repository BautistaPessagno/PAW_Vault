---
title: "CartServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java"]
---

# CartServiceImpl

Carrito de consultas. Agregar valida con [[ContactRules]] y bloquea la Cuenta para el tope de 20. Enviar bloquea los posts en orden de id, vuelve a decidir qué sigue consultable, resuelve la dirección y crea las Consultas en lote; lo omitido queda en el carrito. También arma la ficha con lo que se le ofrece a quien mira. Ver [[Cart flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `cartItemDao`, `postService`, `inquiryService`, `addressService`, `userService`.

Operaciones para localizar en la fuente: `add`, `rejectAdd`, `remove`, `findCheckout`, `countByUser`, `findPostView`, `findContactable`, `countContactable`, `checkout`, `checkoutWithNewAddress`, `send`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AddressNotFoundException]], [[AddressService]], [[Cart]], [[CartAddRejectedException]], [[CartCheckout]], [[CartCheckoutResult]], [[CartItem]], [[CartItemDao]], [[CartSellerGroup]], [[CartService]], [[ContactRules]], [[ContactState]], [[InquiryService]], [[NothingToSendException]], [[OpenInquiryExistsException]], [[PostContactOptions]], [[PostDetail]], [[PostService]], [[PostSummary]], [[PostView]], [[Province]], [[UserService]].

Referenciado por: [[CartServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java>), líneas 1–199.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Cart;
import ar.edu.itba.paw.models.CartCheckout;
import ar.edu.itba.paw.models.CartCheckoutResult;
import ar.edu.itba.paw.models.CartItem;
import ar.edu.itba.paw.models.CartSellerGroup;
import ar.edu.itba.paw.models.ContactState;
import ar.edu.itba.paw.models.PostContactOptions;
import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostView;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.persistence.CartItemDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.LongSupplier;

@Service
public class CartServiceImpl implements CartService {

    private static final Logger LOGGER = LoggerFactory.getLogger(CartServiceImpl.class);

    private final CartItemDao cartItemDao;
    private final PostService postService;
    private final InquiryService inquiryService;
    private final AddressService addressService;
    private final UserService userService;

    @Autowired
    public CartServiceImpl(final CartItemDao cartItemDao, final PostService postService,
                           final InquiryService inquiryService, final AddressService addressService,
                           final UserService userService) {
        this.cartItemDao = cartItemDao;
        this.postService = postService;
        this.inquiryService = inquiryService;
        this.addressService = addressService;
        this.userService = userService;
    }

    // Los mismos chequeos que el contacto, en el mismo orden: los decide ContactRules.
    @Override
    @Transactional
    public PostSummary add(final long userId, final long postId) {
        final PostSummary post = postService.findById(postId);
        final Optional<Long> openInquiryId = inquiryService.findOpenInquiryId(postId, userId);
        switch (ContactRules.stateOf(post.getStatus(), post.getUserId(), userId, openInquiryId.isPresent())) {
            case OPEN_INQUIRY -> throw new OpenInquiryExistsException(openInquiryId.orElseThrow());
            case OWN_POST -> throw rejectAdd(userId, postId, CartAddRejectedException.Reason.OWN_POST);
            case UNAVAILABLE -> throw rejectAdd(userId, postId, CartAddRejectedException.Reason.UNAVAILABLE);
            case CONTACTABLE -> { }
        }
        // Bloquear la cuenta serializa dos agregados simultaneos: el segundo cuenta despues del
        // primero y no pasa el tope. Repetido gana sobre lleno: el aviso es mas preciso.
        userService.lockById(userId);
        if (cartItemDao.contains(userId, postId)) {
            throw rejectAdd(userId, postId, CartAddRejectedException.Reason.ALREADY_IN_CART);
        }
        if (countContactable(userId) >= MAX_ITEMS) {
            throw rejectAdd(userId, postId, CartAddRejectedException.Reason.CART_FULL);
        }
        if (!cartItemDao.add(userId, postId)) {
            throw rejectAdd(userId, postId, CartAddRejectedException.Reason.ALREADY_IN_CART);
        }
        LOGGER.info("Added to cart userId={} postId={}", userId, postId);
        return post;
    }

    private static CartAddRejectedException rejectAdd(final long userId, final long postId,
                                                      final CartAddRejectedException.Reason reason) {
        LOGGER.warn("Rejected cart add userId={} postId={} reason={}", userId, postId, reason);
        return new CartAddRejectedException(postId, reason);
    }

    @Override
    @Transactional
    public void remove(final long userId, final long postId) {
        if (cartItemDao.remove(userId, postId)) {
            LOGGER.info("Removed from cart userId={} postId={}", userId, postId);
        }
    }

    // El DAO ya viene ordenado por Publicante: el LinkedHashMap arma los grupos en ese orden.
    @Override
    @Transactional(readOnly = true)
    public CartCheckout findCheckout(final long userId) {
        final List<CartItem> items = findContactable(userId);
        final Map<Long, List<CartItem>> itemsBySeller = new LinkedHashMap<>();
        for (final CartItem item : items) {
            itemsBySeller.computeIfAbsent(item.getSellerId(), ignored -> new ArrayList<>()).add(item);
        }
        final List<CartSellerGroup> groups = new ArrayList<>();
        itemsBySeller.forEach((sellerId, sellerItems) ->
                groups.add(new CartSellerGroup(sellerId, sellerItems.get(0).getSellerUsername(), sellerItems)));
        final long totalPrice = items.stream().mapToLong(CartItem::getPrice).sum();
        return new CartCheckout(new Cart(groups, items.size(), totalPrice),
                addressService.findShippingOptions(userId));
    }

    @Override
    @Transactional(readOnly = true)
    public int countByUser(final long userId) {
        return countContactable(userId);
    }

    @Override
    @Transactional(readOnly = true)
    public PostView findPostView(final long postId, final Long viewerId, final boolean moderator) {
        final PostDetail detail = postService.findDetail(postId, viewerId, moderator);
        final PostSummary post = detail.getPost();
        if (viewerId == null) {
            return new PostView(detail,
                    new PostContactOptions(ContactRules.stateForAnonymous(post.getStatus()), null, false));
        }
        final Optional<Long> openInquiryId = inquiryService.findOpenInquiryId(postId, viewerId);
        final ContactState state = ContactRules.stateOf(post.getStatus(), post.getUserId(), viewerId,
                openInquiryId.isPresent());
        final boolean inCart = state == ContactState.CONTACTABLE && cartItemDao.contains(viewerId, postId);
        return new PostView(detail, new PostContactOptions(state, openInquiryId.orElse(null), inCart));
    }

    // Lo que se puede consultar, con las mismas constantes de ContactRules filtradas en la base.
    private List<CartItem> findContactable(final long userId) {
        return cartItemDao.findByUserId(userId, ContactRules.CONTACTABLE_POST_STATUS,
                ContactRules.BLOCKING_INQUIRY_STATUSES);
    }

    private int countContactable(final long userId) {
        return cartItemDao.countByUserId(userId, ContactRules.CONTACTABLE_POST_STATUS,
                ContactRules.BLOCKING_INQUIRY_STATUSES);
    }

    @Override
    @Transactional
    public CartCheckoutResult checkout(final long userId, final long addressId) {
        return send(userId, () -> {
            // La pudo archivar en otra pestania despues de abrir el carrito.
            if (addressService.findActiveOwned(addressId, userId).isEmpty()) {
                LOGGER.warn("Rejected cart checkout with unavailable address userId={} addressId={}", userId,
                        addressId);
                throw new AddressNotFoundException();
            }
            return addressId;
        });
    }

    @Override
    @Transactional
    public CartCheckoutResult checkoutWithNewAddress(final long userId, final String street,
                                                     final String streetNumber, final String apartment,
                                                     final String city, final Province province,
                                                     final String postalCode, final String notes) {
        return send(userId, () -> addressService.create(userId, street, streetNumber, apartment, city, province,
                postalCode, notes).getId());
    }

    /*
     * Lo que el comprador vio pudo cambiar mientras tenia el carrito abierto: se bloquean los
     * posts y se vuelve a decidir que se puede enviar. La direccion se resuelve recien despues,
     * para que un envio sin nada que mandar no deje una direccion nueva en la libreta.
     */
    private CartCheckoutResult send(final long userId, final LongSupplier addressId) {
        final List<Long> postIds = findContactable(userId).stream()
                .map(CartItem::getPostId)
                .toList();
        if (postIds.isEmpty()) {
            LOGGER.warn("Rejected empty cart checkout userId={}", userId);
            throw new NothingToSendException();
        }
        final List<PostSummary> posts = postService.lockByIds(postIds);
        final Set<Long> alreadyOpen = inquiryService.findPostIdsWithOpenInquiry(userId, postIds);
        final List<PostSummary> sendable = posts.stream()
                .filter(post -> ContactRules.stateOf(post.getStatus(), post.getUserId(), userId,
                        alreadyOpen.contains(post.getId())) == ContactState.CONTACTABLE)
                .toList();
        if (sendable.isEmpty()) {
            LOGGER.warn("Rejected cart checkout with nothing sendable userId={} postIds={}", userId, postIds);
            throw new NothingToSendException();
        }

        inquiryService.submitAll(userId, addressId.getAsLong(), sendable);
        final List<Long> sentIds = sendable.stream().map(PostSummary::getId).toList();
        cartItemDao.removeAll(userId, sentIds);

        final int skipped = postIds.size() - sentIds.size();
        LOGGER.info("Checked out cart userId={} sent={} skipped={}", userId, sentIds.size(), skipped);
        return new CartCheckoutResult(sentIds.size(), skipped);
    }
}
```
