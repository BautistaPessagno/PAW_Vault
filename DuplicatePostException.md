---
title: "DuplicatePostException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java"]
---

# DuplicatePostException

Unchecked business exception for a user who already published the same album. Publishing raises it from the pre-check or a translated uniqueness failure; editing raises it when the new catalog identity collides with another post of the same owner. [[PublishController]] maps it to the global form error `publish.duplicate` and redisplays the submitted form.

## Connections

Project types referenced: none.

Referenced by: [[PostServiceImpl]], [[PostServiceImplTest]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java>)

```java
package ar.edu.itba.paw.services;

public class DuplicatePostException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
