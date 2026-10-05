---
title: "InquirySummary"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java"]
---

# InquirySummary

La Consulta como la muestran la bandeja y el detalle: partes con su foto, álbum, precio (el actual del post mientras está pendiente y el fijado al aceptar después; ver ADR 0004), último mensaje, estados de la consulta y del post, dirección y si hay comprobante. Trae las reglas de estado (`isCancellableBy`, `isSale`, `isConversationOpen`). Si el post fue eliminado, el álbum y el vendedor salen de la copia que guarda la consulta.

## Guía de lectura

Datos y dependencias declaradas: `id`, `postId`, `albumId`, `buyerId`, `sellerId`, `buyerUsername`, `buyerEmail`, `buyerLocale`, `sellerUsername`, `sellerPaymentInfo`, `title`, `artistName`, `coverImageId`, `price`, `lastMessage`, `status`, `postStatus`, `address`, `hasReceipt`, `buyerAvatarImageId`, `sellerAvatarImageId`.

Operaciones para localizar en la fuente: `getId`, `getPostId`, `getAlbumId`, `getBuyerId`, `getSellerId`, `getBuyerUsername`, `getBuyerEmail`, `getBuyerLocale`, `getSellerUsername`, `getSellerPaymentInfo`, `getTitle`, `getArtistName`, `getCoverImageId`, `getPrice`, `getLastMessage`, `getStatus`, `getPostStatus`, `getAddress`, `getBuyerAvatarImageId`, `getSellerAvatarImageId`, `isHasReceipt`, `hasSellerPaymentInfo`, `withAddress`, `isPending`, `isPostAvailable`, `isPostDeleted`, `isAwaitingPayment`, `isPaymentSubmitted`, `isCancellableBy`, `isSale`, `isConversationOpen`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Address]], [[InquiryStatus]], [[Message]], [[PaymentInfo]], [[PostStatus]].

Referenciado por: [[InquiryDao]], [[InquiryDetail]], [[InquiryGroup]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java>), líneas 1–115.

```java
package ar.edu.itba.paw.models;

/*
 * Una consulta como la muestra la bandeja: quien la mando, quien la recibio, que album
 * es y en que estado quedaron la consulta y la publicacion. Si la publicacion fue
 * eliminada, postId y postStatus vienen en null y el album y el vendedor salen de la
 * copia que guarda la consulta. albumId y sellerId identifican ese vinilo aunque la
 * publicacion ya no exista.
 */
public final class InquirySummary {
    private final long id;
    private final Long postId;
    private final long albumId;
    private final long buyerId;
    private final long sellerId;
    private final String buyerUsername;
    private final String buyerEmail;
    private final String buyerLocale;
    private final String sellerUsername;
    private final PaymentInfo sellerPaymentInfo;
    private final String title;
    private final String artistName;
    private final Long coverImageId;
    // Precio actual mientras esta pendiente y precio fijado al aceptar. Las consultas legacy
    // conservan el fallback del post; null si no existe ni snapshot ni publicacion.
    private final Integer price;
    // null mientras la Conversacion esta vacia.
    private final Message lastMessage;
    private final InquiryStatus status;
    private final PostStatus postStatus;
    private final Address address;
    private final boolean hasReceipt;
    private final Long buyerAvatarImageId;
    private final Long sellerAvatarImageId;

    public InquirySummary(final long id, final Long postId, final long albumId, final long buyerId,
                          final long sellerId, final String buyerUsername, final String buyerEmail,
                          final String buyerLocale, final String sellerUsername,
                          final PaymentInfo sellerPaymentInfo, final String title, final String artistName,
                          final Long coverImageId, final Integer price, final Message lastMessage,
                          final InquiryStatus status, final PostStatus postStatus,
                          // null en las consultas anteriores a la direccion de envio.
                          final Address address, final boolean hasReceipt,
                          // null si la Cuenta no tiene foto o no esta verificada.
                          final Long buyerAvatarImageId, final Long sellerAvatarImageId) {
        this.id = id;
        this.postId = postId;
        this.albumId = albumId;
        this.buyerId = buyerId;
        this.sellerId = sellerId;
        this.buyerUsername = buyerUsername;
        this.buyerEmail = buyerEmail;
        this.buyerLocale = buyerLocale;
        this.sellerUsername = sellerUsername;
        this.sellerPaymentInfo = sellerPaymentInfo;
        this.title = title;
        this.artistName = artistName;
        this.coverImageId = coverImageId;
        this.price = price;
        this.lastMessage = lastMessage;
        this.status = status;
        this.postStatus = postStatus;
        this.address = address;
        this.hasReceipt = hasReceipt;
        this.buyerAvatarImageId = buyerAvatarImageId;
        this.sellerAvatarImageId = sellerAvatarImageId;
    }

    public long getId() { return id; }
    public Long getPostId() { return postId; }
    public long getAlbumId() { return albumId; }
    public long getBuyerId() { return buyerId; }
    public long getSellerId() { return sellerId; }
    public String getBuyerUsername() { return buyerUsername; }
    public String getBuyerEmail() { return buyerEmail; }
    public String getBuyerLocale() { return buyerLocale; }
    public String getSellerUsername() { return sellerUsername; }
    public PaymentInfo getSellerPaymentInfo() { return sellerPaymentInfo; }
    public String getTitle() { return title; }
    public String getArtistName() { return artistName; }
    public Long getCoverImageId() { return coverImageId; }
    public Integer getPrice() { return price; }
    public Message getLastMessage() { return lastMessage; }
    public InquiryStatus getStatus() { return status; }
    public PostStatus getPostStatus() { return postStatus; }
    public Address getAddress() { return address; }
    public Long getBuyerAvatarImageId() { return buyerAvatarImageId; }
    public Long getSellerAvatarImageId() { return sellerAvatarImageId; }
    public boolean isHasReceipt() { return hasReceipt; }
    public boolean hasSellerPaymentInfo() { return sellerPaymentInfo.isPresent(); }

    public InquirySummary withAddress(final Address newAddress) {
        return new InquirySummary(id, postId, albumId, buyerId, sellerId, buyerUsername, buyerEmail, buyerLocale,
                sellerUsername, sellerPaymentInfo, title, artistName, coverImageId, price, lastMessage, status,
                postStatus, newAddress, hasReceipt, buyerAvatarImageId, sellerAvatarImageId);
    }

    // La bandeja solo ofrece aceptar o rechazar mientras la consulta sigue abierta y el
    // ejemplar sigue a la venta.
    public boolean isPending() { return status == InquiryStatus.PENDING; }
    public boolean isPostAvailable() { return postStatus == PostStatus.AVAILABLE; }
    public boolean isPostDeleted() { return postId == null; }
    public boolean isAwaitingPayment() { return status == InquiryStatus.AWAITING_PAYMENT; }
    public boolean isPaymentSubmitted() { return status == InquiryStatus.PAYMENT_SUBMITTED; }
    // El comprador solo puede echarse atras antes de subir el comprobante; el Publicante, tambien despues.
    public boolean isCancellableBy(final boolean seller) {
        return isAwaitingPayment() || (seller && isPaymentSubmitted());
    }
    // Desde que se acepto hay una venta que mirar, aunque haya terminado cancelada.
    public boolean isSale() { return status != InquiryStatus.PENDING && status != InquiryStatus.REJECTED; }
    // Rechazada o cancelada, la Conversacion queda de solo lectura.
    public boolean isConversationOpen() {
        return status != InquiryStatus.REJECTED && status != InquiryStatus.CANCELLED;
    }
}
```
