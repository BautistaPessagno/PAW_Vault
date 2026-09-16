---
title: "UserNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java"]
---

# UserNotFoundException

Service-contract exception for a missing publisher account during publish. This is a new type in ar.edu.itba.paw.services; the deleted web exception remains at [[Legacy UserNotFoundException]]. No dedicated HTTP mapping is declared here.

## Connections

Project types referenced: [[User]].

Referenced by: [[PostServiceImpl]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java, lines 1–7](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java>)

```java
package ar.edu.itba.paw.services;

public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException() {
        super("User not found");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
