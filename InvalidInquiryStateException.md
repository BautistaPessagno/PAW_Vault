---
title: "InvalidInquiryStateException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidInquiryStateException.java"]
---

# InvalidInquiryStateException

A guarded sale or inquiry update did not find its expected open state, or the inquiry's publication has been deleted. [[InquiryController]] maps it to HTTP 409.

## Connections

Project types referenced: none.

Referenced by: [[InquiryController]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidInquiryStateException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidInquiryStateException.java>)

```java
package ar.edu.itba.paw.services;

public class InvalidInquiryStateException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
