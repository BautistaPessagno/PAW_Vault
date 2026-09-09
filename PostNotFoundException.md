---
title: "PostNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java"]
---

# PostNotFoundException

Unchecked missing-publication signal used when the contact GET lookup or notification lookup returns empty. [[PostContactController]] has a local ExceptionHandler and ResponseStatus NOT_FOUND, so this contact path returns HTTP 404.

## Connections

Project types referenced: none.

Referenced by: [[PostContactController]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java>)

```java
package ar.edu.itba.paw.services;

public class PostNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
