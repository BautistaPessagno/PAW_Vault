---
title: "CartServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java"]
---

# CartServiceImplTest

Tests de `CartServiceImpl` en `services`: 21 casos declarados. Cubre: agregar con cada motivo de rechazo, tope, pantalla de envío, envío parcial, nada para enviar y dirección nueva. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `BUYER_ID`, `SELLER_ID`, `OTHER_SELLER_ID`, `POST_ID`, `ADDRESS_ID`, `OPEN_INQUIRY_ID`, `CONTACTABLE`, `BLOCKING`, `cartItemDao`, `postService`, `inquiryService`, `addressService`, `userService`, `cartService`.

Operaciones para localizar en la fuente: `post`, `detail`, `item`, `address`.

Casos declarados: 21.

- `testAddWhenPostIsContactableReturnsThePost`
- `testAddWhenPostIsAlreadyInCartReturnsAlreadyInCartRejection`
- `testAddWhenCartHasMaxSendableItemsReturnsCartFullRejection`
- `testAddWhenCartAddRaceLosesReturnsAlreadyInCartRejection`
- `testAddWhenBuyerOwnsPostReturnsOwnPostRejection`
- `testAddWhenPostIsReservedReturnsUnavailableRejection`
- `testAddWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsException`
- `testFindCheckoutWhenItemsAreFromTwoSellersReturnsOneGroupPerSellerAndTotals`
- `testFindPostViewWhenBuyerHasOpenInquiryReturnsItsId`
- `testFindPostViewWhenPostIsContactableAndInCartReturnsInCart`
- `testFindPostViewWhenBuyerOwnsPostReturnsOwnPost`
- `testFindPostViewWhenPostIsSoldReturnsUnavailable`
- `testFindPostViewWithoutSessionWhenPostIsReservedReturnsUnavailable`
- `testFindPostViewWithoutSessionWhenPostIsAvailableReturnsContactable`
- `testCheckoutWhenCartIsEmptyReturnsNothingToSendException`
- `testCheckoutWhenEveryPostWasReservedMeanwhileReturnsNothingToSendException`
- `testCheckoutWhenOnePostChangedMeanwhileReturnsSentAndSkippedCounts`
- `testCheckoutWhenBuyerConsultedAPostMeanwhileReturnsItAsSkipped`
- `testCheckoutWhenAddressIsNotOwnedReturnsAddressNotFoundException`
- `testCheckoutWithNewAddressWhenPostsAreAvailableReturnsSentCount`
- `testCheckoutWithNewAddressWhenNothingIsSendableReturnsNothingToSendExceptionBeforeSavingAddress`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressNotFoundException]], [[AddressService]], [[Cart]], [[CartAddRejectedException]], [[CartCheckout]], [[CartCheckoutResult]], [[CartItem]], [[CartItemDao]], [[CartService]], [[CartServiceImpl]], [[Condition]], [[ContactState]], [[InquiryService]], [[InquiryStatus]], [[NothingToSendException]], [[OpenInquiryExistsException]], [[PostContactOptions]], [[PostDetail]], [[PostService]], [[PostStatus]], [[PostSummary]], [[PostView]], [[Province]], [[ShippingOptions]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java>), líneas 1–412.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Cart;
import ar.edu.itba.paw.models.CartCheckout;
import ar.edu.itba.paw.models.CartCheckoutResult;
import ar.edu.itba.paw.models.CartItem;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.ContactState;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.PostContactOptions;
import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostView;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ShippingOptions;
import ar.edu.itba.paw.persistence.CartItemDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;
import java.util.Set;

@ExtendWith(MockitoExtension.class)
public class CartServiceImplTest {

    private static final long BUYER_ID = 2;
    private static final long SELLER_ID = 1;
    private static final long OTHER_SELLER_ID = 3;
    private static final long POST_ID = 7;
    private static final long ADDRESS_ID = 4;
    private static final long OPEN_INQUIRY_ID = 9;
    private static final PostStatus CONTACTABLE = PostStatus.AVAILABLE;
    private static final List<InquiryStatus> BLOCKING = InquiryStatus.OPEN_STATUSES;

