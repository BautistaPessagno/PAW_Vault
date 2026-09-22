---
title: "DuplicateUserException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicateUserException.java"]
---

# DuplicateUserException

Registration error for an already enabled email or a competing duplicate insert. [[AuthenticationController]] attaches a localized error to the email field.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticationController]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicateUserException.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicateUserException.java>)

```java
package ar.edu.itba.paw.services;

public class DuplicateUserException extends RuntimeException {
    public DuplicateUserException() {
        super("A user with that email already exists");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
