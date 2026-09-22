---
title: "PostUnavailableException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java"]
---

# PostUnavailableException

The publication is no longer AVAILABLE. Raised for contact attempts and for edit or delete of a sold post. [[PostContactController]] and [[PublishController]] map it to HTTP 409.

## Connections

Project types referenced: none.

Referenced by: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java>)

```java
package ar.edu.itba.paw.services;

public class PostUnavailableException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
