---
title: "Condition"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Condition.java"]
---

# Condition

Fixed physical-condition choices NEW and USED. Required on every publication in this revision: PublishForm declares @NotNull, and schema.sql backfills legacy nulls to USED before adding NOT NULL and a CHECK. Usable as an exact search filter, rendered as a segmented control.

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
