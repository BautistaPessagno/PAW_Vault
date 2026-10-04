---
title: "InquiryDetail"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryDetail.java"]
---

# InquiryDetail

La Consulta vista por una de sus partes, con su conversación y la reseña propia. Decide qué puede hacer quien mira (aceptar, subir comprobante, cancelar, escribir, calificar) con las mismas reglas que [[InquiryServiceImpl]] aplica antes de escribir. Ver [[Inquiry and sale flow]].

## Guía de lectura

Datos y dependencias declaradas: `inquiry`, `sellerView`, `viewerId`, `messages`, `ownReview`.

Operaciones para localizar en la fuente: `getInquiry`, `isSellerView`, `getCounterpartyId`, `getCounterpartyUsername`, `getViewerId`, `getMessages`, `isSale`, `isCanWrite`, `isCanAccept`, `isCanReject`, `isOpen`, `isPaymentInfoVisible`, `isPaymentInfoMissing`, `isCanUploadReceipt`, `isReceiptRequested`, `isCanReviewReceipt`, `isCanCancel`, `isAddressVisible`, `isCanReview`, `getOwnReview`, `withOwnReview`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquiryStatus]], [[InquirySummary]], [[Message]], [[Review]].

Referenciado por: [[InquiryController]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/InquiryDetail.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryDetail.java>), líneas 1–89.

```java
package ar.edu.itba.paw.models;

import java.util.List;

/*
 * Una consulta vista por una de sus partes, en cualquier estado, con su Conversacion. Decide
 * que puede hacer quien mira segun su lado y el estado; InquiryService usa las mismas reglas
 * antes de escribir, y los UPDATE condicionales son la guarda final ante carreras.
 */
public final class InquiryDetail {

    private final InquirySummary inquiry;
    private final boolean sellerView;
    private final long viewerId;
    private final List<Message> messages;
    private final Review ownReview;

    public InquiryDetail(final InquirySummary inquiry, final boolean sellerView, final long viewerId,
                         final List<Message> messages) {
        this(inquiry, sellerView, viewerId, messages, null);
    }

    private InquiryDetail(final InquirySummary inquiry, final boolean sellerView, final long viewerId,
                          final List<Message> messages, final Review ownReview) {
        this.inquiry = inquiry;
        this.sellerView = sellerView;
        this.viewerId = viewerId;
        this.messages = List.copyOf(messages);
        this.ownReview = ownReview;
    }

    public InquirySummary getInquiry() { return inquiry; }

    public boolean isSellerView() { return sellerView; }

    // La otra parte de la Consulta: a quien se linkea y a quien califica quien mira.
    public long getCounterpartyId() { return sellerView ? inquiry.getBuyerId() : inquiry.getSellerId(); }

    public String getCounterpartyUsername() {
        return sellerView ? inquiry.getBuyerUsername() : inquiry.getSellerUsername();
    }

    // La vista marca los Mensajes propios comparando senderId con este id: EL no llama metodos con argumentos.
    public long getViewerId() { return viewerId; }

    // Del mas viejo al mas nuevo.
    public List<Message> getMessages() { return messages; }

    public boolean isSale() { return inquiry.isSale(); }

    // Mismo chequeo que InquiryService.sendMessage.
    public boolean isCanWrite() { return inquiry.isConversationOpen() && !inquiry.isPostDeleted(); }

    // Aceptar y rechazar deciden sobre el Comprador, no sobre un Mensaje.
    public boolean isCanAccept() { return sellerView && inquiry.isPending() && inquiry.isPostAvailable(); }

    public boolean isCanReject() { return sellerView && inquiry.isPending(); }

    private boolean isOpen() { return inquiry.isAwaitingPayment() || inquiry.isPaymentSubmitted(); }

    // El comprador ve a donde transferir mientras la venta esta abierta.
    public boolean isPaymentInfoVisible() { return !sellerView && isOpen(); }

    public boolean isPaymentInfoMissing() {
        return isPaymentInfoVisible() && !inquiry.hasSellerPaymentInfo();
    }

    public boolean isCanUploadReceipt() { return !sellerView && inquiry.isAwaitingPayment(); }

    // Esperando pago con un comprobante ya cargado: el Publicante pidio otro.
    public boolean isReceiptRequested() { return inquiry.isAwaitingPayment() && inquiry.isHasReceipt(); }

    public boolean isCanReviewReceipt() { return sellerView && inquiry.isPaymentSubmitted(); }

    // Misma regla que InquiryService.cancel.
    public boolean isCanCancel() { return inquiry.isCancellableBy(sellerView); }

    public boolean isAddressVisible() { return sellerView; }

    // Solo una venta confirmada se califica. Mismo chequeo que InquiryService.saveReview.
    public boolean isCanReview() { return inquiry.getStatus() == InquiryStatus.ACCEPTED; }

    // La Resena vigente de quien mira, o null si todavia no califico.
    public Review getOwnReview() { return ownReview; }

    public InquiryDetail withOwnReview(final Review review) {
        return new InquiryDetail(inquiry, sellerView, viewerId, messages, review);
    }
}
```
