---
title: "InquiryService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java"]
---

# InquiryService

Validates contactability, persists a buyer inquiry, lists sent/received inquiries and lets the owner accept or reject one. Buyer identity arguments come from [[AuthenticatedUser]] in the web controller.

## Connections

Project types referenced: [[Inquiry]], [[InquirySummary]], [[PostSummary]].

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[PostContactController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquirySummary;
import ar.edu.itba.paw.models.PostSummary;

import java.util.List;

public interface InquiryService {

    PostSummary findContactablePost(long postId, long buyerId);

    // El nombre y el correo del comprador llegan del usuario autenticado, asi que no hace
    // falta volver a buscarlos en la base.
    Inquiry submit(long postId, long buyerId, String buyerUsername, String buyerEmail, String message);

    List<InquirySummary> findSentBy(long buyerId);

    List<InquirySummary> findReceivedBy(long sellerId);

    void accept(long inquiryId, long sellerId);

    void reject(long inquiryId, long sellerId);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
