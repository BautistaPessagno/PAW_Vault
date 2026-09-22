---
title: "UnchangedPasswordException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UnchangedPasswordException.java"]
---

# UnchangedPasswordException

Raised when a password change or recovery chooses the password already in use. [[ProfileController]] and [[AuthenticationController]] map it to a field error on password; recovery leaves the emailed link usable for another attempt.

## Connections

Project types referenced: none.

Referenced by: [[AuthenticationController]], [[ProfileController]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UnchangedPasswordException.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UnchangedPasswordException.java>)

```java
package ar.edu.itba.paw.services;

public class UnchangedPasswordException extends RuntimeException {
    public UnchangedPasswordException() {
        super("The new password must differ from the current one");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
