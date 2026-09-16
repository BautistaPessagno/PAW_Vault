---
title: "Inquiry"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Inquiry.java"]
---

# Inquiry

Persisted purchase inquiry identity, post ID, buyer ID and optional message. This compact model omits database status and timestamp; [[InquirySummary]] supplies status for the inbox.

## Connections

Project types referenced: none.

Referenced by: [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Inquiry.java, lines 1–32](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Inquiry.java>)

```java
package ar.edu.itba.paw.models;

public class Inquiry {
    private final long id;
    private final long postId;
    private final long buyerId;
    private final String message;

    public Inquiry(final long id, final long postId, final long buyerId, final String message) {
        this.id = id;
        this.postId = postId;
        this.buyerId = buyerId;
        this.message = message;
    }

    public long getId() {
        return id;
    }

    public long getPostId() {
        return postId;
    }

    public long getBuyerId() {
        return buyerId;
    }

    // null cuando el comprador no dejo ningun mensaje.
    public String getMessage() {
        return message;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
