---
title: "EmailService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java"]
---

# EmailService

Welcome and post-interest mail contract. Both operations accept a Locale explicitly; callers resolve it in the request thread before asynchronous delivery. [[EmailServiceImpl]] implements both with @Async and catches rendering/sending failures. The deleted [[EmailDeliveryException]] is historical.

## Connections

Project types referenced: [[PostInterestNotification]], [[User]].

Referenced by: [[EmailServiceImpl]], [[PostServiceImpl]], [[PostServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]], [[WebConfig]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java, lines 1–16](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;

public interface EmailService {

    void sendWelcomeEmail(User user, Locale locale);

    /*
     * El locale se recibe como parametro y no se toma de LocaleContextHolder porque el
     * envio corre en otro hilo: hay que resolverlo en el hilo del request y pasarlo.
     */
    void sendPostInterestEmail(PostInterestNotification notification, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
