---
title: "PostStatus"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostStatus.java"]
---

# PostStatus

Publication states AVAILABLE and SOLD. Search includes AVAILABLE only; accepting an inquiry transitions the exemplar to SOLD.

## Connections

Project types referenced: none.

Referenced by: [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]], [[Post]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImplTest]], [[PostSummary]].

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
