---
title: "PageNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PageNotFoundException.java"]
---

# PageNotFoundException

Unchecked signal for a page number below one, past a known total, or empty beyond page one in catalog search. [[Pagination]] and [[PostServiceImpl]] raise it; [[LandingController]], [[ProfileController]] and [[InquiryController]] map it to HTTP 404.

## Connections

Project types referenced: none.

Referenced by: [[InquiryController]], [[InquiryServiceImplTest]], [[LandingController]], [[Pagination]], [[PaginationTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[ProfileController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PageNotFoundException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PageNotFoundException.java>)

```java
package ar.edu.itba.paw.services;

public class PageNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
