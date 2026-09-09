---
title: "EmailService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java"]
---

# EmailService

Two mail operations with deliberately different implementations. [[EmailServiceImpl]] sends welcome mail asynchronously and swallows delivery failures; contact mail runs synchronously and raises [[EmailDeliveryException]]. The interface itself carries no async annotation, return future or delivery receipt.

## Connections

Project types referenced: [[PostInterestNotification]], [[User]].

Referenced by: [[EmailServiceImpl]], [[PostServiceImpl]], [[UserServiceImpl]].

Tests: [[PostServiceImplTest]], [[UserServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;

public interface EmailService {

    void sendWelcomeEmail(User user, Locale locale);

    void sendPostInterestEmail(PostInterestNotification notification);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
