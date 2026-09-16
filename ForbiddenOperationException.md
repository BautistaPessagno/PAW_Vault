---
title: "ForbiddenOperationException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java"]
---

# ForbiddenOperationException

Business authorization failure for self-contact or acting on another seller publication. Contact and inquiry controllers map it to HTTP 403.

## Connections

Project types referenced: none.

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]].

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
