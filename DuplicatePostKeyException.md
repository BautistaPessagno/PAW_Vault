---
title: "DuplicatePostKeyException"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java"]
---

# DuplicatePostKeyException

Unchecked persistence-contract exception raised by [[PostJdbcDao]] after Spring reports a duplicate insert key. It has no custom message or cause constructor. [[PostServiceImpl]] translates it to [[DuplicatePostException]] so the controller need not import DAO-layer exceptions.

## Connections

Project types referenced: none.

Referenced by: [[PostJdbcDao]], [[PostServiceImpl]].

Tests: [[PostJdbcDaoTest]], [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java>)

```java
package ar.edu.itba.paw.persistence;

public class DuplicatePostKeyException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
