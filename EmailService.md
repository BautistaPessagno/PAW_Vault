---
title: "EmailService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java"]
---

# EmailService

Three mail operations: verification, welcome and post interest. Each takes an explicit Locale for use outside request context.

## Connections

Project types referenced: [[PostInterestNotification]], [[User]].

Referenced by: [[EmailServiceImpl]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java, lines 1–18](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;

import java.util.Locale;

public interface EmailService {

    void sendWelcomeEmail(User user, Locale locale);

    void sendVerificationEmail(User user, String token, Locale locale);

    /*
     * El locale se recibe como parametro y no se toma de LocaleContextHolder porque el
     * envio corre en otro hilo: hay que resolverlo en el hilo del request y pasarlo.
     */
    void sendPostInterestEmail(PostInterestNotification notification, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
