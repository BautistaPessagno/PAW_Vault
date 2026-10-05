---
title: "InquiryServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java"]
---

# InquiryServiceImpl

Consultas, ventas, conversación y reseñas. Contactar bloquea el post; aceptar reserva el post y fija el precio de la venta con `startSale`; cada transición bloquea el post, vuelve a chequear al actor y actualiza con guarda de estado; los avisos salen después del commit en el idioma del destinatario. `submitAll` crea en lote las consultas del carrito. Las bandejas traducen el filtro a estados (sin filtro, todos) y los chips salen de `InquiryStatusFilter.countsFrom`. Ver [[Inquiry and sale flow]], [[Contact flow]], [[Conversation flow]], [[Reviews flow]] y [[Status filters flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `INBOX_PAGE_SIZE`, `inquiryDao`, `messageDao`, `postService`, `userService`, `addressService`, `reviewService`, `emailService`.

Operaciones para localizar en la fuente: `findContactablePost`, `submit`, `submitWithNewAddress`, `lockContactablePost`, `create`, `submitAll`, `interestedPost`, `findPostIdsWithOpenInquiry`, `findOpenInquiryId`, `findSentGroupedByPost`, `findReceivedGroupedByPost`, `statusesOf`, `withAddressForSeller`, `groupByPost`, `PostGroupKey`, `countSentBy`, `countReceivedBy`, `countSentByFilter`, `countReceivedByFilter`, `accept`, `reject`, `uploadReceipt`, `requestNewReceipt`, `confirm`, `cancel`, `findDetail`, `saveReview`, `removeReview`, `lockConfirmedSale`, `sendMessage`, `findReceipt`, `findParties`, `findSaleToResume`, `requireBuyer`, `requireSeller`, `requireParty`, `getSummary`, `lockPost`, `move`, `notifyBuyer`, `notifySeller`, `schedule`, `validateContactable`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[AddressNotFoundException]], [[AddressService]], [[ContactRules]], [[EmailService]], [[FilterCounts]], [[ForbiddenOperationException]], [[Inquiry]], [[InquiryDao]], [[InquiryDetail]], [[InquiryEvent]], [[InquiryGroup]], [[InquiryNotFoundException]], [[InquiryPage]], [[InquiryParties]], [[InquiryService]], [[InquiryStatus]], [[InquiryStatusFilter]], [[InquirySummary]], [[InquiryUpdateNotification]], [[InvalidInquiryStateException]], [[InvalidMessageException]], [[InvalidReceiptException]], [[Message]], [[MessageDao]], [[MessageNotification]], [[MessageRules]], [[MissingPaymentInfoException]], [[OpenInquiryExistsException]], [[Pagination]], [[PostInterestNotification]], [[PostService]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[Province]], [[Receipt]], [[ReceiptNotFoundException]], [[ReceiptRules]], [[Review]], [[ReviewService]], [[SupportedLocales]], [[TransactionCallbacks]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenciado por: [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>), líneas 1–562.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Address;
import ar.edu.itba.paw.models.FilterCounts;
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
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.Receipt;
import ar.edu.itba.paw.models.ReceiptRules;
import ar.edu.itba.paw.models.Review;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.MessageDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

@Service
public class InquiryServiceImpl implements InquiryService {

    private static final Logger LOGGER = LoggerFactory.getLogger(InquiryServiceImpl.class);
    private static final int INBOX_PAGE_SIZE = 5;

    private final InquiryDao inquiryDao;
    private final MessageDao messageDao;
    private final PostService postService;
    private final UserService userService;
    private final AddressService addressService;
    private final ReviewService reviewService;
    private final EmailService emailService;

    @Autowired
    public InquiryServiceImpl(final InquiryDao inquiryDao, final MessageDao messageDao,
                              final PostService postService, final UserService userService,
                              final AddressService addressService, final ReviewService reviewService,
                              final EmailService emailService) {
        this.inquiryDao = inquiryDao;
        this.messageDao = messageDao;
        this.postService = postService;
        this.userService = userService;
        this.addressService = addressService;
        this.reviewService = reviewService;
        this.emailService = emailService;
    }

    @Override
    @Transactional(readOnly = true)
    public PostSummary findContactablePost(final long postId, final long buyerId) {
        final PostSummary post = postService.findById(postId);
        validateContactable(post, buyerId);
        return post;
    }

    @Override
    @Transactional
    public Inquiry submit(final long postId, final long buyerId, final String message, final long addressId) {
        final PostSummary post = lockContactablePost(postId, buyerId);
        // La direccion tiene que ser del comprador y seguir vigente: puede haberla archivado
        // en otra pestania despues de cargar el formulario.
        if (addressService.findActiveOwned(addressId, buyerId).isEmpty()) {
            throw new AddressNotFoundException();
        }
        return create(post, buyerId, message, addressId);
    }

    // El post se valida antes de guardar la direccion: si la consulta no puede entrar, no
    // se escribe nada.
    @Override
    @Transactional
    public Inquiry submitWithNewAddress(final long postId, final long buyerId, final String message,
                                        final String street, final String streetNumber, final String apartment,
                                        final String city, final Province province, final String postalCode,
                                        final String notes) {
        final PostSummary post = lockContactablePost(postId, buyerId);
        final Address address = addressService.create(buyerId, street, streetNumber, apartment, city, province,
                postalCode, notes);
        return create(post, buyerId, message, address.getId());
    }

    // El summary ya trae el correo y el idioma del publicante del mismo JOIN: no hace falta
    // volver a buscar al vendedor para armar el aviso. Se bloquea la fila para que la consulta
    // no entre justo mientras se vende el ejemplar; el mismo bloqueo serializa dos envios del
    // mismo comprador, asi el chequeo de Consulta abierta no deja pasar un duplicado.
    private PostSummary lockContactablePost(final long postId, final long buyerId) {
        final PostSummary post = postService.lockById(postId);
        validateContactable(post, buyerId);
        return post;
    }

    // El texto opcional es el primer Mensaje. No dispara el mail de Mensaje nuevo: ya viaja en
    // el de Consulta nueva.
    private Inquiry create(final PostSummary post, final long buyerId, final String message, final long addressId) {
        final String normalizedMessage = MessageRules.normalize(message);
        if (normalizedMessage != null && !MessageRules.isValid(normalizedMessage)) {
            throw new InvalidMessageException();
        }
        final User buyer = userService.findById(buyerId).orElseThrow(UserNotFoundException::new);
        final Inquiry inquiry = inquiryDao.create(post.getId(), buyerId, addressId, post.getPrice());
        if (normalizedMessage != null) {
            messageDao.create(inquiry.getId(), buyerId, normalizedMessage);
        }

        final PostInterestNotification notification = new PostInterestNotification(post.getPublisherEmail(),
                buyer.getUsername(), normalizedMessage, List.of(interestedPost(post, inquiry)));
        // El idioma sale de la preferencia del publicante y se resuelve aca, antes del envio
        // @Async: del otro lado ya no hay request del que sacarlo.
        final Locale publisherLocale = SupportedLocales.localeOf(post.getPublisherLocale());
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Created inquiry inquiryId={} postId={} buyerId={}", inquiry.getId(), post.getId(), buyerId);
            emailService.sendPostInterestEmail(notification, publisherLocale);
        });
        return inquiry;
    }

    // Los posts llegan bloqueados y validados por CartService; MANDATORY porque sin su
    // transaccion los bloqueos ya se habrian soltado.
    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public List<PostInterestNotification> submitAll(final long buyerId, final long addressId,
                                                    final List<PostSummary> posts) {
        final User buyer = userService.findById(buyerId).orElseThrow(UserNotFoundException::new);
        final Map<Long, Integer> priceByPostId = new LinkedHashMap<>();
        posts.forEach(post -> priceByPostId.put(post.getId(), post.getPrice()));
        final Map<Long, Inquiry> inquiryByPostId = inquiryDao.createAll(buyerId, addressId, priceByPostId);
        // Un correo por Publicante con todos sus vinilos: el orden de llegada se conserva.
        final Map<Long, List<PostInterestNotification.InterestedPost>> postsBySeller = new LinkedHashMap<>();
        final Map<Long, PostSummary> firstPostBySeller = new LinkedHashMap<>();
        for (final PostSummary post : posts) {
            postsBySeller.computeIfAbsent(post.getUserId(), ignored -> new ArrayList<>())
                    .add(interestedPost(post, inquiryByPostId.get(post.getId())));
            firstPostBySeller.putIfAbsent(post.getUserId(), post);
        }
        final List<PostInterestNotification> notifications = new ArrayList<>();
        firstPostBySeller.forEach((sellerId, post) -> {
            final PostInterestNotification notification = new PostInterestNotification(post.getPublisherEmail(),
                    buyer.getUsername(), null, postsBySeller.get(sellerId));
            notifications.add(notification);
            final Locale publisherLocale = SupportedLocales.localeOf(post.getPublisherLocale());
            TransactionCallbacks.afterCommit(() -> emailService.sendPostInterestEmail(notification, publisherLocale));
        });
        LOGGER.info("Created inquiries from cart buyerId={} count={} sellers={}", buyerId, posts.size(),
                notifications.size());
        return List.copyOf(notifications);
    }

    private static PostInterestNotification.InterestedPost interestedPost(final PostSummary post,
                                                                          final Inquiry inquiry) {
        return new PostInterestNotification.InterestedPost(post.getId(), inquiry.getId(), post.getTitle(),
                post.getArtistName(), post.getReleaseYear());
    }

    @Override
    @Transactional(readOnly = true)
    public Set<Long> findPostIdsWithOpenInquiry(final long buyerId, final Collection<Long> postIds) {
        return inquiryDao.findPostIdsWithOpenInquiry(buyerId, postIds);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Long> findOpenInquiryId(final long postId, final long buyerId) {
        return inquiryDao.findOpenIdByPostAndBuyer(postId, buyerId);
    }

    @Override
    @Transactional(readOnly = true)
    public InquiryPage findSentGroupedByPost(final long buyerId, final InquiryStatusFilter filter,
                                             final int pageNumber) {
        final List<InquiryStatus> statuses = statusesOf(filter);
        final int totalPages = Pagination.pagesFor(inquiryDao.countGroupsByBuyerId(buyerId, statuses),
                INBOX_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, INBOX_PAGE_SIZE, totalPages);
        return new InquiryPage(groupByPost(inquiryDao.findByBuyerId(buyerId, statuses, INBOX_PAGE_SIZE, offset)),
                pageNumber, totalPages);
    }

    @Override
    @Transactional(readOnly = true)
    public InquiryPage findReceivedGroupedByPost(final long sellerId, final InquiryStatusFilter filter,
                                                 final int pageNumber) {
        final List<InquiryStatus> statuses = statusesOf(filter);
        final int totalPages = Pagination.pagesFor(inquiryDao.countGroupsBySellerId(sellerId, statuses),
                INBOX_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, INBOX_PAGE_SIZE, totalPages);
        final List<InquirySummary> inquiries = inquiryDao.findBySellerId(sellerId, statuses, INBOX_PAGE_SIZE, offset)
                .stream()
                .map(InquiryServiceImpl::withAddressForSeller)
                .toList();
        return new InquiryPage(groupByPost(inquiries), pageNumber, totalPages);
    }

    // Sin filtro, la bandeja muestra las consultas en cualquier estado.
    private static List<InquiryStatus> statusesOf(final InquiryStatusFilter filter) {
        return filter == null ? List.of(InquiryStatus.values()) : filter.getStatuses();
    }

    // Publicar un vinilo no puede servir para juntar domicilios: el vendedor ve la direccion
    // completa solo mientras hay una venta en curso o concretada. Pendiente, rechazada o
    // cancelada, solo sabe a que ciudad y provincia iria el envio.
    private static InquirySummary withAddressForSeller(final InquirySummary inquiry) {
        final Address address = inquiry.getAddress();
        if (address == null || (inquiry.isSale() && inquiry.getStatus() != InquiryStatus.CANCELLED)) {
            return inquiry;
        }
        return inquiry.withAddress(address.withCityAndProvinceOnly());
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
            groups.add(new InquiryGroup(first.getPostId(), first.getAlbumId(), first.getTitle(), first.getArtistName(),
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

    @Override
    @Transactional(readOnly = true)
    public FilterCounts<InquiryStatusFilter> countSentByFilter(final long buyerId) {
        return InquiryStatusFilter.countsFrom(inquiryDao.countByStatusForBuyer(buyerId));
    }

    @Override
    @Transactional(readOnly = true)
    public FilterCounts<InquiryStatusFilter> countReceivedByFilter(final long sellerId) {
        return InquiryStatusFilter.countsFrom(inquiryDao.countByStatusForSeller(sellerId));
    }

    /*
     * Toda transicion bloquea el post antes de escribir: las consultas de un mismo ejemplar
     * compiten por esa unica fila. Cada escritura lleva su guarda de estado; si no encuentra
     * la fila como esperaba, se corta con InvalidInquiryStateException y el rollback deshace
     * lo anterior.
     */
    @Override
    @Transactional
    public Inquiry accept(final long inquiryId, final long sellerId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireSeller(inquiry, sellerId);
        final PostSummary post = lockPost(inquiry);
        // El estado va antes que los datos de cobro: una consulta que ya no se puede aceptar
        // es un conflicto, no un motivo para mandar al Publicante a cargar su CBU.
        if (!inquiry.isPending() || post.getStatus() != PostStatus.AVAILABLE) {
            throw new InvalidInquiryStateException();
        }
        // Los datos de cobro se leen de la fila bloqueada, no del summary: asi no se cruza con
        // un updatePaymentInfo que los este borrando en paralelo.
        final User seller = userService.lockById(sellerId);
        if (!seller.hasPaymentInfo()) {
            throw new MissingPaymentInfoException();
        }
        if (!postService.reserve(post.getId())) {
            throw new InvalidInquiryStateException();
        }
        if (!inquiryDao.startSale(inquiryId, post.getPrice())) {
            throw new InvalidInquiryStateException();
        }
        notifyBuyer(inquiry, post, InquiryEvent.ACCEPTED);
        LOGGER.info("Accepted inquiry inquiryId={} postId={} sellerId={}", inquiryId, post.getId(), sellerId);
        return new Inquiry(inquiryId, inquiry.getPostId(), inquiry.getBuyerId(), InquiryStatus.AWAITING_PAYMENT);
    }

    @Override
    @Transactional
    public Inquiry reject(final long inquiryId, final long sellerId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireSeller(inquiry, sellerId);
        final PostSummary post = lockPost(inquiry);
        move(inquiryId, InquiryStatus.PENDING, InquiryStatus.REJECTED);
        notifyBuyer(inquiry, post, InquiryEvent.REJECTED);
        LOGGER.info("Rejected inquiry inquiryId={} postId={} sellerId={}", inquiryId, post.getId(), sellerId);
        return new Inquiry(inquiryId, inquiry.getPostId(), inquiry.getBuyerId(), InquiryStatus.REJECTED);
    }

    @Override
    @Transactional
    public void uploadReceipt(final long inquiryId, final long buyerId, final String contentType,
                              final byte[] data) {
        final String normalizedType = ReceiptRules.normalizeContentType(contentType);
        if (!ReceiptRules.isValid(normalizedType, data)) {
            LOGGER.warn("Rejected receipt inquiryId={} contentType={} bytes={}", inquiryId, contentType,
                    data == null ? 0 : data.length);
            throw new InvalidReceiptException();
        }
        final InquirySummary inquiry = getSummary(inquiryId);
        requireBuyer(inquiry, buyerId);
        final PostSummary post = lockPost(inquiry);
        if (!inquiryDao.saveReceipt(inquiryId, normalizedType, data)) {
            throw new InvalidInquiryStateException();
        }
        notifySeller(inquiry, post, InquiryEvent.RECEIPT_UPLOADED);
        LOGGER.info("Uploaded receipt inquiryId={} bytes={}", inquiryId, data.length);
    }

    @Override
    @Transactional
    public void requestNewReceipt(final long inquiryId, final long sellerId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireSeller(inquiry, sellerId);
        final PostSummary post = lockPost(inquiry);
        move(inquiryId, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.AWAITING_PAYMENT);
        notifyBuyer(inquiry, post, InquiryEvent.RECEIPT_REQUESTED);
        LOGGER.info("Requested new receipt inquiryId={}", inquiryId);
    }

    // Recien aca se vende el ejemplar y se cierran las consultas que esperaban detras.
    @Override
    @Transactional
    public void confirm(final long inquiryId, final long sellerId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireSeller(inquiry, sellerId);
        final PostSummary post = lockPost(inquiry);
        move(inquiryId, InquiryStatus.PAYMENT_SUBMITTED, InquiryStatus.ACCEPTED);
        if (!postService.markSold(post.getId())) {
            throw new InvalidInquiryStateException();
        }
        final List<InquirySummary> waiting = inquiryDao.findPendingByPostId(post.getId());
        final int rejected = inquiryDao.rejectOtherPending(post.getId(), inquiryId);
        notifyBuyer(inquiry, post, InquiryEvent.CONFIRMED);
        notifySeller(inquiry, post, InquiryEvent.CONFIRMED);
        waiting.forEach(other -> notifyBuyer(other, post, InquiryEvent.REJECTED));
        LOGGER.info("Confirmed sale inquiryId={} postId={} rejectedCompeting={}", inquiryId, post.getId(), rejected);
    }

    @Override
    @Transactional
    public void cancel(final long inquiryId, final long userId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireParty(inquiry, userId);
        final PostSummary post = lockPost(inquiry);
        final boolean bySeller = inquiry.getSellerId() == userId;
        if (!inquiry.isCancellableBy(bySeller)) {
            throw new InvalidInquiryStateException();
        }
        move(inquiryId, inquiry.getStatus(), InquiryStatus.CANCELLED);
        if (!postService.release(post.getId())) {
            throw new InvalidInquiryStateException();
        }
        if (bySeller) {
            notifyBuyer(inquiry, post, InquiryEvent.CANCELLED);
        } else {
            notifySeller(inquiry, post, InquiryEvent.CANCELLED);
        }
        LOGGER.info("Cancelled sale inquiryId={} postId={} bySeller={}", inquiryId, post.getId(), bySeller);
    }

    @Override
    @Transactional(readOnly = true)
    public InquiryDetail findDetail(final long inquiryId, final long viewerId) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireParty(inquiry, viewerId);
        final boolean sellerView = inquiry.getSellerId() == viewerId;
        // La pagina existe en cualquier estado: la direccion sigue la misma regla que la bandeja.
        final InquiryDetail detail = new InquiryDetail(sellerView ? withAddressForSeller(inquiry) : inquiry,
                sellerView, viewerId, messageDao.findByInquiryId(inquiryId));
        return detail.isCanReview()
                ? detail.withOwnReview(reviewService.findActive(inquiryId, viewerId).orElse(null))
                : detail;
    }

    @Override
    @Transactional
    public Review saveReview(final long inquiryId, final long authorId, final int rating, final String body) {
        final long subjectId = lockConfirmedSale(inquiryId, authorId);
        return reviewService.save(inquiryId, authorId, subjectId, rating, body);
    }

    // Un segundo POST (doble clic) no encuentra nada que quitar: no es un error.
    @Override
    @Transactional
    public boolean removeReview(final long inquiryId, final long authorId) {
        lockConfirmedSale(inquiryId, authorId);
        return reviewService.remove(inquiryId, authorId);
    }

    /*
     * Bloquea la consulta para que dos guardados o quitados de la misma parte se ordenen entre si.
     * Solo las partes de una venta confirmada se califican, y cada una a la otra: devuelve a
     * quien califica el autor.
     */
    private long lockConfirmedSale(final long inquiryId, final long authorId) {
        final Inquiry inquiry = inquiryDao.findByIdForUpdate(inquiryId).orElseThrow(InquiryNotFoundException::new);
        final InquiryParties parties = inquiryDao.findPartiesById(inquiryId)
                .orElseThrow(InquiryNotFoundException::new);
        if (!parties.isParty(authorId)) {
            throw new ForbiddenOperationException();
        }
        if (inquiry.getStatus() != InquiryStatus.ACCEPTED) {
            throw new InvalidInquiryStateException();
        }
        return parties.isBuyer(authorId) ? parties.getSellerId() : parties.getBuyerId();
    }

    /*
     * Escribir no es una transicion de estado: no bloquea el post. Si la Consulta se rechaza en
     * el mismo instante, el Mensaje puede entrar igual; es un riesgo aceptado. Toda Conversacion
     * abierta tiene un post vivo, de donde salen el correo y el idioma del Publicante.
     */
    @Override
    @Transactional
    public Message sendMessage(final long inquiryId, final long senderId, final String body) {
        final InquirySummary inquiry = getSummary(inquiryId);
        requireParty(inquiry, senderId);
        if (!inquiry.isConversationOpen() || inquiry.isPostDeleted()) {
            throw new InvalidInquiryStateException();
        }
        final String normalizedBody = MessageRules.normalize(body);
        if (!MessageRules.isValid(normalizedBody)) {
            throw new InvalidMessageException();
        }
        final Message message = messageDao.create(inquiryId, senderId, normalizedBody);

        final PostSummary post = postService.findById(inquiry.getPostId());
        final boolean bySeller = inquiry.getSellerId() == senderId;
        final String recipientEmail = bySeller ? inquiry.getBuyerEmail() : post.getPublisherEmail();
        final Locale recipientLocale = SupportedLocales.localeOf(
                bySeller ? inquiry.getBuyerLocale() : post.getPublisherLocale());
        final MessageNotification notification = new MessageNotification(inquiryId, recipientEmail,
                bySeller ? inquiry.getSellerUsername() : inquiry.getBuyerUsername(), normalizedBody,
                post.getTitle(), post.getArtistName(), post.getReleaseYear());
        TransactionCallbacks.afterCommit(() -> emailService.sendMessageEmail(notification, recipientLocale));
        LOGGER.info("Sent message inquiryId={} messageId={} bySeller={}", inquiryId, message.getId(), bySeller);
        return message;
    }

    @Override
    @Transactional(readOnly = true)
    public Receipt findReceipt(final long inquiryId, final long viewerId) {
        final InquiryParties parties = inquiryDao.findPartiesById(inquiryId).orElseThrow(InquiryNotFoundException::new);
        if (!parties.isParty(viewerId)) {
            throw new ForbiddenOperationException();
        }
        return inquiryDao.findReceipt(inquiryId).orElseThrow(ReceiptNotFoundException::new);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<InquiryParties> findParties(final long inquiryId) {
        return inquiryDao.findPartiesById(inquiryId);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Long> findSaleToResume(final long inquiryId, final long sellerId) {
        return inquiryDao.findPartiesById(inquiryId).filter(parties -> parties.isSeller(sellerId))
                .map(parties -> inquiryId);
    }

    private static void requireBuyer(final InquirySummary inquiry, final long userId) {
        if (inquiry.getBuyerId() != userId) {
            throw new ForbiddenOperationException();
        }
    }

    private static void requireSeller(final InquirySummary inquiry, final long userId) {
        if (inquiry.getSellerId() != userId) {
            throw new ForbiddenOperationException();
        }
    }

    private static void requireParty(final InquirySummary inquiry, final long userId) {
        if (inquiry.getBuyerId() != userId && inquiry.getSellerId() != userId) {
            throw new ForbiddenOperationException();
        }
    }

    private InquirySummary getSummary(final long inquiryId) {
        return inquiryDao.findSummaryById(inquiryId).orElseThrow(InquiryNotFoundException::new);
    }

    private PostSummary lockPost(final InquirySummary inquiry) {
        if (inquiry.isPostDeleted()) {
            throw new InvalidInquiryStateException();
        }
        return postService.lockById(inquiry.getPostId());
    }

    private void move(final long inquiryId, final InquiryStatus from, final InquiryStatus to) {
        if (!inquiryDao.updateStatus(inquiryId, from, to)) {
            throw new InvalidInquiryStateException();
        }
    }

    // El idioma de cada destinatario se resuelve aca, antes del envio @Async.
    private void notifyBuyer(final InquirySummary inquiry, final PostSummary post, final InquiryEvent event) {
        schedule(new InquiryUpdateNotification(event, inquiry.getId(), inquiry.getBuyerEmail(), post.getTitle(),
                post.getArtistName(), post.getReleaseYear()), SupportedLocales.localeOf(inquiry.getBuyerLocale()));
    }

    private void notifySeller(final InquirySummary inquiry, final PostSummary post, final InquiryEvent event) {
        schedule(new InquiryUpdateNotification(event, inquiry.getId(), post.getPublisherEmail(), post.getTitle(),
                post.getArtistName(), post.getReleaseYear()), SupportedLocales.localeOf(post.getPublisherLocale()));
    }

    private void schedule(final InquiryUpdateNotification notification, final Locale locale) {
        TransactionCallbacks.afterCommit(() -> emailService.sendInquiryUpdateEmail(notification, locale));
    }

    // Un comprador tiene a lo sumo una Consulta abierta por post: si ya la tiene, va a esa
    // Conversacion.
    private void validateContactable(final PostSummary post, final long buyerId) {
        final Optional<Long> openId = inquiryDao.findOpenIdByPostAndBuyer(post.getId(), buyerId);
        switch (ContactRules.stateOf(post.getStatus(), post.getUserId(), buyerId, openId.isPresent())) {
            case OPEN_INQUIRY -> throw new OpenInquiryExistsException(openId.orElseThrow());
            case UNAVAILABLE -> throw new PostUnavailableException();
            case OWN_POST -> throw new ForbiddenOperationException();
            case CONTACTABLE -> { }
        }
    }
}
```
