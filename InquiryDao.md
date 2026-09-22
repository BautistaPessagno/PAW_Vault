---
title: "InquiryDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java"]
---

# InquiryDao

Persists inquiries and loads one by ID. Inbox reads return the rows of one page of groups, where groupLimit and groupOffset count publications; companion methods count groups and raw inquiries per buyer or seller. It also applies guarded PENDING transitions, rejects competitors after a sale and detaches inquiries before a publication is deleted. The service owns transactions and seller checks.

## Connections

Project types referenced: [[Inquiry]], [[InquirySummary]].

Referenced by: [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquirySummary;

import java.util.List;
import java.util.Optional;

public interface InquiryDao {
    Inquiry create(long postId, long buyerId, String message);

    Optional<Inquiry> findById(long id);

    // Bandejas paginadas por publicacion: devuelven las consultas de una pagina de grupos,
    // ordenadas de la mas nueva a la mas vieja. El grupo es el post, o el album y el vendedor
    // cuando el post fue eliminado. groupLimit/groupOffset cuentan grupos, no consultas.
    List<InquirySummary> findByBuyerId(long buyerId, int groupLimit, int groupOffset);

    List<InquirySummary> findBySellerId(long sellerId, int groupLimit, int groupOffset);

    int countGroupsByBuyerId(long buyerId);

    int countGroupsBySellerId(long sellerId);

    boolean acceptPending(long id);

    boolean rejectPending(long id);

    int rejectOtherPending(long postId, long acceptedInquiryId);

    int countByBuyerId(long buyerId);

    int countBySellerId(long sellerId);

    int detachFromPost(long postId);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
