---
title: "InquiryServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java"]
---

# InquiryServiceImpl

Submission locks the post, rejects SOLD posts and self-contact, normalizes the optional message, stores the inquiry and requests email using the seller preferred locale. Accept/reject first lock the publication and check seller ownership. Accept marks the available post SOLD, accepts a pending inquiry and rejects competing pending inquiries in one transaction. Failed guarded writes raise InvalidInquiryStateException. Mail submission occurs before commit and has no outbox.

## Connections

Project types referenced: [[EmailService]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryDao]], [[InquiryNotFoundException]], [[InquiryService]], [[InquirySummary]], [[InvalidInquiryStateException]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[SupportedLocales]].

Referenced by: [[InquiryServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java, lines 1–136](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PostDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class InquiryServiceImpl implements InquiryService {

    private static final Logger LOGGER = LoggerFactory.getLogger(InquiryServiceImpl.class);

    private final InquiryDao inquiryDao;
    private final PostDao postDao;
    private final EmailService emailService;

    @Autowired
    public InquiryServiceImpl(final InquiryDao inquiryDao, final PostDao postDao,
                              final EmailService emailService) {
        this.inquiryDao = inquiryDao;
        this.postDao = postDao;
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
    public Inquiry submit(final long postId, final long buyerId, final String buyerUsername,
                          final String buyerEmail, final String message) {
        // El summary ya trae el correo y el idioma del publicante del mismo JOIN: no hace
        // falta volver a buscar al vendedor para armar el aviso. Se bloquea la fila para que
        // la consulta no entre justo mientras se vende el ejemplar.
        final PostSummary post = postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new);
        validateContactable(post, buyerId);
        final String normalizedMessage = normalizeMessage(message);
        final Inquiry inquiry = inquiryDao.create(postId, buyerId, normalizedMessage);
        LOGGER.info("Created inquiry inquiryId={} postId={} buyerId={}", inquiry.getId(), postId, buyerId);

        final PostInterestNotification notification = new PostInterestNotification(
                post.getId(), post.getPublisherEmail(), buyerUsername, buyerEmail, normalizedMessage,
                post.getTitle(), post.getArtistName(), post.getReleaseYear());
        // El idioma sale de la preferencia del publicante y se resuelve aca, antes del envio
        // @Async: del otro lado ya no hay request del que sacarlo.
        emailService.sendPostInterestEmail(notification, SupportedLocales.localeOf(post.getPublisherLocale()));
        return inquiry;
    }

    @Override
    @Transactional(readOnly = true)
    public List<InquirySummary> findSentBy(final long buyerId) {
        return inquiryDao.findByBuyerId(buyerId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<InquirySummary> findReceivedBy(final long sellerId) {
        return inquiryDao.findBySellerId(sellerId);
    }

    /*
     * Cada escritura es una sentencia con su propia guarda: si alguna no encuentra la fila
     * en el estado esperado se corta ahi, sin depender de que el rollback deshaga la anterior.
     */
    @Override
    @Transactional
    public void accept(final long inquiryId, final long sellerId) {
        final long postId = lockPostForSeller(inquiryId, sellerId);
        if (!postDao.markSoldIfAvailable(postId)) {
            throw new InvalidInquiryStateException();
        }
        if (!inquiryDao.acceptPending(inquiryId)) {
            throw new InvalidInquiryStateException();
        }
        final int rejected = inquiryDao.rejectOtherPending(postId, inquiryId);
        LOGGER.info("Accepted inquiry inquiryId={} postId={} sellerId={} rejectedCompeting={}",
                inquiryId, postId, sellerId, rejected);
    }

    @Override
    @Transactional
    public void reject(final long inquiryId, final long sellerId) {
        final long postId = lockPostForSeller(inquiryId, sellerId);
        if (!inquiryDao.rejectPending(inquiryId)) {
            throw new InvalidInquiryStateException();
        }
        LOGGER.info("Rejected inquiry inquiryId={} postId={} sellerId={}", inquiryId, postId, sellerId);
    }

    /*
     * Aceptar y rechazar bloquean la publicacion antes de escribir: las consultas de un
     * mismo ejemplar compiten por esa unica fila y se ordenan entre si.
     */
    private long lockPostForSeller(final long inquiryId, final long sellerId) {
        final Inquiry inquiry = inquiryDao.findById(inquiryId).orElseThrow(InquiryNotFoundException::new);
        final PostSummary post = postDao.findByIdForUpdate(inquiry.getPostId())
                .orElseThrow(PostNotFoundException::new);
        if (post.getUserId() != sellerId) {
            throw new ForbiddenOperationException();
        }
        return post.getId();
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
