---
title: "ImageService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java"]
---

# ImageService

Service contract for Optional<Image> lookup and image creation. [[ImageServiceImpl]] validates content type and byte length for create. It exposes no replace/delete operation, matching the long-lived cache policy in [[ImageController]].

## Connections

Project types referenced: [[Image]].

Referenced by: [[ImageController]], [[ImageServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Image;

import java.util.Optional;

public interface ImageService {

    Optional<Image> findById(long id);

    Image create(String contentType, byte[] data);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
