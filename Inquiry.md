---
title: "Inquiry"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Inquiry.java"]
---

# Inquiry

Persisted purchase inquiry: ID, nullable post ID, buyer ID, optional message and [[InquiryStatus]]. postId becomes null when the publication is deleted; isPostDeleted exposes that case and [[InquiryServiceImpl]] refuses to accept or reject such an inquiry. The timestamp and the album/seller copy kept for deleted publications are not part of this compact model.

## Connections

Project types referenced: [[InquiryStatus]].

Referenced by: [[EmailServiceImpl]], [[InquiryDao]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/Inquiry.java, lines 1–47](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Inquiry.java>)

```java
package ar.edu.itba.paw.models;

/*
 * Una consulta tal como esta guardada. postId es null cuando la publicacion consultada fue
 * eliminada: la consulta sobrevive, pero ya no hay post sobre el que actuar.
 */
public final class Inquiry {
    private final long id;
    private final Long postId;
    private final long buyerId;
    private final String message;
    private final InquiryStatus status;

    public Inquiry(final long id, final Long postId, final long buyerId, final String message,
                   final InquiryStatus status) {
        this.id = id;
        this.postId = postId;
        this.buyerId = buyerId;
        this.message = message;
        this.status = status;
    }

    public long getId() {
        return id;
    }

    public Long getPostId() {
        return postId;
    }

    public boolean isPostDeleted() {
        return postId == null;
    }

    public long getBuyerId() {
        return buyerId;
    }

    // null cuando el comprador no dejo ningun mensaje.
    public String getMessage() {
        return message;
    }

    public InquiryStatus getStatus() {
        return status;
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
