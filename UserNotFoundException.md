---
title: "UserNotFoundException"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java"]
---

# UserNotFoundException

Service-contract exception for a missing account in publish, inquiry notifications, username/password updates and password reset. [[ProfileController]] maps it to HTTP 404; other callers let it propagate. The deleted web exception remains at [[Legacy UserNotFoundException]].

## Connections

Project types referenced: [[User]].

Referenced by: [[InquiryServiceImpl]], [[PostServiceImpl]], [[ProfileController]], [[UserServiceImpl]], [[UserServiceImplTest]].

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
