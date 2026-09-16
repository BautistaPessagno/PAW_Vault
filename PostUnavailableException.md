---
title: "PostUnavailableException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java"]
---

# PostUnavailableException

Contact attempted on a publication whose status is not AVAILABLE. [[PostContactController]] maps it to HTTP 409.

## Connections

Project types referenced: none.

Referenced by: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java>)

```java
package ar.edu.itba.paw.services;

public class PostUnavailableException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
