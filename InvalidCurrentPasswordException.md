---
title: "InvalidCurrentPasswordException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java"]
---

# InvalidCurrentPasswordException

Raised by [[UserServiceImpl]] when the typed current password does not match, or when a concurrent change replaced the hash before the guarded update. [[ProfileController]] turns it into a field error on currentPassword.

## Connections

Project types referenced: none.

Referenced by: [[ProfileController]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java>)

```java
package ar.edu.itba.paw.services;

public class InvalidCurrentPasswordException extends RuntimeException {
    public InvalidCurrentPasswordException() {
        super("The current password is incorrect");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
