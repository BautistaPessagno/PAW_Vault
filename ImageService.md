---
title: "ImageService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java"]
---

# ImageService

Service contract for Optional<Image> lookup, validated creation and deletion. [[ImageServiceImpl]] validates content type and byte length for create. Deletion is used when a publication with its own photo is removed. There is no replace operation: editing a photo stores a new image ID, which fits the long-lived cache policy in [[ImageController]].

## Connections

Project types referenced: [[Image]].

Referenced by: [[ImageController]], [[ImageServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;

import java.util.Optional;

public interface ImageService {

    Optional<Image> findById(long id);

    Image create(String contentType, byte[] data);

    boolean delete(long id);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
