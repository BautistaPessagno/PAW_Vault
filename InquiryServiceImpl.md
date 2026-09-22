---
title: "InquiryServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java"]
---

# InquiryServiceImpl

Submission locks the post, rejects SOLD posts and self-contact, normalizes the optional message and stores the inquiry; the interest mail in the seller's preferred locale is registered to run after commit. Inbox reads page by publication, five groups per page, and regroup DAO rows in a LinkedHashMap keyed by post, album and seller. Accept and reject refuse inquiries whose post was deleted, lock the publication and check ownership. Accept marks it SOLD, accepts the chosen inquiry, rejects competitors and schedules the buyer's acceptance mail after commit.

## Connections

Project types referenced: [[EmailService]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryAcceptedNotification]], [[InquiryDao]], [[InquiryGroup]], [[InquiryNotFoundException]], [[InquiryPage]], [[InquiryService]], [[InquiryStatus]], [[InquirySummary]], [[InvalidInquiryStateException]], [[Pagination]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[SupportedLocales]], [[TransactionCallbacks]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenced by: [[InquiryServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java, lines 1–219](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryGroup;
import ar.edu.itba.paw.models.InquiryPage;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PostDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

@Service
public class InquiryServiceImpl implements InquiryService {

    private static final Logger LOGGER = LoggerFactory.getLogger(InquiryServiceImpl.class);
    private static final int INBOX_PAGE_SIZE = 5;

    private final InquiryDao inquiryDao;
    private final PostDao postDao;
    private final UserService userService;
    private final EmailService emailService;

    @Autowired
    public InquiryServiceImpl(final InquiryDao inquiryDao, final PostDao postDao,
                              final UserService userService, final EmailService emailService) {
        this.inquiryDao = inquiryDao;
        this.postDao = postDao;
        this.userService = userService;
        this.emailService = emailService;
    }

    @Override
    @Transactional(readOnly = true)
    public PostSummary findContactablePost(final long postId, final long buyerId) {
        final PostSummary post = postDao.findById(postId).orElseThrow(PostNotFoundException::new);
        validateContactable(post, buyerId);
        return post;
    }

    @Override
    @Transactional
    public Inquiry submit(final long postId, final long buyerId, final String message) {
        // El summary ya trae el correo y el idioma del publicante del mismo JOIN: no hace
        // falta volver a buscar al vendedor para armar el aviso. Se bloquea la fila para que
        // la consulta no entre justo mientras se vende el ejemplar.
        final PostSummary post = postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new);
        validateContactable(post, buyerId);
        final User buyer = userService.findById(buyerId).orElseThrow(UserNotFoundException::new);
        final String normalizedMessage = normalizeMessage(message);
        final Inquiry inquiry = inquiryDao.create(postId, buyerId, normalizedMessage);

        final PostInterestNotification notification = new PostInterestNotification(
                post.getId(), post.getPublisherEmail(), buyer.getUsername(), buyer.getEmail(),
                normalizedMessage, post.getTitle(), post.getArtistName(), post.getReleaseYear());
        // El idioma sale de la preferencia del publicante y se resuelve aca, antes del envio
        // @Async: del otro lado ya no hay request del que sacarlo.
        final Locale publisherLocale = SupportedLocales.localeOf(post.getPublisherLocale());
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Created inquiry inquiryId={} postId={} buyerId={}", inquiry.getId(), postId, buyerId);
            emailService.sendPostInterestEmail(notification, publisherLocale);
        });
        return inquiry;
    }

    @Override
    @Transactional(readOnly = true)
    public InquiryPage findSentGroupedByPost(final long buyerId, final int pageNumber) {
        final int totalPages = Pagination.pagesFor(inquiryDao.countGroupsByBuyerId(buyerId), INBOX_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, INBOX_PAGE_SIZE, totalPages);
        return new InquiryPage(groupByPost(inquiryDao.findByBuyerId(buyerId, INBOX_PAGE_SIZE, offset)),
                pageNumber, totalPages);
    }

    @Override
    @Transactional(readOnly = true)
    public InquiryPage findReceivedGroupedByPost(final long sellerId, final int pageNumber) {
        final int totalPages = Pagination.pagesFor(inquiryDao.countGroupsBySellerId(sellerId), INBOX_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, INBOX_PAGE_SIZE, totalPages);
        return new InquiryPage(groupByPost(inquiryDao.findBySellerId(sellerId, INBOX_PAGE_SIZE, offset)),
                pageNumber, totalPages);
    }

    /*
     * Los dos listados vienen ordenados por consulta, de la mas nueva a la mas vieja. El
     * LinkedHashMap conserva ese orden: los grupos salen ordenados por su consulta mas
     * nueva, y los datos de la publicacion se toman de la primera del grupo porque son
     * los mismos para todas. Las consultas de publicaciones eliminadas ya no tienen id de
     * post: las agrupa el album y el vendedor que conservan.
     */
    private static List<InquiryGroup> groupByPost(final List<InquirySummary> inquiries) {
        final Map<PostGroupKey, List<InquirySummary>> inquiriesByPost = new LinkedHashMap<>();
        for (final InquirySummary inquiry : inquiries) {
            final PostGroupKey key = new PostGroupKey(inquiry.getPostId(), inquiry.getAlbumId(),
                    inquiry.getSellerId());
            inquiriesByPost.computeIfAbsent(key, ignored -> new ArrayList<>()).add(inquiry);
        }

        final List<InquiryGroup> groups = new ArrayList<>();
        for (final List<InquirySummary> grouped : inquiriesByPost.values()) {
            final InquirySummary first = grouped.get(0);
            groups.add(new InquiryGroup(first.getPostId(), first.getTitle(), first.getArtistName(),
                    first.getSellerUsername(), first.getCoverImageId(), first.getPostStatus(), grouped));
        }
        return List.copyOf(groups);
    }

    // Clave de agrupacion de la bandeja: el id del post distingue una publicacion viva de
    // una eliminada del mismo album y vendedor; entre eliminadas, los alcanza album y vendedor.
    private record PostGroupKey(Long postId, long albumId, long sellerId) { }

    @Override
    @Transactional(readOnly = true)
    public int countSentBy(final long buyerId) {
        return inquiryDao.countByBuyerId(buyerId);
    }

    @Override
    @Transactional(readOnly = true)
    public int countReceivedBy(final long sellerId) {
        return inquiryDao.countBySellerId(sellerId);
    }

    /*
     * Cada escritura es una sentencia con su propia guarda: si alguna no encuentra la fila
     * en el estado esperado se corta ahi, sin depender de que el rollback deshaga la anterior.
     */
    @Override
    @Transactional
    public Inquiry accept(final long inquiryId, final long sellerId) {
        final Inquiry inquiry = getInquiry(inquiryId);
        final PostSummary post = lockPostForSeller(inquiry, sellerId);
        if (!postDao.markSoldIfAvailable(post.getId())) {
            throw new InvalidInquiryStateException();
        }
        if (!inquiryDao.acceptPending(inquiryId)) {
            throw new InvalidInquiryStateException();
        }
        final int rejected = inquiryDao.rejectOtherPending(post.getId(), inquiryId);
        scheduleInquiryAcceptedEmail(inquiry, post);
        LOGGER.info("Accepted inquiry inquiryId={} postId={} sellerId={} rejectedCompeting={}",
                inquiryId, post.getId(), sellerId, rejected);
        return withStatus(inquiry, InquiryStatus.ACCEPTED);
    }

    @Override
    @Transactional
    public Inquiry reject(final long inquiryId, final long sellerId) {
        final Inquiry inquiry = getInquiry(inquiryId);
        final PostSummary post = lockPostForSeller(inquiry, sellerId);
        if (!inquiryDao.rejectPending(inquiryId)) {
            throw new InvalidInquiryStateException();
        }
        LOGGER.info("Rejected inquiry inquiryId={} postId={} sellerId={}", inquiryId, post.getId(), sellerId);
        return withStatus(inquiry, InquiryStatus.REJECTED);
    }

    /*
     * Aceptar y rechazar bloquean la publicacion antes de escribir: las consultas de un
     * mismo ejemplar compiten por esa unica fila y se ordenan entre si.
     */
    private PostSummary lockPostForSeller(final Inquiry inquiry, final long sellerId) {
        if (inquiry.isPostDeleted()) {
            throw new InvalidInquiryStateException();
        }
        final PostSummary post = postDao.findByIdForUpdate(inquiry.getPostId())
                .orElseThrow(PostNotFoundException::new);
        if (post.getUserId() != sellerId) {
            throw new ForbiddenOperationException();
        }
        return post;
    }

    private Inquiry getInquiry(final long inquiryId) {
        return inquiryDao.findById(inquiryId).orElseThrow(InquiryNotFoundException::new);
    }

    private static Inquiry withStatus(final Inquiry inquiry, final InquiryStatus status) {
        return new Inquiry(inquiry.getId(), inquiry.getPostId(), inquiry.getBuyerId(), inquiry.getMessage(), status);
    }

    private void scheduleInquiryAcceptedEmail(final Inquiry inquiry, final PostSummary post) {
        final User buyer = userService.findById(inquiry.getBuyerId()).orElseThrow(UserNotFoundException::new);
        final InquiryAcceptedNotification notification = new InquiryAcceptedNotification(inquiry.getId(),
                buyer.getEmail(), post.getTitle(), post.getArtistName(), post.getReleaseYear());
        final Locale locale = SupportedLocales.localeOf(buyer.getPreferredLocale());
        TransactionCallbacks.afterCommit(() -> emailService.sendInquiryAcceptedEmail(notification, locale));
    }

    // El mensaje es opcional: si no trae texto util se guarda en null.
    private static String normalizeMessage(final String message) {
        if (message == null) {
            return null;
        }
        final String trimmed = message.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

    private static void validateContactable(final PostSummary post, final long buyerId) {
        if (post.getStatus() != PostStatus.AVAILABLE) {
            throw new PostUnavailableException();
        }
        if (post.getUserId() == buyerId) {
            throw new ForbiddenOperationException();
        }
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
