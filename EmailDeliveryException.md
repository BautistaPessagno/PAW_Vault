---
title: "EmailDeliveryException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java"]
---

# EmailDeliveryException

Unchecked wrapper retaining a message and Throwable cause through its constructor. [[EmailServiceImpl]] raises it for contact delivery or rendering errors; [[PostServiceImpl]] lets it propagate; [[PostContactController]] converts it to a 503 form response. Welcome mail catches its own failures without using this exception.

## Connections

Project types referenced: none.

Referenced by: [[EmailServiceImpl]], [[PostContactController]].

Tests: [[EmailServiceImplTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java, lines 1–8](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/exceptions/EmailDeliveryException.java>)

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
