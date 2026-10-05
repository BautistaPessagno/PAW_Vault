---
title: "InquiryServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java"]
---

# InquiryServiceImplTest

Tests de `InquiryServiceImpl` en `services`: 92 casos declarados. Cubre: contactabilidad, alta, bandejas (también filtradas), cada transición de la venta con sus estados inválidos (incluida una aceptación cuya transición falla), direcciones parciales, mensajes, reseñas, alta en lote, venta a la que volver y avisos después del commit. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `POST_ID`, `INQUIRY_ID`, `SELLER_ID`, `ALL_STATUSES`, `BUYER_ID`, `ADDRESS_ID`, `OUTSIDER_ID`, `BUYER_USERNAME`, `BUYER_EMAIL`, `SELLER_EMAIL`, `SELLER_LOCALE`, `RECEIPT`, `inquiryDao`, `messageDao`, `postService`, `userService`, `addressService`, `reviewService`, `emailService`, `inquiryService`, `notification`, `locale`, `updates`, `updateLocales`, `messages`, `messageLocales`.

Operaciones para localizar en la fuente: `setUp`, `tearDown`, `address`, `stubLock`, `confirmedSale`, `review`, `sale`, `stubSale`, `commitTransaction`, `post`, `inquiry`, `message`, `pendingOnAvailablePost`, `summary`, `seller`, `buyer`, `sendPostInterestEmail`, `sendInquiryUpdateEmail`, `sendMessageEmail`.

Casos declarados: 92.

