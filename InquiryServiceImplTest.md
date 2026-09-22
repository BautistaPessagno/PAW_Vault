---
title: "InquiryServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java"]
---

# InquiryServiceImplTest

Service tests with mocks and a capturing mail service. The fixture initializes TransactionSynchronizationManager by hand and runs registered after-commit callbacks explicitly; direct construction still does not activate real transaction or async proxies. Source evidence for [[InquiryServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindContactablePostWhenPostIsAvailableReturnsPost`
- `testFindContactablePostWhenPostDoesNotExistReturnsPostNotFoundException`
- `testFindContactablePostWhenPostIsSoldReturnsPostUnavailableException`
- `testFindContactablePostWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenMessageHasSurroundingSpacesReturnsInquiryNotifiedInPublisherLocale`
- `testSubmitWhenMessageIsBlankReturnsInquiryWithoutMessage`
- `testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenPostIsSoldReturnsPostUnavailableException`
- `testAcceptWhenSellerOwnsAvailablePostSchedulesNotificationAfterCommit`
- `testAcceptWhenUserDoesNotOwnPostReturnsForbiddenOperationException`
- `testAcceptWhenPostIsNoLongerAvailableReturnsInvalidInquiryStateException`
- `testAcceptWhenInquiryIsNoLongerPendingReturnsInvalidInquiryStateException`
- `testRejectWhenSellerOwnsPostClosesTheInquiry`
- `testRejectWhenInquiryIsNotPendingReturnsInvalidInquiryStateException`
- `testFindReceivedGroupedByPostWhenSecondPageOfSevenGroupsReturnsGroupedPage`
- `testFindReceivedGroupedByPostWhenPageIsPastTheLastOneReturnsPageNotFoundException`
- `testFindReceivedGroupedByPostWhenPageIsBelowOneReturnsPageNotFoundException`
- `testFindReceivedGroupedByPostWhenSellerHasNoInquiriesReturnsEmptyFirstPage`
- `testFindSentGroupedByPostWhenBuyerRepeatsAPostReturnsOneGroupWithSeller`
- `testFindSentGroupedByPostWhenPostsWereDeletedReturnsOneGroupPerAlbumAndSeller`
- `testAcceptWhenPostWasDeletedThrowsInvalidInquiryStateException`

## Connections

Project types referenced: [[Condition]], [[EmailService]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryAcceptedNotification]], [[InquiryDao]], [[InquiryGroup]], [[InquiryPage]], [[InquiryServiceImpl]], [[InquiryStatus]], [[InquirySummary]], [[InvalidInquiryStateException]], [[PageNotFoundException]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[User]], [[UserRole]], [[UserService]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java, lines 1–448](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryGroup;
import ar.edu.itba.paw.models.InquiryPage;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PostDao;
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

import java.util.List;
import java.util.Locale;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class InquiryServiceImplTest {

    private static final long POST_ID = 7;
    private static final long INQUIRY_ID = 9;
    private static final long SELLER_ID = 1;
    private static final long BUYER_ID = 2;
    private static final String BUYER_USERNAME = "buyer";
    private static final String BUYER_EMAIL = "buyer@example.com";
    private static final String SELLER_EMAIL = "seller@example.com";
    private static final String SELLER_LOCALE = "fr";

    @Mock
    private InquiryDao inquiryDao;

    @Mock
    private PostDao postDao;

    @Mock
    private UserService userService;

    private CapturingEmailService emailService;

    private InquiryServiceImpl inquiryService;

    @BeforeEach
    public void setUp() {
        emailService = new CapturingEmailService();
        inquiryService = new InquiryServiceImpl(inquiryDao, postDao, userService, emailService);
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
        Mockito.when(postDao.findById(POST_ID)).thenReturn(Optional.of(expected));

        // 2. Exercise
        final PostSummary result = inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testFindContactablePostWhenPostDoesNotExistReturnsPostNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.findById(POST_ID)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, find);
    }

    @Test
    public void testFindContactablePostWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postDao.findById(POST_ID)).thenReturn(Optional.of(post(SELLER_ID, PostStatus.SOLD)));

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, find);
    }

    @Test
    public void testFindContactablePostWhenBuyerOwnsPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(postDao.findById(POST_ID)).thenReturn(Optional.of(post(BUYER_ID, PostStatus.AVAILABLE)));

        // 2. Exercise
        final Executable find = () -> inquiryService.findContactablePost(POST_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, find);
    }

    @Test
    public void testSubmitWhenMessageHasSurroundingSpacesReturnsInquiryNotifiedInPublisherLocale() {
        // 1. Arrange
        final Inquiry expected = inquiry("Quiero negociar el precio");
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, expected.getMessage())).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, "  Quiero negociar el precio  ");

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertNull(emailService.notification);
        commitTransaction();
        Assertions.assertEquals(SELLER_EMAIL, emailService.notification.getPublisherEmail());
        Assertions.assertEquals(BUYER_USERNAME, emailService.notification.getContactName());
        Assertions.assertEquals(BUYER_EMAIL, emailService.notification.getContactEmail());
        Assertions.assertEquals("Quiero negociar el precio", emailService.notification.getMessage());
        Assertions.assertEquals(SELLER_LOCALE, emailService.locale.getLanguage());
    }

    @Test
    public void testSubmitWhenMessageIsBlankReturnsInquiryWithoutMessage() {
        // 1. Arrange
        final Inquiry expected = inquiry(null);
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.AVAILABLE)));
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, null)).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, "   ");

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertNull(emailService.notification);
        commitTransaction();
        Assertions.assertNull(emailService.notification.getMessage());
    }

    @Test
    public void testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(BUYER_ID, PostStatus.AVAILABLE)));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, null);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, submit);
    }

    @Test
    public void testSubmitWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.SOLD)));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, null);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, submit);
    }

    @Test
    public void testAcceptWhenSellerOwnsAvailablePostSchedulesNotificationAfterCommit() {
        // 1. Arrange
        stubLock();
        Mockito.when(postDao.markSoldIfAvailable(POST_ID)).thenReturn(true);
        Mockito.when(inquiryDao.acceptPending(INQUIRY_ID)).thenReturn(true);
        Mockito.when(inquiryDao.rejectOtherPending(POST_ID, INQUIRY_ID)).thenReturn(2);
        Mockito.when(userService.findById(BUYER_ID)).thenReturn(Optional.of(buyer()));

        // 2. Exercise
        final Inquiry result = inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertEquals(InquiryStatus.ACCEPTED, result.getStatus());
        Assertions.assertNull(emailService.acceptedNotification);
        commitTransaction();
        Assertions.assertNotNull(emailService.acceptedNotification);
        Assertions.assertEquals(BUYER_EMAIL, emailService.acceptedNotification.getBuyerEmail());
        Assertions.assertEquals("Versus", emailService.acceptedNotification.getAlbumTitle());
        Assertions.assertEquals("en", emailService.acceptedLocale.getLanguage());
    }

    @Test
    public void testAcceptWhenUserDoesNotOwnPostReturnsForbiddenOperationException() {
        // 1. Arrange
        stubLock();

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, BUYER_ID);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, accept);
    }

    @Test
    public void testAcceptWhenPostIsNoLongerAvailableReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubLock();
        Mockito.when(postDao.markSoldIfAvailable(POST_ID)).thenReturn(false);

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    @Test
    public void testAcceptWhenInquiryIsNoLongerPendingReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubLock();
        Mockito.when(postDao.markSoldIfAvailable(POST_ID)).thenReturn(true);
        Mockito.when(inquiryDao.acceptPending(INQUIRY_ID)).thenReturn(false);

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    @Test
    public void testRejectWhenSellerOwnsPostClosesTheInquiry() {
        // 1. Arrange
        stubLock();
        Mockito.when(inquiryDao.rejectPending(INQUIRY_ID)).thenReturn(true);

        // 2. Exercise
        final Inquiry result = inquiryService.reject(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertEquals(InquiryStatus.REJECTED, result.getStatus());
    }

    @Test
    public void testRejectWhenInquiryIsNotPendingReturnsInvalidInquiryStateException() {
        // 1. Arrange
        stubLock();
        Mockito.when(inquiryDao.rejectPending(INQUIRY_ID)).thenReturn(false);

        // 2. Exercise
        final Executable reject = () -> inquiryService.reject(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, reject);
    }

    @Test
    public void testFindReceivedGroupedByPostWhenSecondPageOfSevenGroupsReturnsGroupedPage() {
        // 1. Arrange
        final List<InquirySummary> rows = List.of(
                summary(3, 20, InquiryStatus.PENDING),
                summary(2, 20, InquiryStatus.REJECTED),
                summary(1, 10, InquiryStatus.ACCEPTED));
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID)).thenReturn(7);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, 5, 5)).thenReturn(rows);

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, 2);

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
    public void testFindReceivedGroupedByPostWhenPageIsPastTheLastOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID)).thenReturn(7);

        // 2. Exercise
        final Executable findPage = () -> inquiryService.findReceivedGroupedByPost(SELLER_ID, 3);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindReceivedGroupedByPostWhenPageIsBelowOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID)).thenReturn(7);

        // 2. Exercise
        final Executable findPage = () -> inquiryService.findReceivedGroupedByPost(SELLER_ID, 0);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindReceivedGroupedByPostWhenSellerHasNoInquiriesReturnsEmptyFirstPage() {
        // 1. Arrange
        Mockito.when(inquiryDao.countGroupsBySellerId(SELLER_ID)).thenReturn(0);
        Mockito.when(inquiryDao.findBySellerId(SELLER_ID, 5, 0)).thenReturn(List.of());

        // 2. Exercise
        final InquiryPage result = inquiryService.findReceivedGroupedByPost(SELLER_ID, 1);

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
        Mockito.when(inquiryDao.countGroupsByBuyerId(BUYER_ID)).thenReturn(1);
        Mockito.when(inquiryDao.findByBuyerId(BUYER_ID, 5, 0)).thenReturn(rows);

        // 2. Exercise
        final InquiryPage result = inquiryService.findSentGroupedByPost(BUYER_ID, 1);

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
        final InquirySummary original = new InquirySummary(INQUIRY_ID, null, 1L, SELLER_ID, BUYER_USERNAME,
                "seller", "Versus", "IKV", null, null, InquiryStatus.REJECTED, null);
        final InquirySummary reissue = new InquirySummary(10L, null, 2L, SELLER_ID, BUYER_USERNAME,
                "seller", "Versus", "IKV", null, null, InquiryStatus.REJECTED, null);
        Mockito.when(inquiryDao.countGroupsByBuyerId(BUYER_ID)).thenReturn(2);
        Mockito.when(inquiryDao.findByBuyerId(BUYER_ID, 5, 0)).thenReturn(List.of(original, reissue));

        // 2. Exercise
        final InquiryPage result = inquiryService.findSentGroupedByPost(BUYER_ID, 1);

        // 3. Assert
        Assertions.assertEquals(2, result.getGroups().size());
        Assertions.assertTrue(result.getGroups().get(0).isPostDeleted());
        Assertions.assertEquals(List.of(INQUIRY_ID), result.getGroups().get(0).getInquiries().stream()
                .map(InquirySummary::getId).toList());
        Assertions.assertEquals(List.of(10L), result.getGroups().get(1).getInquiries().stream()
                .map(InquirySummary::getId).toList());
    }

    @Test
    public void testAcceptWhenPostWasDeletedThrowsInvalidInquiryStateException() {
        // 1. Arrange
        Mockito.when(inquiryDao.findById(INQUIRY_ID))
                .thenReturn(Optional.of(new Inquiry(INQUIRY_ID, null, BUYER_ID, null, InquiryStatus.REJECTED)));

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertThrows(InvalidInquiryStateException.class, accept);
    }

    private void stubLock() {
        Mockito.when(inquiryDao.findById(INQUIRY_ID)).thenReturn(Optional.of(inquiry(null)));
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.AVAILABLE)));
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

    private static Inquiry inquiry(final String message) {
        return new Inquiry(INQUIRY_ID, POST_ID, BUYER_ID, message, InquiryStatus.PENDING);
    }

    private static InquirySummary summary(final long inquiryId, final long postId, final InquiryStatus status) {
        return new InquirySummary(inquiryId, postId, 1L, SELLER_ID, BUYER_USERNAME, "seller", "Versus", "IKV",
                null, null, status, PostStatus.AVAILABLE);
    }

    private static User buyer() {
        return new User(BUYER_ID, BUYER_USERNAME, BUYER_EMAIL, "hash", UserRole.USER, true, "en");
    }

    private static final class CapturingEmailService implements EmailService {
        private PostInterestNotification notification;
        private Locale locale;
        private InquiryAcceptedNotification acceptedNotification;
        private Locale acceptedLocale;

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
        public void sendInquiryAcceptedEmail(final InquiryAcceptedNotification notification, final Locale locale) {
            this.acceptedNotification = notification;
            this.acceptedLocale = locale;
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
