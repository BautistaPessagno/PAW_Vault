---
title: "InquiryService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java"]
---

# InquiryService

Validates contactability, persists a buyer inquiry, pages sent and received inquiries grouped by publication, counts both sides for the inbox sub-navigation and lets the owner accept or reject one. submit now takes only post ID, buyer ID and message; the buyer's name and email come from the stored account.

## Connections

Project types referenced: [[Inquiry]], [[InquiryPage]], [[PostSummary]].

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[PostContactController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java, lines 1–27](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquiryPage;
import ar.edu.itba.paw.models.PostSummary;

public interface InquiryService {

    PostSummary findContactablePost(long postId, long buyerId);

    Inquiry submit(long postId, long buyerId, String message);

    // Las dos bandejas agrupan por publicacion y se paginan por grupo: varias consultas
    // sobre el mismo ejemplar son una sola entrada y nunca quedan partidas entre paginas.
    InquiryPage findSentGroupedByPost(long buyerId, int pageNumber);

    InquiryPage findReceivedGroupedByPost(long sellerId, int pageNumber);

    // Cada vista de la bandeja muestra el total de la otra en la sub-nav.
    int countSentBy(long buyerId);

    int countReceivedBy(long sellerId);

    Inquiry accept(long inquiryId, long sellerId);

    Inquiry reject(long inquiryId, long sellerId);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
