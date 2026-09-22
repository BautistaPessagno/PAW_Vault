---
title: "ImageDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java"]
---

# ImageDao

Persistence contract for findById, create and delete of [[Image]]. create accepts a content type and bytes validated earlier by [[ImageServiceImpl]]; delete removes one row and reports whether it existed. The application deletes images only when a publication with its own photo is deleted.

## Connections

Project types referenced: [[Image]].

Referenced by: [[ImageJdbcDao]], [[ImageJdbcDaoTest]], [[ImageServiceImpl]], [[ImageServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Image;

import java.util.Optional;

public interface ImageDao {

    Optional<Image> findById(long id);

    Image create(String contentType, byte[] data);

    boolean delete(long id);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
