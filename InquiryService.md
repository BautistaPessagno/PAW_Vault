---
title: "InquiryService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java"]
---

# InquiryService

Contrato de consultas y ventas: contactar, envío en lote del carrito, bandejas agrupadas, transiciones de la venta, comprobante, conversación, reseñas y consultas de pertenencia para [[InquiryAccessHandler]].

## Guía de lectura

Operaciones para localizar en la fuente: `findContactablePost`, `submit`, `submitWithNewAddress`, `submitAll`, `findPostIdsWithOpenInquiry`, `findOpenInquiryId`, `findSentGroupedByPost`, `findReceivedGroupedByPost`, `countSentBy`, `countReceivedBy`, `accept`, `reject`, `uploadReceipt`, `requestNewReceipt`, `confirm`, `cancel`, `findDetail`, `saveReview`, `removeReview`, `sendMessage`, `findReceipt`, `findParties`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Inquiry]], [[InquiryDetail]], [[InquiryPage]], [[InquiryParties]], [[Message]], [[PostInterestNotification]], [[PostSummary]], [[Province]], [[Receipt]], [[Review]].

Referenciado por: [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryAccessHandler]], [[InquiryController]], [[InquiryServiceImpl]], [[PostContactController]], [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java>), líneas 1–96.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryDetail;
import ar.edu.itba.paw.models.InquiryPage;
import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.models.Message;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.Province;
import ar.edu.itba.paw.models.Receipt;
import ar.edu.itba.paw.models.Review;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.Set;

public interface InquiryService {

    // Lanza OpenInquiryExistsException si el comprador ya tiene una Consulta abierta sobre el post.
    PostSummary findContactablePost(long postId, long buyerId);

    // El texto, si trae, es el primer Mensaje de la Conversacion. Lanza OpenInquiryExistsException
    // si el comprador ya tiene una Consulta abierta sobre el post.
    Inquiry submit(long postId, long buyerId, String message, long addressId);

    // Guarda la direccion nueva en la libreta y la consulta en una sola transaccion: si la
    // consulta no entra, la direccion tampoco queda ocupando un lugar del tope.
    Inquiry submitWithNewAddress(long postId, long buyerId, String message, String street, String streetNumber,
                                 String apartment, String city, Province province, String postalCode, String notes);

    /*
     * Interna del carrito: solo CartService la llama, dentro de su transaccion, con los posts ya
     * bloqueados, disponibles, ajenos y sin Consulta abierta del comprador, y con una direccion
     * suya y vigente. Crea una Consulta sin Mensaje por post y avisa con un correo por Publicante,
     * despues del commit. Devuelve esos avisos, uno por Publicante, en el orden de los posts.
     */
    List<PostInterestNotification> submitAll(long buyerId, long addressId, List<PostSummary> posts);

    // De entre postIds, los posts sobre los que el comprador ya tiene una Consulta abierta.
    Set<Long> findPostIdsWithOpenInquiry(long buyerId, Collection<Long> postIds);

    // La Consulta abierta del comprador sobre el post, para mandarlo a su Conversacion.
    Optional<Long> findOpenInquiryId(long postId, long buyerId);

    // Las dos bandejas agrupan por publicacion y se paginan por grupo: varias consultas
    // sobre el mismo ejemplar son una sola entrada y nunca quedan partidas entre paginas.
    InquiryPage findSentGroupedByPost(long buyerId, int pageNumber);

    // Salvo en una venta en curso o concretada, el vendedor ve solo la ciudad y la provincia del envio.
    InquiryPage findReceivedGroupedByPost(long sellerId, int pageNumber);

    // Cada vista de la bandeja muestra el total de la otra en la sub-nav.
    int countSentBy(long buyerId);

    int countReceivedBy(long sellerId);

    Inquiry accept(long inquiryId, long sellerId);

    Inquiry reject(long inquiryId, long sellerId);

    // Cada operacion de la Venta recibe a quien la pide y lanza ForbiddenOperationException si
    // no le corresponde: subir es del comprador, revisar es del vendedor, ver y cancelar de los dos.
    // Lanza InvalidReceiptException si el archivo no cumple ReceiptRules.
    void uploadReceipt(long inquiryId, long buyerId, String contentType, byte[] data);

    void requestNewReceipt(long inquiryId, long sellerId);

    void confirm(long inquiryId, long sellerId);

    void cancel(long inquiryId, long userId);

    // La Consulta en cualquier estado, con su Conversacion. Mismas reglas de acceso y de
    // direccion parcial que la bandeja. En una venta confirmada trae ademas la Resena vigente de
    // quien mira, si ya califico.
    InquiryDetail findDetail(long inquiryId, long viewerId);

    // Califica a la otra parte de una venta confirmada, o reemplaza la calificacion anterior.
    // Lanza ForbiddenOperationException si el autor no es una de las partes,
    // InvalidInquiryStateException si la venta no esta confirmada e InvalidReviewException si no
    // cumple ReviewRules.
    Review saveReview(long inquiryId, long authorId, int rating, String body);

    // Idempotente: false si no habia una Resena vigente. Mismas excepciones que saveReview.
    boolean removeReview(long inquiryId, long authorId);

    // Lanza ForbiddenOperationException si quien escribe no es una de las partes,
    // InvalidInquiryStateException si la Conversacion esta cerrada e InvalidMessageException si
    // el texto no cumple MessageRules. Una Conversacion cerrada gana sobre un texto invalido.
    Message sendMessage(long inquiryId, long senderId, String body);

    Receipt findReceipt(long inquiryId, long viewerId);

    // Para InquiryAccessHandler: devuelve las partes, no decide. Vacio si la consulta no existe.
    Optional<InquiryParties> findParties(long inquiryId);
}
```
