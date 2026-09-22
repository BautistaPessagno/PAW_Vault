---
title: "EmailService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java"]
---

# EmailService

Six mail operations: verification, welcome, post interest, inquiry accepted, password changed and password reset. Each takes an explicit Locale because delivery runs on a worker thread outside the request.

## Connections

Project types referenced: [[InquiryAcceptedNotification]], [[PostInterestNotification]], [[User]].

Referenced by: [[EmailServiceImpl]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>)

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

    void sendInquiryAcceptedEmail(InquiryAcceptedNotification notification, Locale locale);

    void sendPasswordChangedEmail(User user, Locale locale);

    void sendPasswordResetEmail(User user, String token, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
