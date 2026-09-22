---
title: "ConcurrentPublishException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java"]
---

# ConcurrentPublishException

Unchecked business exception used when publish or update catches a Spring DataIntegrityViolationException other than a duplicate post key. [[PublishController]] maps it to `publish.concurrent` on both the publish and edit forms and retains form data. The catch does not inspect a constraint name, so it does not prove that every integrity failure was a race. Retrying is manual and not guaranteed to repair unrelated integrity failures.

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
