---
title: "InvalidImageException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java"]
---

# InvalidImageException

Runtime marker raised by [[ImageServiceImpl]] for unsupported content type, null/empty bytes or more than 5 MiB. [[PublishController]] maps it to a localized cover field error on the publish and edit forms. It also rolls back the surrounding publish or update transaction when it leaves the service.

## Connections

Project types referenced: none.

Referenced by: [[ImageServiceImpl]], [[ImageServiceImplTest]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java>)

```java
package ar.edu.itba.paw.services;

public class InvalidImageException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
