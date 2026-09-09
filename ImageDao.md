---
title: "ImageDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java"]
---

# ImageDao

Persistence contract for findById and create of [[Image]]. create accepts a content type and bytes; [[ImageServiceImpl]] validates them before the normal application write path reaches this interface.

## Connections

Project types referenced: [[Image]].

Referenced by: [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageServiceImpl]], [[ImageServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;

import java.util.Optional;

public interface ImageDao {

    Optional<Image> findById(long id);

    Image create(String contentType, byte[] data);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
