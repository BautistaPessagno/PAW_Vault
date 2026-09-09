---
title: "EmailDeliveryException"
categories: ["History"]
type: "historical-code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
source_commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
tags: ["codemap", "services"]
sources: []
---

# EmailDeliveryException

> [!note] Historical source
> This type is absent at ff96f27. The text and excerpt below describe the previous implementation at 041ce34.

Unchecked wrapper retaining a message and Throwable cause through its constructor. [[EmailServiceImpl]] raises it for contact delivery or rendering errors; [[PostServiceImpl]] lets it propagate; [[PostContactController]] converts it to a 503 form response. Welcome mail catches its own failures without using this exception.

## Connections

Project types referenced: none.

Referenced by: [[EmailServiceImpl]], [[PostContactController]].

Tests: [[EmailServiceImplTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java, lines 1–8](<https://bitbucket.org/itba/paw-2026b-14/src/041ce34404963b689d05443ca00abb7e75aa7f15/services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java>)

```java
package ar.edu.itba.paw.services.exceptions;

public class EmailDeliveryException extends RuntimeException {

    public EmailDeliveryException(final String message, final Throwable cause) {
        super(message, cause);
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
