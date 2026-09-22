---
title: "DuplicatePostKeyException"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java"]
---

# DuplicatePostKeyException

Unchecked persistence-contract exception raised by [[PostJdbcDao]] when Spring reports a duplicate key on create, update or updateWithImage. It has no custom message or cause constructor. [[PostServiceImpl]] translates it to [[DuplicatePostException]] so the controller need not import DAO-layer exceptions.

## Connections

Project types referenced: none.

Referenced by: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java>)

```java
package ar.edu.itba.paw.persistence;

public class DuplicatePostKeyException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