    @Mock
    private CartItemDao cartItemDao;

    @Mock
    private PostService postService;

    @Mock
    private InquiryService inquiryService;

    @Mock
    private AddressService addressService;

    @Mock
    private UserService userService;

    @InjectMocks
    private CartServiceImpl cartService;

    @Test
    public void testAddWhenPostIsContactableReturnsThePost() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(false);
        Mockito.when(cartItemDao.countByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(0);
        Mockito.when(cartItemDao.add(BUYER_ID, POST_ID)).thenReturn(true);

        // 2. Exercise
        final PostSummary result = cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        Assertions.assertEquals(POST_ID, result.getId());
    }

    @Test
    public void testAddWhenPostIsAlreadyInCartReturnsAlreadyInCartRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(true);

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.ALREADY_IN_CART, exception.getReason());
        Assertions.assertEquals(POST_ID, exception.getPostId());
    }

    @Test
    public void testAddWhenCartHasMaxSendableItemsReturnsCartFullRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(false);
        Mockito.when(cartItemDao.countByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(CartService.MAX_ITEMS);

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.CART_FULL, exception.getReason());
    }

    @Test
    public void testAddWhenCartAddRaceLosesReturnsAlreadyInCartRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(false);
        Mockito.when(cartItemDao.countByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(0);
        // Otra transaccion lo agrego entre el chequeo y el insert.
        Mockito.when(cartItemDao.add(BUYER_ID, POST_ID)).thenReturn(false);

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.ALREADY_IN_CART, exception.getReason());
    }

    @Test
    public void testAddWhenBuyerOwnsPostReturnsOwnPostRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, BUYER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.OWN_POST, exception.getReason());
    }

    @Test
    public void testAddWhenPostIsReservedReturnsUnavailableRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.RESERVED));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.UNAVAILABLE, exception.getReason());
    }

    @Test
    public void testAddWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsException() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.of(OPEN_INQUIRY_ID));

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final OpenInquiryExistsException exception = Assertions.assertThrows(OpenInquiryExistsException.class, add);
        Assertions.assertEquals(OPEN_INQUIRY_ID, exception.getInquiryId());
    }

    @Test
    public void testFindCheckoutWhenItemsAreFromTwoSellersReturnsOneGroupPerSellerAndTotals() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(
                item(10, SELLER_ID, "seller"), item(11, SELLER_ID, "seller"), item(12, OTHER_SELLER_ID, "other")));
        final ShippingOptions shipping = new ShippingOptions(List.of(address()), address(), true);
        Mockito.when(addressService.findShippingOptions(BUYER_ID)).thenReturn(shipping);

        // 2. Exercise
        final CartCheckout checkout = cartService.findCheckout(BUYER_ID);

        // 3. Assert
        Assertions.assertSame(shipping, checkout.getShipping());
        final Cart result = checkout.getCart();
        Assertions.assertEquals(3, result.getItemCount());
        Assertions.assertEquals(2, result.getSellerCount());
        Assertions.assertEquals(135000L, result.getTotalPrice());
        Assertions.assertEquals("seller", result.getGroups().get(0).getSellerUsername());
        Assertions.assertEquals(List.of(10L, 11L), result.getGroups().get(0).getItems().stream()
                .map(CartItem::getPostId).toList());
        Assertions.assertEquals("other", result.getGroups().get(1).getSellerUsername());
    }

    @Test
    public void testFindPostViewWhenBuyerHasOpenInquiryReturnsItsId() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, BUYER_ID, false)).thenReturn(detail(post(POST_ID, SELLER_ID, PostStatus.RESERVED)));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.of(OPEN_INQUIRY_ID));

        // 2. Exercise
        final PostContactOptions result = cartService.findPostView(POST_ID, BUYER_ID, false).getContact();

        // 3. Assert
        Assertions.assertEquals(ContactState.OPEN_INQUIRY, result.getState());
        Assertions.assertEquals(Optional.of(OPEN_INQUIRY_ID), result.getOpenInquiryId());
        Assertions.assertFalse(result.isInCart());
    }

    @Test
    public void testFindPostViewWhenPostIsContactableAndInCartReturnsInCart() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, BUYER_ID, false)).thenReturn(detail(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(true);

        // 2. Exercise
        final PostContactOptions result = cartService.findPostView(POST_ID, BUYER_ID, false).getContact();

        // 3. Assert
        Assertions.assertEquals(ContactState.CONTACTABLE, result.getState());
        Assertions.assertTrue(result.isInCart());
        Assertions.assertTrue(result.getOpenInquiryId().isEmpty());
    }

    @Test
    public void testFindPostViewWhenBuyerOwnsPostReturnsOwnPost() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, BUYER_ID, false)).thenReturn(detail(post(POST_ID, BUYER_ID, PostStatus.AVAILABLE)));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final PostContactOptions result = cartService.findPostView(POST_ID, BUYER_ID, false).getContact();

        // 3. Assert
        Assertions.assertEquals(ContactState.OWN_POST, result.getState());
        Assertions.assertFalse(result.isInCart());
    }

    @Test
    public void testFindPostViewWhenPostIsSoldReturnsUnavailable() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, BUYER_ID, false)).thenReturn(detail(post(POST_ID, SELLER_ID, PostStatus.SOLD)));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final PostContactOptions result = cartService.findPostView(POST_ID, BUYER_ID, false).getContact();

        // 3. Assert
        Assertions.assertEquals(ContactState.UNAVAILABLE, result.getState());
        Assertions.assertFalse(result.isContactable());
        Assertions.assertFalse(result.isInCart());
    }

    @Test
    public void testFindPostViewWithoutSessionWhenPostIsReservedReturnsUnavailable() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, null, false)).thenReturn(detail(post(POST_ID, SELLER_ID, PostStatus.RESERVED)));

        // 2. Exercise
        final PostView result = cartService.findPostView(POST_ID, null, false);

        // 3. Assert
        Assertions.assertEquals(POST_ID, result.getDetail().getPost().getId());
        Assertions.assertEquals(ContactState.UNAVAILABLE, result.getContact().getState());
        Assertions.assertTrue(result.getContact().getOpenInquiryId().isEmpty());
    }

    @Test
    public void testFindPostViewWithoutSessionWhenPostIsAvailableReturnsContactable() {
        // 1. Arrange
        Mockito.when(postService.findDetail(POST_ID, null, false)).thenReturn(detail(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE)));

        // 2. Exercise
        final PostView result = cartService.findPostView(POST_ID, null, false);

        // 3. Assert
        Assertions.assertTrue(result.getContact().isContactable());
        Assertions.assertFalse(result.getContact().isInCart());
    }

    @Test
    public void testCheckoutWhenCartIsEmptyReturnsNothingToSendException() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of());

        // 2. Exercise
        final Executable checkout = () -> cartService.checkout(BUYER_ID, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(NothingToSendException.class, checkout);
    }

    @Test
    public void testCheckoutWhenEveryPostWasReservedMeanwhileReturnsNothingToSendException() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(item(10, SELLER_ID, "seller")));
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, List.of(10L))).thenReturn(Set.of());
        Mockito.when(postService.lockByIds(List.of(10L))).thenReturn(List.of(post(10, SELLER_ID, PostStatus.RESERVED)));

        // 2. Exercise
        final Executable checkout = () -> cartService.checkout(BUYER_ID, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(NothingToSendException.class, checkout);
    }

    @Test
    public void testCheckoutWhenOnePostChangedMeanwhileReturnsSentAndSkippedCounts() {
        // 1. Arrange
        final List<Long> postIds = List.of(10L, 11L, 12L);
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(
                item(10, SELLER_ID, "seller"), item(11, SELLER_ID, "seller"), item(12, OTHER_SELLER_ID, "other")));
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, postIds)).thenReturn(Set.of());
        Mockito.when(postService.lockByIds(postIds)).thenReturn(List.of(post(10, SELLER_ID, PostStatus.AVAILABLE),
                post(11, SELLER_ID, PostStatus.SOLD), post(12, OTHER_SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.of(address()));

        // 2. Exercise
        final CartCheckoutResult result = cartService.checkout(BUYER_ID, ADDRESS_ID);

        // 3. Assert
        Assertions.assertEquals(2, result.getSentCount());
        Assertions.assertEquals(1, result.getSkippedCount());
    }

    @Test
    public void testCheckoutWhenBuyerConsultedAPostMeanwhileReturnsItAsSkipped() {
        // 1. Arrange
        final List<Long> postIds = List.of(10L, 12L);
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(
                item(10, SELLER_ID, "seller"), item(12, OTHER_SELLER_ID, "other")));
        // Al leer el carrito no habia Consulta; al volver a mirar con los posts bloqueados, si.
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, postIds)).thenReturn(Set.of(10L));
        Mockito.when(postService.lockByIds(postIds)).thenReturn(List.of(post(10, SELLER_ID, PostStatus.AVAILABLE),
                post(12, OTHER_SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.of(address()));

        // 2. Exercise
        final CartCheckoutResult result = cartService.checkout(BUYER_ID, ADDRESS_ID);

        // 3. Assert
        Assertions.assertEquals(1, result.getSentCount());
        Assertions.assertEquals(1, result.getSkippedCount());
    }

    @Test
    public void testCheckoutWhenAddressIsNotOwnedReturnsAddressNotFoundException() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(item(10, SELLER_ID, "seller")));
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, List.of(10L))).thenReturn(Set.of());
        Mockito.when(postService.lockByIds(List.of(10L))).thenReturn(List.of(post(10, SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable checkout = () -> cartService.checkout(BUYER_ID, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(AddressNotFoundException.class, checkout);
    }

    @Test
    public void testCheckoutWithNewAddressWhenPostsAreAvailableReturnsSentCount() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(item(10, SELLER_ID, "seller")));
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, List.of(10L))).thenReturn(Set.of());
        Mockito.when(postService.lockByIds(List.of(10L))).thenReturn(List.of(post(10, SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(addressService.create(BUYER_ID, "Belgrano", "850", null, "Mendoza", Province.MENDOZA, "5500",
                null)).thenReturn(address());

        // 2. Exercise
        final CartCheckoutResult result = cartService.checkoutWithNewAddress(BUYER_ID, "Belgrano", "850", null,
                "Mendoza", Province.MENDOZA, "5500", null);

        // 3. Assert
        Assertions.assertEquals(1, result.getSentCount());
        Assertions.assertEquals(0, result.getSkippedCount());
    }

    @Test
    public void testCheckoutWithNewAddressWhenNothingIsSendableReturnsNothingToSendExceptionBeforeSavingAddress() {
        // 1. Arrange
        Mockito.when(cartItemDao.findByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(List.of(item(10, SELLER_ID, "seller")));
        Mockito.when(inquiryService.findPostIdsWithOpenInquiry(BUYER_ID, List.of(10L))).thenReturn(Set.of());
        Mockito.when(postService.lockByIds(List.of(10L))).thenReturn(List.of(post(10, SELLER_ID, PostStatus.RESERVED)));
        // addressService.create queda sin stub: si se guardara la direccion antes de decidir que
        // no hay nada que enviar, devolveria null y el envio cortaria con otra excepcion.

        // 2. Exercise
        final Executable checkout = () -> cartService.checkoutWithNewAddress(BUYER_ID, "Belgrano", "850", null,
                "Mendoza", Province.MENDOZA, "5500", null);

        // 3. Assert
        Assertions.assertThrows(NothingToSendException.class, checkout);
    }

    private static PostSummary post(final long postId, final long sellerId, final PostStatus status) {
        return new PostSummary(postId, sellerId, "seller@example.com", "es", 3, "Versus", "IKV", 1997,
                null, null, 45000, null, Condition.USED, null, null, status);
    }

    private static PostDetail detail(final PostSummary post) {
        return new PostDetail(post, null, List.of(), false, false);
    }

    private static CartItem item(final long postId, final long sellerId, final String sellerUsername) {
        return new CartItem(postId, sellerId, sellerUsername, "Versus", "IKV", 1997, null, 45000);
    }

    private static Address address() {
        return new Address(ADDRESS_ID, BUYER_ID, "Belgrano", "850", null, "Mendoza", Province.MENDOZA, "5500",
                null, false);
    }
}
```
