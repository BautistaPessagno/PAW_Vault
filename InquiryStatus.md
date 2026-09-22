---
title: "InquiryStatus"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java"]
---

# InquiryStatus

Inquiry states PENDING, ACCEPTED and REJECTED. [[InquiryJdbcDao]] applies guarded transitions from PENDING, and deleting a publication also turns its pending inquiries into REJECTED.

## Connections

Project types referenced: none.

Referenced by: [[Inquiry]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java>)

```java
package ar.edu.itba.paw.models;

public enum InquiryStatus {
    PENDING,
    ACCEPTED,
    REJECTED
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