- `testFindContactablePostWhenPostIsAvailableReturnsPost`
- `testFindContactablePostWhenPostDoesNotExistReturnsPostNotFoundException`
- `testFindContactablePostWhenPostIsSoldReturnsPostUnavailableException`
- `testFindContactablePostWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenMessageHasSurroundingSpacesReturnsInquiryNotifiedInPublisherLocale`
- `testSubmitWhenMessageIsBlankReturnsInquiryWithoutMessage`
- `testSubmitAllWhenPostsAreFromTwoSellersReturnsOneNotificationPerSeller`
- `testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenPostIsSoldReturnsPostUnavailableException`
- `testSubmitWhenAddressIsArchivedReturnsAddressNotFoundException`
- `testSubmitWithNewAddressWhenPostIsAvailableReturnsInquiryWithTheNewAddress`
- `testSubmitWithNewAddressWhenPostIsSoldReturnsPostUnavailableException`
- `testFindContactablePostWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsExceptionWithItsId`
- `testSubmitWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsExceptionWithItsId`
- `testSubmitWithNewAddressWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsException`
- `testSubmitWhenPreviousInquiryIsClosedReturnsNewInquiry`
- `testSendMessageWhenBuyerWritesOnPendingInquiryReturnsMessageNotifiedToPublisherOnCommit`
- `testSendMessageWhenPublisherWritesReturnsMessageNotifiedToBuyerInBuyerLocale`
- `testSendMessageWhenSaleIsConfirmedReturnsMessage`
- `testSendMessageWhenInquiryIsRejectedReturnsInvalidInquiryStateException`
- `testSendMessageWhenSaleIsCancelledReturnsInvalidInquiryStateException`
- `testSendMessageWhenUserIsNotAPartyReturnsForbiddenOperationException`
- `testSendMessageWhenBodyIsBlankReturnsInvalidMessageException`
- `testSendMessageWhenBodyExceedsTheLimitReturnsInvalidMessageException`
- `testSendMessageWhenInquiryIsRejectedAndBodyIsBlankReturnsInvalidInquiryStateException`
- `testAcceptWhenSellerHasPaymentInfoReturnsAwaitingPaymentAndNotifiesBuyer`
- `testAcceptWhenTransitionFailsReturnsConflictWithoutNotification`
- `testAcceptWhenSellerHasNoPaymentInfoReturnsMissingPaymentInfoException`
- `testAcceptWhenPostIsAlreadyReservedReturnsInvalidInquiryStateException`
- `testAcceptWhenInquiryWasRejectedAndSellerHasNoPaymentInfoReturnsInvalidInquiryStateException`
- `testAcceptWhenUserDoesNotOwnPostReturnsForbiddenOperationException`
- `testRejectWhenPostWasDeletedAndUserIsNotTheSellerReturnsForbiddenOperationException`
- `testAcceptWhenPostWasDeletedReturnsInvalidInquiryStateException`
- `testRejectWhenSellerOwnsPostReturnsRejectedAndNotifiesBuyer`
- `testRejectWhenInquiryIsNotPendingReturnsInvalidInquiryStateException`
- `testUploadReceiptWhenPaymentIsAwaitedReturnsNotificationToSeller`
- `testUploadReceiptWhenTypeIsNotAllowedReturnsInvalidReceiptException`
- `testUploadReceiptWhenFileExceedsTheLimitReturnsInvalidReceiptException`
- `testUploadReceiptWhenPdfLacksItsSignatureReturnsInvalidReceiptException`
- `testUploadReceiptWhenSaleWasCancelledReturnsInvalidInquiryStateException`
- `testUploadReceiptWhenUserIsTheSellerReturnsForbiddenOperationException`
- `testRequestNewReceiptWhenUserIsTheBuyerReturnsForbiddenOperationException`
- `testRequestNewReceiptWhenPaymentWasSubmittedReturnsNotificationToBuyer`
- `testRequestNewReceiptWhenInquiryIsAwaitingPaymentReturnsInvalidInquiryStateException`
- `testConfirmWhenPaymentWasSubmittedReturnsSoldPostAndRejectsWaitingInquiries`
- `testConfirmWhenUserIsTheBuyerReturnsForbiddenOperationException`
- `testConfirmWhenPaymentIsStillAwaitedReturnsInvalidInquiryStateException`
- `testConfirmWhenMarkSoldFailsReturnsInvalidInquiryStateException`
- `testCancelWhenBuyerCancelsBeforeUploadingReturnsReleasedPostAndNotifiesSeller`
- `testCancelWhenSellerCancelsAfterUploadReturnsNotificationToBuyer`
- `testCancelWhenBuyerCancelsAfterUploadingReturnsInvalidInquiryStateException`
- `testCancelWhenSellerCancelsAcceptedSaleReturnsInvalidInquiryStateException`
- `testCancelWhenUserIsNotAPartyReturnsForbiddenOperationException`
- `testCancelWhenReleaseFailsReturnsInvalidInquiryStateException`
- `testFindDetailWhenSellerHasNoPaymentInfoReturnsDetailWithMissingPaymentInfo`
- `testFindDetailWhenSellerAskedForAnotherReceiptReturnsReceiptRequested`
- `testFindDetailWhenSellerOpensPendingInquiryReturnsCityAndProvinceOnly`
- `testFindDetailWhenSellerOpensReservedSaleReturnsFullAddress`
- `testFindDetailWhenUserIsNotAPartyReturnsForbiddenOperationException`
- `testFindDetailWhenPublisherOpensPendingInquiryReturnsCanDecideAndWriteWithMessages`
- `testFindDetailWhenBuyerOpensPendingInquiryReturnsCanWriteButCannotDecide`
- `testFindDetailWhenPostIsReservedForAnotherBuyerReturnsCanRejectButCannotAccept`
- `testFindDetailWhenInquiryIsRejectedReturnsReadOnlyConversation`
- `testFindDetailWhenSaleIsConfirmedReturnsWritableSale`
- `testFindDetailWhenViewerReviewedConfirmedSaleReturnsOwnReview`
- `testFindDetailWhenSaleIsNotConfirmedReturnsDetailWithoutReview`
- `testSaveReviewWhenBuyerReviewsConfirmedSaleReturnsReviewForSeller`
- `testSaveReviewWhenSellerReviewsConfirmedSaleReturnsReviewForBuyer`
- `testSaveReviewWhenActorIsOutsiderReturnsForbiddenOperationException`
- `testSaveReviewWhenSaleIsNotConfirmedReturnsInvalidInquiryStateException`
- `testRemoveReviewWhenReviewWasAlreadyRemovedReturnsFalse`
- `testRemoveReviewWhenReviewIsActiveReturnsTrue`
- `testRemoveReviewWhenInquiryDoesNotExistReturnsInquiryNotFoundException`
- `testRemoveReviewWhenActorIsOutsiderReturnsForbiddenOperationException`
- `testFindReceiptWhenNothingWasUploadedReturnsReceiptNotFoundException`
- `testFindReceiptWhenUserIsNotAPartyReturnsForbiddenOperationException`
- `testFindReceiptWhenInquiryDoesNotExistReturnsInquiryNotFoundException`
- `testFindSaleToResumeWhenUserIsSellerReturnsInquiryId`
- `testFindSaleToResumeWhenUserIsBuyerReturnsEmpty`
- `testFindSaleToResumeWhenInquiryDoesNotExistReturnsEmpty`
- `testFindReceivedGroupedByPostWhenSecondPageOfSevenGroupsReturnsGroupedPage`
- `testFindReceivedGroupedByPostWhenInquiryIsPendingReturnsCityAndProvinceOnly`
- `testFindReceivedGroupedByPostWhenFilteringPendingReturnsPendingWithCityAndProvinceOnly`
- `testFindSentGroupedByPostWhenFilteringClosedReturnsRejectedAndCancelledPage`
- `testFindReceivedGroupedByPostWhenInquiryIsAcceptedReturnsFullAddress`
- `testFindReceivedGroupedByPostWhenInquiryAwaitsPaymentReturnsFullAddress`
- `testFindReceivedGroupedByPostWhenSaleWasCancelledReturnsCityAndProvinceOnly`
- `testFindReceivedGroupedByPostWhenPageIsPastTheLastOneReturnsPageNotFoundException`
- `testFindReceivedGroupedByPostWhenPageIsBelowOneReturnsPageNotFoundException`
- `testFindReceivedGroupedByPostWhenSellerHasNoInquiriesReturnsEmptyFirstPage`
- `testFindSentGroupedByPostWhenBuyerRepeatsAPostReturnsOneGroupWithSeller`
- `testFindSentGroupedByPostWhenPostsWereDeletedReturnsOneGroupPerAlbumAndSeller`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressNotFoundException]], [[AddressService]], [[Condition]], [[EmailService]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryDao]], [[InquiryDetail]], [[InquiryEvent]], [[InquiryGroup]], [[InquiryNotFoundException]], [[InquiryPage]], [[InquiryParties]], [[InquiryServiceImpl]], [[InquiryStatus]], [[InquiryStatusFilter]], [[InquirySummary]], [[InquiryUpdateNotification]], [[InvalidInquiryStateException]], [[InvalidMessageException]], [[InvalidReceiptException]], [[Message]], [[MessageDao]], [[MessageNotification]], [[MessageRules]], [[MissingPaymentInfoException]], [[OpenInquiryExistsException]], [[PageNotFoundException]], [[PaymentInfo]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostService]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[Province]], [[ReceiptNotFoundException]], [[ReceiptRules]], [[Review]], [[ReviewService]], [[User]], [[UserRole]], [[UserService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java>), líneas 1–1619.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryDetail;
import ar.edu.itba.paw.models.InquiryGroup;
import ar.edu.itba.paw.models.InquiryPage;
import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquiryStatusFilter;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.Message;
import ar.edu.itba.paw.models.MessageRules;
import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.ReceiptRules;
import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.MessageDao;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class InquiryServiceImplTest {

    private static final long POST_ID = 7;
    private static final long INQUIRY_ID = 9;
    private static final long SELLER_ID = 1;
    private static final List<InquiryStatus> ALL_STATUSES = List.of(InquiryStatus.values());
    private static final long BUYER_ID = 2;
    private static final long ADDRESS_ID = 4;
    private static final long OUTSIDER_ID = 99;
    private static final String BUYER_USERNAME = "buyer";
    private static final String BUYER_EMAIL = "buyer@example.com";
    private static final String SELLER_EMAIL = "seller@example.com";
    private static final String SELLER_LOCALE = "fr";
    private static final byte[] RECEIPT = "%PDF-1.7".getBytes(StandardCharsets.US_ASCII);

    @Mock
    private InquiryDao inquiryDao;

    @Mock
    private MessageDao messageDao;

    @Mock
    private PostService postService;

    @Mock
    private UserService userService;

    @Mock
    private AddressService addressService;

    @Mock
    private ReviewService reviewService;

    private CapturingEmailService emailService;

    private InquiryServiceImpl inquiryService;

    @BeforeEach
    public void setUp() {
        emailService = new CapturingEmailService();
        inquiryService = new InquiryServiceImpl(inquiryDao, messageDao, postService, userService, addressService,
                reviewService, emailService);
        TransactionSynchronizationManager.initSynchronization();
    }

    @AfterEach
    public void tearDown() {
        TransactionSynchronizationManager.clearSynchronization();
    }

    @Test
    public void testFindContactablePostWhenPostIsAvailableReturnsPost() {
        // 1. Arrange
        final PostSummary expected = post(SELLER_ID, PostStatus.AVAILABLE);
        Mockito.when(postService.findById(POST_ID)).thenReturn(expected);

        // 2. Exercise
        final PostSummary result = inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testFindContactablePostWhenPostDoesNotExistReturnsPostNotFoundException() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenThrow(new PostNotFoundException());

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, find);
    }

    @Test
    public void testFindContactablePostWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.SOLD));

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, find);
    }

    @Test
    public void testFindContactablePostWhenBuyerOwnsPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(BUYER_ID, PostStatus.AVAILABLE));

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, find);
    }

    @Test
    public void testSubmitWhenMessageHasSurroundingSpacesReturnsInquiryNotifiedInPublisherLocale() {
        // 1. Arrange
        final Inquiry expected = inquiry();
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.of(address()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, ADDRESS_ID, 45000)).thenReturn(expected);
        Mockito.when(messageDao.create(INQUIRY_ID, BUYER_ID, "Quiero negociar el precio"))
                .thenReturn(message(BUYER_ID, "Quiero negociar el precio"));

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, "  Quiero negociar el precio  ", ADDRESS_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertNull(emailService.notification);
        commitTransaction();
        Assertions.assertEquals(SELLER_EMAIL, emailService.notification.getPublisherEmail());
        Assertions.assertEquals(BUYER_USERNAME, emailService.notification.getContactName());
        Assertions.assertEquals(INQUIRY_ID, emailService.notification.getPosts().get(0).getInquiryId());
        Assertions.assertEquals("Quiero negociar el precio", emailService.notification.getMessage());
        Assertions.assertEquals(SELLER_LOCALE, emailService.locale.getLanguage());
        // El primer Mensaje ya viaja en el mail de Consulta nueva: no dispara el de Mensaje nuevo.
        Assertions.assertTrue(emailService.messages.isEmpty());
    }

    @Test
    public void testSubmitWhenMessageIsBlankReturnsInquiryWithoutMessage() {
        // 1. Arrange
        final Inquiry expected = inquiry();
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.of(address()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, ADDRESS_ID, 45000)).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, "   ", ADDRESS_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertNull(emailService.notification);
        commitTransaction();
        Assertions.assertNull(emailService.notification.getMessage());
    }

    @Test
    public void testSubmitAllWhenPostsAreFromTwoSellersReturnsOneNotificationPerSeller() {
        // 1. Arrange
        final long otherSellerId = 3;
        final PostSummary first = post(10, SELLER_ID, "Versus");
        final PostSummary second = post(11, otherSellerId, "Cancion animal");
        final PostSummary third = post(12, SELLER_ID, "Kamikaze");
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(inquiryDao.createAll(BUYER_ID, ADDRESS_ID, Map.of(10L, 45000, 11L, 45000, 12L, 45000)))
                .thenReturn(Map.of(10L, inquiry(20, 10), 11L, inquiry(21, 11), 12L, inquiry(22, 12)));

        // 2. Exercise
        final List<PostInterestNotification> result =
                inquiryService.submitAll(BUYER_ID, ADDRESS_ID, List.of(first, second, third));

        // 3. Assert
        Assertions.assertEquals(2, result.size());
        final PostInterestNotification toFirstSeller = result.get(0);
        Assertions.assertEquals(List.of(20L, 22L), toFirstSeller.getPosts().stream()
                .map(PostInterestNotification.InterestedPost::getInquiryId).toList());
        Assertions.assertEquals(BUYER_USERNAME, toFirstSeller.getContactName());
        // Las Consultas del carrito no traen texto: la Conversacion empieza vacia.
        Assertions.assertNull(toFirstSeller.getMessage());
        Assertions.assertEquals(List.of(21L), result.get(1).getPosts().stream()
                .map(PostInterestNotification.InterestedPost::getInquiryId).toList());
    }

    @Test
    public void testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(BUYER_ID, PostStatus.AVAILABLE));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, null, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, submit);
    }

    @Test
    public void testSubmitWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.SOLD));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, null, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, submit);
    }

    @Test
    public void testSubmitWhenAddressIsArchivedReturnsAddressNotFoundException() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, null, ADDRESS_ID);

        // 3. Assert
        Assertions.assertThrows(AddressNotFoundException.class, submit);
    }

    @Test
    public void testSubmitWithNewAddressWhenPostIsAvailableReturnsInquiryWithTheNewAddress() {
        // 1. Arrange
        final Inquiry expected = inquiry();
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(addressService.create(BUYER_ID, "Av. Madero", "399", null, "Buenos Aires", Province.CABA,
                "1106", null)).thenReturn(address());
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, ADDRESS_ID, 45000)).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submitWithNewAddress(POST_ID, BUYER_ID, null, "Av. Madero", "399",
                null, "Buenos Aires", Province.CABA, "1106", null);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testSubmitWithNewAddressWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.SOLD));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submitWithNewAddress(POST_ID, BUYER_ID, null, "Av. Madero",
                "399", null, "Buenos Aires", Province.CABA, "1106", null);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, submit);
    }

    @Test
    public void testFindContactablePostWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsExceptionWithItsId() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryDao.findOpenIdByPostAndBuyer(POST_ID, BUYER_ID)).thenReturn(Optional.of(INQUIRY_ID));

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        final OpenInquiryExistsException exception = Assertions.assertThrows(OpenInquiryExistsException.class, find);
        Assertions.assertEquals(INQUIRY_ID, exception.getInquiryId());
    }

    @Test
    public void testSubmitWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsExceptionWithItsId() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryDao.findOpenIdByPostAndBuyer(POST_ID, BUYER_ID)).thenReturn(Optional.of(INQUIRY_ID));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, "Otra vez", ADDRESS_ID);

        // 3. Assert
        final OpenInquiryExistsException exception = Assertions.assertThrows(OpenInquiryExistsException.class,
                submit);
        Assertions.assertEquals(INQUIRY_ID, exception.getInquiryId());
    }

    @Test
    public void testSubmitWithNewAddressWhenBuyerHasOpenInquiryReturnsOpenInquiryExistsException() {
        // 1. Arrange
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryDao.findOpenIdByPostAndBuyer(POST_ID, BUYER_ID)).thenReturn(Optional.of(INQUIRY_ID));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submitWithNewAddress(POST_ID, BUYER_ID, null, "Av. Madero",
                "399", null, "Buenos Aires", Province.CABA, "1106", null);

        // 3. Assert
        Assertions.assertThrows(OpenInquiryExistsException.class, submit);
    }

    @Test
    public void testSubmitWhenPreviousInquiryIsClosedReturnsNewInquiry() {
        // 1. Arrange
        final Inquiry expected = inquiry();
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        // La anterior quedo rechazada o cancelada: ya no cuenta como abierta.
        Mockito.when(inquiryDao.findOpenIdByPostAndBuyer(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(addressService.findActiveOwned(ADDRESS_ID, BUYER_ID)).thenReturn(Optional.of(address()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, ADDRESS_ID, 45000)).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, null, ADDRESS_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testSendMessageWhenBuyerWritesOnPendingInquiryReturnsMessageNotifiedToPublisherOnCommit() {
        // 1. Arrange
        final Message expected = message(BUYER_ID, "Tiene rayones?");
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));
        Mockito.when(messageDao.create(INQUIRY_ID, BUYER_ID, "Tiene rayones?")).thenReturn(expected);
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));

        // 2. Exercise
        final Message result = inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, "  Tiene rayones?\r\n ");

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertTrue(emailService.messages.isEmpty());
        commitTransaction();
        Assertions.assertEquals(1, emailService.messages.size());
        final MessageNotification notification = emailService.messages.get(0);
        Assertions.assertEquals(SELLER_EMAIL, notification.getRecipientEmail());
        Assertions.assertEquals(BUYER_USERNAME, notification.getSenderUsername());
        Assertions.assertEquals("Tiene rayones?", notification.getBody());
        Assertions.assertEquals(INQUIRY_ID, notification.getInquiryId());
        Assertions.assertEquals(1997, notification.getReleaseYear());
        Assertions.assertEquals(SELLER_LOCALE, emailService.messageLocales.get(0).getLanguage());
    }

    @Test
    public void testSendMessageWhenPublisherWritesReturnsMessageNotifiedToBuyerInBuyerLocale() {
        // 1. Arrange
        final Message expected = message(SELLER_ID, "Esta impecable.");
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, "vende.discos")));
        Mockito.when(messageDao.create(INQUIRY_ID, SELLER_ID, "Esta impecable.")).thenReturn(expected);
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.RESERVED));

        // 2. Exercise
        final Message result = inquiryService.sendMessage(INQUIRY_ID, SELLER_ID, "Esta impecable.");

        // 3. Assert
        Assertions.assertSame(expected, result);
        commitTransaction();
        Assertions.assertEquals(BUYER_EMAIL, emailService.messages.get(0).getRecipientEmail());
        Assertions.assertEquals("seller", emailService.messages.get(0).getSenderUsername());
        Assertions.assertEquals("en", emailService.messageLocales.get(0).getLanguage());
    }

    @Test
    public void testSendMessageWhenSaleIsConfirmedReturnsMessage() {
        // 1. Arrange
        final Message expected = message(BUYER_ID, "Cuando lo despachas?");
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.ACCEPTED, true, null, "vende.discos")));
        Mockito.when(messageDao.create(INQUIRY_ID, BUYER_ID, "Cuando lo despachas?")).thenReturn(expected);
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.SOLD));

        // 2. Exercise
        final Message result = inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, "Cuando lo despachas?");

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testSendMessageWhenInquiryIsRejectedReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.REJECTED, false, null, null)));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, "Y ahora?");

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, send);
    }

    @Test
    public void testSendMessageWhenSaleIsCancelledReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.CANCELLED, false, null, "vende.discos")));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, SELLER_ID, "Una lastima");

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, send);
    }

    @Test
    public void testSendMessageWhenUserIsNotAPartyReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, OUTSIDER_ID, "Hola");

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, send);
    }

    @Test
    public void testSendMessageWhenBodyIsBlankReturnsInvalidMessageException() {
        // 1. Arrange
        final String blank = " \r\n ";
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, blank);

        // 3. Assert
        Assertions.assertThrows(InvalidMessageException.class, send);
    }

    @Test
    public void testSendMessageWhenBodyExceedsTheLimitReturnsInvalidMessageException() {
        // 1. Arrange
        final String tooLong = "a".repeat(MessageRules.MAX_LENGTH + 1);
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, tooLong);

        // 3. Assert
        Assertions.assertThrows(InvalidMessageException.class, send);
    }

    @Test
    public void testSendMessageWhenInquiryIsRejectedAndBodyIsBlankReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.REJECTED, false, null, null)));

        // 2. Exercise
        final Executable send = () -> inquiryService.sendMessage(INQUIRY_ID, BUYER_ID, " ");

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, send);
    }

    private static Address address() {
        return new Address(ADDRESS_ID, BUYER_ID, "Av. Madero", "399", null, "Buenos Aires", Province.CABA,
                "1106", null, false);
    }

    @Test
    public void testAcceptWhenSellerHasPaymentInfoReturnsAwaitingPaymentAndNotifiesBuyer() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(new InquirySummary(INQUIRY_ID, POST_ID, 3L, BUYER_ID, SELLER_ID,
                        BUYER_USERNAME, BUYER_EMAIL, "en", "seller", new PaymentInfo(null, "vende.discos"),
                        "Versus", "IKV", null, 39000, null, InquiryStatus.PENDING,
                        PostStatus.AVAILABLE, null, false, null, null)));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(userService.lockById(SELLER_ID)).thenReturn(seller("vende.discos"));
        Mockito.when(postService.reserve(POST_ID)).thenReturn(true);
        Mockito.when(inquiryDao.startSale(INQUIRY_ID, 45000))
                .thenReturn(true);

        // 2. Exercise
        final InquiryStatus result = inquiryService.accept(INQUIRY_ID, SELLER_ID).getStatus();

        // 3. Assert
        Assertions.assertEquals(InquiryStatus.AWAITING_PAYMENT, result);
        Assertions.assertTrue(emailService.updates.isEmpty());
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.ACCEPTED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(BUYER_EMAIL, emailService.updates.get(0).getRecipientEmail());
        Assertions.assertEquals("en", emailService.updateLocales.get(0).getLanguage());
    }

    @Test
    public void testAcceptWhenTransitionFailsReturnsConflictWithoutNotification() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, "vende.discos")));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(userService.lockById(SELLER_ID)).thenReturn(seller("vende.discos"));
        Mockito.when(postService.reserve(POST_ID)).thenReturn(true);
        Mockito.when(inquiryDao.startSale(INQUIRY_ID, 45000)).thenReturn(false);

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
        Assertions.assertTrue(emailService.updates.isEmpty());
    }

    @Test
    public void testAcceptWhenSellerHasNoPaymentInfoReturnsMissingPaymentInfoException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(userService.lockById(SELLER_ID)).thenReturn(seller(null));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(MissingPaymentInfoException.class, accept);
    }

    @Test
    public void testAcceptWhenPostIsAlreadyReservedReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, "vende.discos")));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.RESERVED));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    @Test
    public void testAcceptWhenInquiryWasRejectedAndSellerHasNoPaymentInfoReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.REJECTED, false, null, null)));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    @Test
    public void testAcceptWhenUserDoesNotOwnPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, "vende.discos")));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, accept);
    }

    @Test
    public void testRejectWhenPostWasDeletedAndUserIsNotTheSellerReturnsForbiddenOperationException() {
        // 1. Arrange
        final InquirySummary orphan = new InquirySummary(INQUIRY_ID, null, 3L, BUYER_ID, SELLER_ID, BUYER_USERNAME,
                BUYER_EMAIL, "en", "seller", PaymentInfo.NONE, "Versus", "IKV", null, null, null, InquiryStatus.PENDING,
                null, null, false, null, null);
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID)).thenReturn(Optional.of(orphan));

        // 2. Exercise
        final Executable reject = () -> inquiryService.reject(INQUIRY_ID, OUTSIDER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, reject);
    }

    @Test
    public void testAcceptWhenPostWasDeletedReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID)).thenReturn(Optional.of(
                new InquirySummary(INQUIRY_ID, null, 3L, BUYER_ID, SELLER_ID, BUYER_USERNAME, BUYER_EMAIL,
                        "en", "seller", new PaymentInfo(null, "vende.discos"), "Versus", "IKV", null, 45000, null,
                        InquiryStatus.PENDING, null, null, false, null, null)));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    @Test
    public void testRejectWhenSellerOwnsPostReturnsRejectedAndNotifiesBuyer() {
        // 1. Arrange
        stubLock();
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PENDING, InquiryStatus.REJECTED))
                .thenReturn(true);

        // 2. Exercise
        final Inquiry result = inquiryService.reject(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertEquals(InquiryStatus.REJECTED, result.getStatus());
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.REJECTED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(BUYER_EMAIL, emailService.updates.get(0).getRecipientEmail());
    }

    @Test
    public void testRejectWhenInquiryIsNotPendingReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubLock();
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PENDING, InquiryStatus.REJECTED))
                .thenReturn(false);

        // 2. Exercise
        final Executable reject = () -> inquiryService.reject(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, reject);
    }

    @Test
    public void testUploadReceiptWhenPaymentIsAwaitedReturnsNotificationToSeller() {
        // 1. Arrange
        stubSale(InquiryStatus.AWAITING_PAYMENT, false);
        Mockito.when(inquiryDao.saveReceipt(INQUIRY_ID, "application/pdf", RECEIPT)).thenReturn(true);

        // 2. Exercise
        inquiryService.uploadReceipt(INQUIRY_ID, BUYER_ID, "application/pdf", RECEIPT);

        // 3. Assert
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.RECEIPT_UPLOADED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(SELLER_EMAIL, emailService.updates.get(0).getRecipientEmail());
        Assertions.assertEquals(SELLER_LOCALE, emailService.updateLocales.get(0).getLanguage());
    }

    @Test
    public void testUploadReceiptWhenTypeIsNotAllowedReturnsInvalidReceiptException() {
        // 1. Arrange
        final byte[] page = "<html></html>".getBytes(StandardCharsets.US_ASCII);

        // 2. Exercise
        final Executable upload = () -> inquiryService.uploadReceipt(INQUIRY_ID, BUYER_ID, "text/html", page);

        // 3. Assert
        Assertions.assertThrows(InvalidReceiptException.class, upload);
    }

    @Test
    public void testUploadReceiptWhenFileExceedsTheLimitReturnsInvalidReceiptException() {
        // 1. Arrange
        final byte[] oversized = new byte[(int) ReceiptRules.MAX_BYTES + 1];

        // 2. Exercise
        final Executable upload = () -> inquiryService.uploadReceipt(INQUIRY_ID, BUYER_ID, "image/png", oversized);

        // 3. Assert
        Assertions.assertThrows(InvalidReceiptException.class, upload);
    }

    @Test
    public void testUploadReceiptWhenPdfLacksItsSignatureReturnsInvalidReceiptException() {
        // 1. Arrange
        final byte[] notAPdf = "<html></html>".getBytes(StandardCharsets.US_ASCII);

        // 2. Exercise
        final Executable upload = () -> inquiryService.uploadReceipt(INQUIRY_ID, BUYER_ID, "application/pdf",
                notAPdf);

        // 3. Assert
        Assertions.assertThrows(InvalidReceiptException.class, upload);
    }

    @Test
    public void testUploadReceiptWhenSaleWasCancelledReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.CANCELLED, false);
        Mockito.when(inquiryDao.saveReceipt(INQUIRY_ID, "application/pdf", RECEIPT)).thenReturn(false);

        // 2. Exercise
        final Executable upload = () -> inquiryService.uploadReceipt(INQUIRY_ID, BUYER_ID, "application/pdf", RECEIPT);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, upload);
    }

    @Test
    public void testUploadReceiptWhenUserIsTheSellerReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, "vende.discos")));

        // 2. Exercise
        final Executable upload = () -> inquiryService.uploadReceipt(INQUIRY_ID, SELLER_ID, "application/pdf",
                RECEIPT);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, upload);
    }

    @Test
    public void testRequestNewReceiptWhenUserIsTheBuyerReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PAYMENT_SUBMITTED, true, null, "vende.discos")));

        // 2. Exercise
        final Executable requestNewReceipt = () -> inquiryService.requestNewReceipt(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, requestNewReceipt);
    }

    @Test
    public void testRequestNewReceiptWhenPaymentWasSubmittedReturnsNotificationToBuyer() {
        // 1. Arrange
        stubSale(InquiryStatus.PAYMENT_SUBMITTED, true);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED,
                InquiryStatus.AWAITING_PAYMENT)).thenReturn(true);

        // 2. Exercise
        inquiryService.requestNewReceipt(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.RECEIPT_REQUESTED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(BUYER_EMAIL, emailService.updates.get(0).getRecipientEmail());
    }

    @Test
    public void testRequestNewReceiptWhenInquiryIsAwaitingPaymentReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.AWAITING_PAYMENT, false);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED,
                InquiryStatus.AWAITING_PAYMENT)).thenReturn(false);

        // 2. Exercise
        final Executable requestNewReceipt = () -> inquiryService.requestNewReceipt(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, requestNewReceipt);
    }

    @Test
    public void testConfirmWhenPaymentWasSubmittedReturnsSoldPostAndRejectsWaitingInquiries() {
        // 1. Arrange
        stubSale(InquiryStatus.PAYMENT_SUBMITTED, true);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.ACCEPTED))
                .thenReturn(true);
        Mockito.when(postService.markSold(POST_ID)).thenReturn(true);
        final InquirySummary waiting = new InquirySummary(11L, POST_ID, 3L, 8L, SELLER_ID, "other",
                "other@example.com", "es", "seller", PaymentInfo.NONE, "Versus", "IKV", null, 45000, null,
                InquiryStatus.PENDING, PostStatus.RESERVED, null, false, null, null);
        Mockito.when(inquiryDao.findPendingByPostId(POST_ID)).thenReturn(List.of(waiting));
        Mockito.when(inquiryDao.rejectOtherPending(POST_ID, INQUIRY_ID)).thenReturn(1);

        // 2. Exercise
        inquiryService.confirm(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        commitTransaction();
        Assertions.assertEquals(List.of(InquiryEvent.CONFIRMED, InquiryEvent.CONFIRMED, InquiryEvent.REJECTED),
                emailService.updates.stream().map(InquiryUpdateNotification::getEvent).toList());
        Assertions.assertEquals(List.of(BUYER_EMAIL, SELLER_EMAIL, "other@example.com"),
                emailService.updates.stream().map(InquiryUpdateNotification::getRecipientEmail).toList());
    }

    @Test
    public void testConfirmWhenUserIsTheBuyerReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PAYMENT_SUBMITTED, true, null, "vende.discos")));

        // 2. Exercise
        final Executable confirm = () -> inquiryService.confirm(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, confirm);
    }

    @Test
    public void testConfirmWhenPaymentIsStillAwaitedReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.AWAITING_PAYMENT, false);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.ACCEPTED))
                .thenReturn(false);

        // 2. Exercise
        final Executable confirm = () -> inquiryService.confirm(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, confirm);
    }

    @Test
    public void testConfirmWhenMarkSoldFailsReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.PAYMENT_SUBMITTED, true);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.ACCEPTED))
                .thenReturn(true);
        Mockito.when(postService.markSold(POST_ID)).thenReturn(false);

        // 2. Exercise
        final Executable confirm = () -> inquiryService.confirm(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, confirm);
    }

    @Test
    public void testCancelWhenBuyerCancelsBeforeUploadingReturnsReleasedPostAndNotifiesSeller() {
        // 1. Arrange
        stubSale(InquiryStatus.AWAITING_PAYMENT, false);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.AWAITING_PAYMENT, InquiryStatus.CANCELLED))
                .thenReturn(true);
        Mockito.when(postService.release(POST_ID)).thenReturn(true);

        // 2. Exercise
        inquiryService.cancel(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.CANCELLED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(SELLER_EMAIL, emailService.updates.get(0).getRecipientEmail());
    }

    @Test
    public void testCancelWhenSellerCancelsAfterUploadReturnsNotificationToBuyer() {
        // 1. Arrange
        stubSale(InquiryStatus.PAYMENT_SUBMITTED, true);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.CANCELLED))
                .thenReturn(true);
        Mockito.when(postService.release(POST_ID)).thenReturn(true);

        // 2. Exercise
        inquiryService.cancel(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        commitTransaction();
        Assertions.assertEquals(1, emailService.updates.size());
        Assertions.assertEquals(InquiryEvent.CANCELLED, emailService.updates.get(0).getEvent());
        Assertions.assertEquals(BUYER_EMAIL, emailService.updates.get(0).getRecipientEmail());
    }

    @Test
    public void testCancelWhenBuyerCancelsAfterUploadingReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.PAYMENT_SUBMITTED, true);

        // 2. Exercise
        final Executable cancel = () -> inquiryService.cancel(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, cancel);
    }

    @Test
    public void testCancelWhenSellerCancelsAcceptedSaleReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.ACCEPTED, true);

        // 2. Exercise
        final Executable cancel = () -> inquiryService.cancel(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, cancel);
    }

    @Test
    public void testCancelWhenUserIsNotAPartyReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, "vende.discos")));

        // 2. Exercise
        final Executable cancel = () -> inquiryService.cancel(INQUIRY_ID, OUTSIDER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, cancel);
    }

    @Test
    public void testCancelWhenReleaseFailsReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubSale(InquiryStatus.AWAITING_PAYMENT, false);
        Mockito.when(inquiryDao.updateStatus(INQUIRY_ID, InquiryStatus.AWAITING_PAYMENT, InquiryStatus.CANCELLED))
                .thenReturn(true);
        Mockito.when(postService.release(POST_ID)).thenReturn(false);

        // 2. Exercise
        final Executable cancel = () -> inquiryService.cancel(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, cancel);
    }

    @Test
    public void testFindDetailWhenSellerHasNoPaymentInfoReturnsDetailWithMissingPaymentInfo() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, null)));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertFalse(result.isSellerView());
        Assertions.assertTrue(result.isPaymentInfoMissing());
        Assertions.assertTrue(result.isCanUploadReceipt());
    }

    @Test
    public void testFindDetailWhenSellerAskedForAnotherReceiptReturnsReceiptRequested() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, true, null, "vende.discos")));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isReceiptRequested());
    }

    @Test
    public void testFindDetailWhenSellerOpensPendingInquiryReturnsCityAndProvinceOnly() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null).withAddress(address())));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertTrue(result.getInquiry().getAddress().isCityAndProvinceOnly());
    }

    @Test
    public void testFindDetailWhenSellerOpensReservedSaleReturnsFullAddress() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, null).withAddress(address())));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertEquals("Av. Madero", result.getInquiry().getAddress().getStreet());
    }

    @Test
    public void testFindDetailWhenUserIsNotAPartyReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.AWAITING_PAYMENT, false, null, "vende.discos")));

        // 2. Exercise
        final Executable find = () -> inquiryService.findDetail(INQUIRY_ID, OUTSIDER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, find);
    }

    @Test
    public void testFindDetailWhenPublisherOpensPendingInquiryReturnsCanDecideAndWriteWithMessages() {
        // 1. Arrange
        final List<Message> messages = List.of(message(BUYER_ID, "Hola"));
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID)).thenReturn(Optional.of(pendingOnAvailablePost()));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(messages);

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isCanAccept());
        Assertions.assertTrue(result.isCanReject());
        Assertions.assertTrue(result.isCanWrite());
        Assertions.assertFalse(result.isSale());
        Assertions.assertEquals(SELLER_ID, result.getViewerId());
        Assertions.assertEquals(messages, result.getMessages());
    }

    @Test
    public void testFindDetailWhenBuyerOpensPendingInquiryReturnsCanWriteButCannotDecide() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID)).thenReturn(Optional.of(pendingOnAvailablePost()));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of());

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertFalse(result.isCanAccept());
        Assertions.assertFalse(result.isCanReject());
        Assertions.assertTrue(result.isCanWrite());
    }

    @Test
    public void testFindDetailWhenPostIsReservedForAnotherBuyerReturnsCanRejectButCannotAccept() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, null)));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of());

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertFalse(result.isCanAccept());
        Assertions.assertTrue(result.isCanReject());
    }

    @Test
    public void testFindDetailWhenInquiryIsRejectedReturnsReadOnlyConversation() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.REJECTED, false, null, null)));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of(message(BUYER_ID, "Hola")));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertFalse(result.isCanWrite());
        Assertions.assertEquals(1, result.getMessages().size());
    }

    @Test
    public void testFindDetailWhenSaleIsConfirmedReturnsWritableSale() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.ACCEPTED, true, null, "vende.discos")));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of());

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isSale());
        Assertions.assertTrue(result.isCanWrite());
        Assertions.assertFalse(result.isCanReject());
    }

    @Test
    public void testFindDetailWhenViewerReviewedConfirmedSaleReturnsOwnReview() {
        // 1. Arrange
        final Review own = review(BUYER_ID, SELLER_ID, 4);
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.ACCEPTED, true, null, "vende.discos")));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of());
        Mockito.when(reviewService.findActive(INQUIRY_ID, BUYER_ID)).thenReturn(Optional.of(own));

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isCanReview());
        Assertions.assertSame(own, result.getOwnReview());
        Assertions.assertEquals(SELLER_ID, result.getCounterpartyId());
    }

    @Test
    public void testFindDetailWhenSaleIsNotConfirmedReturnsDetailWithoutReview() {
        // 1. Arrange
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PAYMENT_SUBMITTED, true, null, "vende.discos")));
        Mockito.when(messageDao.findByInquiryId(INQUIRY_ID)).thenReturn(List.of());

        // 2. Exercise
        final InquiryDetail result = inquiryService.findDetail(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertFalse(result.isCanReview());
        Assertions.assertNull(result.getOwnReview());
    }

    @Test
    public void testSaveReviewWhenBuyerReviewsConfirmedSaleReturnsReviewForSeller() {
        // 1. Arrange
        confirmedSale();
        Mockito.when(reviewService.save(INQUIRY_ID, BUYER_ID, SELLER_ID, 5, "Bien"))
                .thenReturn(review(BUYER_ID, SELLER_ID, 5));

        // 2. Exercise
        final Review saved = inquiryService.saveReview(INQUIRY_ID, BUYER_ID, 5, "Bien");

        // 3. Assert
        Assertions.assertEquals(SELLER_ID, saved.getSubjectId());
        Assertions.assertEquals(5, saved.getRating());
    }

    @Test
    public void testSaveReviewWhenSellerReviewsConfirmedSaleReturnsReviewForBuyer() {
        // 1. Arrange
        confirmedSale();
        Mockito.when(reviewService.save(INQUIRY_ID, SELLER_ID, BUYER_ID, 4, null))
                .thenReturn(review(SELLER_ID, BUYER_ID, 4));

        // 2. Exercise
        final Review saved = inquiryService.saveReview(INQUIRY_ID, SELLER_ID, 4, null);

        // 3. Assert
        Assertions.assertEquals(BUYER_ID, saved.getSubjectId());
    }

    @Test
    public void testSaveReviewWhenActorIsOutsiderReturnsForbiddenOperationException() {
        // 1. Arrange
        confirmedSale();

        // 2. Exercise
        final Executable save = () -> inquiryService.saveReview(INQUIRY_ID, OUTSIDER_ID, 5, null);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, save);
    }

    @Test
    public void testSaveReviewWhenSaleIsNotConfirmedReturnsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findByIdForUpdate(INQUIRY_ID)).thenReturn(Optional.of(
                new Inquiry(INQUIRY_ID, POST_ID, BUYER_ID, InquiryStatus.PAYMENT_SUBMITTED)));
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID)).thenReturn(Optional.of(
                new InquiryParties(BUYER_ID, SELLER_ID)));

        // 2. Exercise
        final Executable save = () -> inquiryService.saveReview(INQUIRY_ID, BUYER_ID, 5, null);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, save);
    }

    @Test
    public void testRemoveReviewWhenReviewWasAlreadyRemovedReturnsFalse() {
        // 1. Arrange
        // Un segundo POST de quitar llega cuando la Resena ya no esta vigente.
        confirmedSale();
        Mockito.when(reviewService.remove(INQUIRY_ID, BUYER_ID)).thenReturn(false);

        // 2. Exercise
        final boolean removed = inquiryService.removeReview(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertFalse(removed);
    }

    @Test
    public void testRemoveReviewWhenReviewIsActiveReturnsTrue() {
        // 1. Arrange
        confirmedSale();
        Mockito.when(reviewService.remove(INQUIRY_ID, BUYER_ID)).thenReturn(true);

        // 2. Exercise
        final boolean removed = inquiryService.removeReview(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(removed);
    }

    @Test
    public void testRemoveReviewWhenInquiryDoesNotExistReturnsInquiryNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findByIdForUpdate(INQUIRY_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable remove = () -> inquiryService.removeReview(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(InquiryNotFoundException.class, remove);
    }

    @Test
    public void testRemoveReviewWhenActorIsOutsiderReturnsForbiddenOperationException() {
        // 1. Arrange
        confirmedSale();

        // 2. Exercise
        final Executable remove = () -> inquiryService.removeReview(INQUIRY_ID, OUTSIDER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, remove);
    }

    @Test
    public void testFindReceiptWhenNothingWasUploadedReturnsReceiptNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID))
                .thenReturn(Optional.of(new InquiryParties(BUYER_ID, SELLER_ID)));
        Mockito.when(inquiryDao.findReceipt(INQUIRY_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable find = () -> inquiryService.findReceipt(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ReceiptNotFoundException.class, find);
    }

    @Test
    public void testFindReceiptWhenUserIsNotAPartyReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID))
                .thenReturn(Optional.of(new InquiryParties(BUYER_ID, SELLER_ID)));

        // 2. Exercise
        final Executable find = () -> inquiryService.findReceipt(INQUIRY_ID, OUTSIDER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, find);
    }

    @Test
    public void testFindReceiptWhenInquiryDoesNotExistReturnsInquiryNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable find = () -> inquiryService.findReceipt(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(InquiryNotFoundException.class, find);
    }

    @Test
    public void testFindSaleToResumeWhenUserIsSellerReturnsInquiryId() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID))
                .thenReturn(Optional.of(new InquiryParties(BUYER_ID, SELLER_ID)));

        // 2. Exercise
        final Optional<Long> result = inquiryService.findSaleToResume(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertEquals(Optional.of(INQUIRY_ID), result);
    }

    @Test
    public void testFindSaleToResumeWhenUserIsBuyerReturnsEmpty() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID))
                .thenReturn(Optional.of(new InquiryParties(BUYER_ID, SELLER_ID)));

        // 2. Exercise
        final Optional<Long> result = inquiryService.findSaleToResume(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindSaleToResumeWhenInquiryDoesNotExistReturnsEmpty() {
        // 1. Arrange
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Optional<Long> result = inquiryService.findSaleToResume(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenSecondPageOfSevenGroupsReturnsGroupedPage() {
        // 1. Arrange
        final List<InquirySummary> rows = List.of(
                summary(3, 20, InquiryStatus.PENDING),
                summary(2, 20, InquiryStatus.REJECTED),
                summary(1, 10, InquiryStatus.ACCEPTED));
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(7);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 5)).thenReturn(rows);

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 2);

        // 3. Assert
        Assertions.assertEquals(2, result.getPageNumber());
        Assertions.assertEquals(2, result.getTotalPages());
        Assertions.assertTrue(result.isHasPrevious());
        Assertions.assertFalse(result.isHasNext());
        Assertions.assertEquals(2, result.getGroups().size());
        Assertions.assertEquals(20L, result.getGroups().get(0).getPostId());
        Assertions.assertEquals(List.of(3L, 2L),
                result.getGroups().get(0).getInquiries().stream().map(InquirySummary::getId).toList());
        Assertions.assertEquals(10L, result.getGroups().get(1).getPostId());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenInquiryIsPendingReturnsCityAndProvinceOnly() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(1);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 0))
                .thenReturn(List.of(summary(3, 20, InquiryStatus.PENDING).withAddress(address())));

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 1);

        // 3. Assert
        final Address shown = result.getGroups().get(0).getInquiries().get(0).getAddress();
        Assertions.assertTrue(shown.isCityAndProvinceOnly());
        Assertions.assertNull(shown.getStreetNumber());
        Assertions.assertNull(shown.getPostalCode());
        Assertions.assertEquals("Buenos Aires", shown.getCity());
        Assertions.assertEquals(Province.CABA, shown.getProvince());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenFilteringPendingReturnsPendingWithCityAndProvinceOnly() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, List.of(InquiryStatus.PENDING))).thenReturn(1);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, List.of(InquiryStatus.PENDING), 5, 0))
                .thenReturn(List.of(summary(3, 20, InquiryStatus.PENDING).withAddress(address())));

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, InquiryStatusFilter.PENDING, 1);

        // 3. Assert
        final InquirySummary shown = result.getGroups().get(0).getInquiries().get(0);
        Assertions.assertEquals(3, shown.getId());
        Assertions.assertTrue(shown.getAddress().isCityAndProvinceOnly());
    }

    @Test
    public void testFindSentGroupedByPostWhenFilteringClosedReturnsRejectedAndCancelledPage() {
        // 1. Arrange
        final List<InquiryStatus> closed = List.of(InquiryStatus.REJECTED, InquiryStatus.CANCELLED);
        Mockito.when(inquiryDao.countGroupsByBuyerId(BUYER_ID, closed)).thenReturn(1);
        Mockito.when(inquiryDao.findByBuyerId(BUYER_ID, closed, 5, 0))
                .thenReturn(List.of(summary(4, 20, InquiryStatus.REJECTED)));

        // 2. Exercise
        final InquiryPage result = inquiryService.findSentGroupedByPost(BUYER_ID, InquiryStatusFilter.CLOSED, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getGroups().size());
        Assertions.assertEquals(InquiryStatus.REJECTED, result.getGroups().get(0).getInquiries().get(0).getStatus());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenInquiryIsAcceptedReturnsFullAddress() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(1);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 0))
                .thenReturn(List.of(summary(3, 20, InquiryStatus.ACCEPTED).withAddress(address())));

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 1);

        // 3. Assert
        final Address shown = result.getGroups().get(0).getInquiries().get(0).getAddress();
        Assertions.assertEquals("Av. Madero", shown.getStreet());
        Assertions.assertEquals("1106", shown.getPostalCode());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenInquiryAwaitsPaymentReturnsFullAddress() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(1);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 0))
                .thenReturn(List.of(summary(3, 20, InquiryStatus.AWAITING_PAYMENT).withAddress(address())));

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 1);

        // 3. Assert
        Assertions.assertEquals("Av. Madero", result.getGroups().get(0).getInquiries().get(0).getAddress().getStreet());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenSaleWasCancelledReturnsCityAndProvinceOnly() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(1);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 0))
                .thenReturn(List.of(summary(3, 20, InquiryStatus.CANCELLED).withAddress(address())));

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 1);

        // 3. Assert
        Assertions.assertTrue(result.getGroups().get(0).getInquiries().get(0).getAddress().isCityAndProvinceOnly());
    }

    @Test
    public void testFindReceivedGroupedByPostWhenPageIsPastTheLastOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(7);

        // 2. Exercise
        final Executable findPage = () -> inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 3);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindReceivedGroupedByPostWhenPageIsBelowOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(7);

        // 2. Exercise
        final Executable findPage = () -> inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 0);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindReceivedGroupedByPostWhenSellerHasNoInquiriesReturnsEmptyFirstPage() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID, ALL_STATUSES)).thenReturn(0);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, ALL_STATUSES, 5, 0)).thenReturn(List.of());

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, null, 1);

        // 3. Assert
        Assertions.assertTrue(result.getGroups().isEmpty());
        Assertions.assertEquals(0, result.getTotalPages());
        Assertions.assertFalse(result.isHasNext());
    }

    @Test
    public void testFindSentGroupedByPostWhenBuyerRepeatsAPostReturnsOneGroupWithSeller() {
        // 1. Arrange
        final List<InquirySummary> rows = List.of(
                summary(5, 30, InquiryStatus.PENDING),
                summary(6, 30, InquiryStatus.PENDING));
        Mockito.when(inquiryDao.countGroupsByBuyerId(BUYER_ID, ALL_STATUSES)).thenReturn(1);
        Mockito.when(inquiryDao.findByBuyerId(BUYER_ID, ALL_STATUSES, 5, 0)).thenReturn(rows);

        // 2. Exercise
        final InquiryPage result = inquiryService.findSentGroupedByPost(BUYER_ID, null, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getGroups().size());
        Assertions.assertEquals(30L, result.getGroups().get(0).getPostId());
        Assertions.assertEquals(List.of(5L, 6L),
                result.getGroups().get(0).getInquiries().stream().map(InquirySummary::getId).toList());
        Assertions.assertEquals("seller", result.getGroups().get(0).getSellerUsername());
    }

    @Test
    public void testFindSentGroupedByPostWhenPostsWereDeletedReturnsOneGroupPerAlbumAndSeller() {
        // 1. Arrange
        // Mismo titulo, artista y vendedor pero otro album (distinto anio): son dos vinilos.
        final InquirySummary original = new InquirySummary(INQUIRY_ID, null, 1L, BUYER_ID, SELLER_ID,
                BUYER_USERNAME, null, null, "seller", PaymentInfo.NONE, "Versus", "IKV", null, null, null,
                InquiryStatus.REJECTED, null, null, false, null, null);
        final InquirySummary reissue = new InquirySummary(10L, null, 2L, BUYER_ID, SELLER_ID,
                BUYER_USERNAME, null, null, "seller", PaymentInfo.NONE, "Versus", "IKV", null, null, null,
                InquiryStatus.REJECTED, null, null, false, null, null);
        Mockito.when(inquiryDao.countGroupsByBuyerId(BUYER_ID, ALL_STATUSES)).thenReturn(2);
        Mockito.when(inquiryDao.findByBuyerId(BUYER_ID, ALL_STATUSES, 5, 0)).thenReturn(List.of(original, reissue));

        // 2. Exercise
        final InquiryPage result = inquiryService.findSentGroupedByPost(BUYER_ID, null, 1);

        // 3. Assert
        Assertions.assertEquals(2, result.getGroups().size());
        Assertions.assertTrue(result.getGroups().get(0).isPostDeleted());
        Assertions.assertEquals(1L, result.getGroups().get(0).getAlbumId());
        Assertions.assertEquals(2L, result.getGroups().get(1).getAlbumId());
        Assertions.assertEquals(List.of(INQUIRY_ID), result.getGroups().get(0).getInquiries().stream()
                .map(InquirySummary::getId).toList());
        Assertions.assertEquals(List.of(10L), result.getGroups().get(1).getInquiries().stream()
                .map(InquirySummary::getId).toList());
    }

    private void stubLock() {
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(InquiryStatus.PENDING, false, null, "vende.discos")));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.AVAILABLE));
    }

    private void confirmedSale() {
        Mockito.when(inquiryDao.findByIdForUpdate(INQUIRY_ID)).thenReturn(Optional.of(
                new Inquiry(INQUIRY_ID, POST_ID, BUYER_ID, InquiryStatus.ACCEPTED)));
        Mockito.when(inquiryDao.findPartiesById(INQUIRY_ID)).thenReturn(Optional.of(
                new InquiryParties(BUYER_ID, SELLER_ID)));
    }

    private static Review review(final long authorId, final long subjectId, final int rating) {
        return new Review(1, INQUIRY_ID, authorId, subjectId, "reviewer", null, rating, null, true,
                LocalDateTime.of(2026, 3, 12, 10, 0));
    }

    private static InquirySummary sale(final InquiryStatus status, final boolean hasReceipt,
                                       final String sellerCbu, final String sellerAlias) {
        return new InquirySummary(INQUIRY_ID, POST_ID, 3L, BUYER_ID, SELLER_ID, BUYER_USERNAME, BUYER_EMAIL,
                "en", "seller", new PaymentInfo(sellerCbu, sellerAlias), "Versus", "IKV", null, 45000, null, status,
                PostStatus.RESERVED, null, hasReceipt, null, null);
    }

    private void stubSale(final InquiryStatus status, final boolean hasReceipt) {
        Mockito.when(inquiryDao.findSummaryById(INQUIRY_ID))
                .thenReturn(Optional.of(sale(status, hasReceipt, "2850590940090418135201", null)));
        Mockito.when(postService.lockById(POST_ID)).thenReturn(post(SELLER_ID, PostStatus.RESERVED));
    }

    private static void commitTransaction() {
        for (final TransactionSynchronization synchronization : TransactionSynchronizationManager.getSynchronizations()) {
            synchronization.afterCommit();
        }
    }

    // El publicante viaja dentro del summary: correo e idioma salen del mismo JOIN.
    private static PostSummary post(final long sellerId, final PostStatus status) {
        return new PostSummary(POST_ID, sellerId, SELLER_EMAIL, SELLER_LOCALE, 3, "Versus", "IKV", 1997,
                null, null, 45000, null, Condition.USED, null, null, status);
    }

    private static Inquiry inquiry() {
        return inquiry(INQUIRY_ID, POST_ID);
    }

    private static Inquiry inquiry(final long inquiryId, final long postId) {
        return new Inquiry(inquiryId, postId, BUYER_ID, InquiryStatus.PENDING);
    }

    private static PostSummary post(final long postId, final long sellerId, final String title) {
        return new PostSummary(postId, sellerId, SELLER_EMAIL, SELLER_LOCALE, 3, title, "IKV", 1997,
                null, null, 45000, null, Condition.USED, null, null, PostStatus.AVAILABLE);
    }

    private static Message message(final long senderId, final String body) {
        return new Message(30L, INQUIRY_ID, senderId, body, LocalDateTime.of(2026, 3, 2, 10, 0));
    }

    private static InquirySummary pendingOnAvailablePost() {
        return new InquirySummary(INQUIRY_ID, POST_ID, 3L, BUYER_ID, SELLER_ID, BUYER_USERNAME, BUYER_EMAIL,
                "en", "seller", PaymentInfo.NONE, "Versus", "IKV", null, 45000, null, InquiryStatus.PENDING,
                PostStatus.AVAILABLE, null, false, null, null);
    }

    private static InquirySummary summary(final long inquiryId, final long postId, final InquiryStatus status) {
        return new InquirySummary(inquiryId, postId, 1L, BUYER_ID, SELLER_ID, BUYER_USERNAME, null, null,
                "seller", PaymentInfo.NONE, "Versus", "IKV", null, null, null, status, PostStatus.AVAILABLE, null,
                false, null, null);
    }

    private static User seller(final String alias) {
        return new User(SELLER_ID, "seller", SELLER_EMAIL, "hash", UserRole.USER, true, SELLER_LOCALE, new PaymentInfo(null, alias));
    }

    private static User buyer() {
        return new User(BUYER_ID, BUYER_USERNAME, BUYER_EMAIL, "hash", UserRole.USER, true, "en");
    }

    private static final class CapturingEmailService implements EmailService {
        private PostInterestNotification notification;
        private Locale locale;
        private final List<InquiryUpdateNotification> updates = new ArrayList<>();
        private final List<Locale> updateLocales = new ArrayList<>();
        private final List<MessageNotification> messages = new ArrayList<>();
        private final List<Locale> messageLocales = new ArrayList<>();

        @Override public void sendWelcomeEmail(final User user, final Locale locale) { }
        @Override public void sendVerificationEmail(final User user, final String token, final Locale locale) { }
        @Override public void sendPasswordChangedEmail(final User user, final Locale locale) { }

        @Override public void sendPasswordResetEmail(final User user, final String token,
                                                     final Locale locale) { }

        @Override
        public void sendPostInterestEmail(final PostInterestNotification notification, final Locale locale) {
            this.notification = notification;
            this.locale = locale;
        }

        @Override
        public void sendInquiryUpdateEmail(final InquiryUpdateNotification notification, final Locale locale) {
            this.updates.add(notification);
            this.updateLocales.add(locale);
        }

        @Override
        public void sendMessageEmail(final MessageNotification notification, final Locale locale) {
            this.messages.add(notification);
            this.messageLocales.add(locale);
        }
    }
}
```
