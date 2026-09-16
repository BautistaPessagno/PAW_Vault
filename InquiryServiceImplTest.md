---
title: "InquiryServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java"]
---

# InquiryServiceImplTest

Service tests with mocks or a capturing mail sender. Direct construction does not activate transaction or async proxies. Source evidence for [[InquiryServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindContactablePostWhenPostIsAvailableReturnsPost`
- `testFindContactablePostWhenPostDoesNotExistReturnsPostNotFoundException`
- `testFindContactablePostWhenPostIsSoldReturnsPostUnavailableException`
- `testFindContactablePostWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenMessageHasSurroundingSpacesReturnsInquiryNotifiedInPublisherLocale`
- `testSubmitWhenMessageIsBlankReturnsInquiryWithoutMessage`
- `testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException`
- `testSubmitWhenPostIsSoldReturnsPostUnavailableException`
- `testAcceptWhenSellerOwnsAvailablePostSellsThePostAndClosesTheCompetitors`
- `testAcceptWhenUserDoesNotOwnPostReturnsForbiddenOperationException`
- `testAcceptWhenPostIsNoLongerAvailableReturnsInvalidInquiryStateException`
- `testAcceptWhenInquiryIsNoLongerPendingReturnsInvalidInquiryStateException`
- `testRejectWhenSellerOwnsPostClosesTheInquiry`
- `testRejectWhenInquiryIsNotPendingReturnsInvalidInquiryStateException`

## Connections

Project types referenced: [[Condition]], [[EmailService]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryDao]], [[InquiryServiceImpl]], [[InvalidInquiryStateException]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[User]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java, lines 1–270](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PostDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

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

    private CapturingEmailService emailService;

    private InquiryServiceImpl inquiryService;

    @BeforeEach
    public void setUp() {
        emailService = new CapturingEmailService();
        inquiryService = new InquiryServiceImpl(inquiryDao, postDao, emailService);
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
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, expected.getMessage())).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, BUYER_USERNAME, BUYER_EMAIL,
                "  Quiero negociar el precio  ");

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertEquals(SELLER_EMAIL, emailService.notification.getPublisherEmail());
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
        Mockito.when(inquiryDao.create(POST_ID, BUYER_ID, null)).thenReturn(expected);

        // 2. Exercise
        final Inquiry result = inquiryService.submit(POST_ID, BUYER_ID, BUYER_USERNAME, BUYER_EMAIL, "   ");

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertNull(emailService.notification.getMessage());
    }

    @Test
    public void testSubmitWhenBuyerOwnsPostReturnsForbiddenOperationException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(BUYER_ID, PostStatus.AVAILABLE)));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, BUYER_USERNAME, BUYER_EMAIL, null);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, submit);
    }

    @Test
    public void testSubmitWhenPostIsSoldReturnsPostUnavailableException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.SOLD)));

        // 2. Exercise
        final Executable submit = () -> inquiryService.submit(POST_ID, BUYER_ID, BUYER_USERNAME, BUYER_EMAIL, null);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, submit);
    }

    @Test
    public void testAcceptWhenSellerOwnsAvailablePostSellsThePostAndClosesTheCompetitors() {
        // 1. Arrange
        stubLock();
        Mockito.when(postDao.markSoldIfAvailable(POST_ID)).thenReturn(true);
        Mockito.when(inquiryDao.acceptPending(INQUIRY_ID)).thenReturn(true);
        Mockito.when(inquiryDao.rejectOtherPending(POST_ID, INQUIRY_ID)).thenReturn(2);

        // 2. Exercise
        final Executable accept = () -> inquiryService.accept(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertDoesNotThrow(accept);
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
        final Executable reject = () -> inquiryService.reject(INQUIRY_ID, SELLER_ID);

        // 3. Assert
        Assertions.assertDoesNotThrow(reject);
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

    private void stubLock() {
        Mockito.when(inquiryDao.findById(INQUIRY_ID)).thenReturn(Optional.of(inquiry(null)));
        Mockito.when(postDao.findByIdForUpdate(POST_ID))
                .thenReturn(Optional.of(post(SELLER_ID, PostStatus.AVAILABLE)));
    }

    // El publicante viaja dentro del summary: correo e idioma salen del mismo JOIN.
    private static PostSummary post(final long sellerId, final PostStatus status) {
        return new PostSummary(POST_ID, sellerId, SELLER_EMAIL, SELLER_LOCALE, 3, "Versus", "IKV", 1997,
                null, null, 45000, null, Condition.USED, null, null, status);
    }

    private static Inquiry inquiry(final String message) {
        return new Inquiry(INQUIRY_ID, POST_ID, BUYER_ID, message);
    }

    private static final class CapturingEmailService implements EmailService {
        private PostInterestNotification notification;
        private Locale locale;

        @Override public void sendWelcomeEmail(final User user, final Locale locale) { }
        @Override public void sendVerificationEmail(final User user, final String token, final Locale locale) { }

        @Override
        public void sendPostInterestEmail(final PostInterestNotification notification, final Locale locale) {
            this.notification = notification;
            this.locale = locale;
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
