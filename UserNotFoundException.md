---
title: "UserNotFoundException"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "web"]
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java"]
---

# UserNotFoundException

Unchecked marker thrown by [[HelloWorldController]] for missing users. The class has no ResponseStatus and the controller has no handler for it. This snapshot therefore does not explicitly turn it into a 404; do not infer the contact controller behavior applies to this route.

## Connections

Project types referenced: none.

Referenced by: [[HelloWorldController]].

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java, lines 1–4](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java>)

```java
package ar.edu.itba.paw.webapp.exceptions;

public class UserNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
