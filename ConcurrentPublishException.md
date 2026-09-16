---
title: "ConcurrentPublishException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java"]
---

# ConcurrentPublishException

Unchecked business exception used when publish catches Spring DataIntegrityViolationException. [[PublishController]] maps it to `publish.concurrent` and retains form data. The comment describes a simultaneous identity insert, but the catch does not inspect a constraint name or prove that every integrity failure was caused by a race. Retrying is manual and not guaranteed to repair unrelated integrity failures.

## Connections

Project types referenced: none.

Referenced by: [[PostServiceImpl]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java, lines 1–8](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java>)

```java
package ar.edu.itba.paw.services;

/**
 * Otra publicacion simultanea creo el mismo artista, album o usuario. Su transaccion
 * ya commiteo, asi que reintentar la publicacion funciona.
 */
public class ConcurrentPublishException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
