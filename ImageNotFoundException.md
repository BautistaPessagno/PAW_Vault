---
title: "ImageNotFoundException"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/ImageNotFoundException.java"]
---

# ImageNotFoundException

Web runtime marker for a missing image ID. [[ImageController]] catches it locally and sets HTTP 404. It is distinct from [[PostNotFoundException]], which identifies a missing publication.

## Connections

Project types referenced: none.

Referenced by: [[ImageController]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/ImageNotFoundException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/ImageNotFoundException.java>)

```java
package ar.edu.itba.paw.webapp.exceptions;

public class ImageNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
