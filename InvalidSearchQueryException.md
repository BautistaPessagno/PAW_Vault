---
title: "InvalidSearchQueryException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidSearchQueryException.java"]
---

# InvalidSearchQueryException

Normalized search text exceeds 255 characters. [[LandingController]] maps it to HTTP 400.

## Connections

Project types referenced: none.

Referenced by: [[LandingController]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidSearchQueryException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidSearchQueryException.java>)

```java
package ar.edu.itba.paw.services;

public class InvalidSearchQueryException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
