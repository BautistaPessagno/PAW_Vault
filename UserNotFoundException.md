---
title: "UserNotFoundException"
categories: ["History"]
type: "historical-code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "removed"
source_commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
tags: ["codemap", "web"]
sources: []
---

# UserNotFoundException

> [!note] Historical source
> This type is absent at ff96f27. The text and excerpt below describe the previous implementation at 041ce34.

Unchecked marker thrown by [[HelloWorldController]] for missing users. The class has no ResponseStatus and the controller has no handler for it. This snapshot therefore does not explicitly turn it into a 404; do not infer the contact controller behavior applies to this route.

## Connections

Project types referenced: none.

Referenced by: [[HelloWorldController]].

Tests: no direct test source reference. See [[Testing and evidence]].

## Exact source

[webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java, lines 1–4](<https://bitbucket.org/itba/paw-2026b-14/src/041ce34404963b689d05443ca00abb7e75aa7f15/webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/UserNotFoundException.java>)

```java
package ar.edu.itba.paw.webapp.exceptions;

public class UserNotFoundException extends RuntimeException {
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
