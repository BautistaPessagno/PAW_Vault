---
title: "PostStatus"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostStatus.java"]
---

# PostStatus

Publication states AVAILABLE and SOLD. Search and suggestions include AVAILABLE only. Accepting an inquiry transitions the exemplar to SOLD, after which it can no longer be edited, deleted or contacted; the public detail page still shows it with a sold marker.

## Connections

Project types referenced: none.

Referenced by: [[InquiryGroup]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]], [[Post]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/PostStatus.java, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostStatus.java>)

```java
package ar.edu.itba.paw.models;

public enum PostStatus {
    AVAILABLE,
    SOLD
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
