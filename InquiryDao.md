---
title: "InquiryDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java"]
---

# InquiryDao

Persist inquiries, retrieve sent/received projections and apply conditional pending-state updates. rejectOtherPending closes competitors for the accepted publication. The service owns transaction and seller checks.

## Connections

Project types referenced: [[Inquiry]], [[InquirySummary]].

Referenced by: [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java, lines 1–23](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Inquiry;
import ar.edu.itba.paw.models.InquirySummary;

import java.util.List;
import java.util.Optional;

public interface InquiryDao {
    Inquiry create(long postId, long buyerId, String message);

    Optional<Inquiry> findById(long id);

    List<InquirySummary> findByBuyerId(long buyerId);

    List<InquirySummary> findBySellerId(long sellerId);

    boolean acceptPending(long id);

    boolean rejectPending(long id);

    int rejectOtherPending(long postId, long acceptedInquiryId);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
