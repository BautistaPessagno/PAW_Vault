---
title: "ForbiddenOperationException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java"]
---

# ForbiddenOperationException

Business authorization failure: self-contact, acting on another seller's inquiry, or opening the edit/delete routes of another owner's publication. Contact, inquiry and publish controllers map it to HTTP 403.

## Connections

Project types referenced: none.

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java>)

```java
package ar.edu.itba.paw.services;

public class ForbiddenOperationException extends RuntimeException {
    public ForbiddenOperationException() {
        super("The authenticated user cannot perform this operation");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
