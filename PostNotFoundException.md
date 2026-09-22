---
title: "PostNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java"]
---

# PostNotFoundException

Unchecked missing-publication signal from post and inquiry lookups, locking paths and guarded updates. [[PostController]], [[PublishController]], [[PostContactController]] and [[InquiryController]] map it to HTTP 404.

## Connections

Project types referenced: none.

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostContactController]], [[PostController]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java>)

```java
package ar.edu.itba.paw.services;

public class PostNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
