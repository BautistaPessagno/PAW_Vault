---
title: "DuplicatePostException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java"]
---

# DuplicatePostException

Unchecked business exception for a user who already published the same album. It can originate from the pre-check or from translated database uniqueness failure. [[PublishController]] maps it to the global form error `publish.duplicate` and redisplays the submitted form.

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
