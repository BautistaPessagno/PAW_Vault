---
title: "Condition"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Condition.java"]
---

# Condition

Fixed physical-condition choices NEW and USED. Optional on a publication and usable as an exact search filter.

## Connections

Project types referenced: none.

Referenced by: [[InquiryServiceImplTest]], [[LandingController]], [[Post]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]], [[PublishController]], [[PublishForm]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Condition.java, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Condition.java>)

```java
package ar.edu.itba.paw.models;

public enum Condition {
    NEW,
    USED
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
