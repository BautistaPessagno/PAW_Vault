---
title: "DuplicatePostException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java"]
---

# DuplicatePostException

Unchecked business exception for a user who already published the same album. It can originate from the pre-check or from translated database uniqueness failure. [[PublishController]] maps it to `publish.duplicate` on publisherEmail and redisplays the submitted form.

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

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
