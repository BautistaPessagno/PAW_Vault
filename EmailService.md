---
title: "EmailService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java"]
---

# EmailService

Contrato de envío de correos: siete operaciones, cada una con el `Locale` como parámetro porque el envío corre en otro hilo. Ver [[Mail delivery]].

## Guía de lectura

Operaciones para localizar en la fuente: `sendWelcomeEmail`, `sendVerificationEmail`, `sendPostInterestEmail`, `sendInquiryUpdateEmail`, `sendMessageEmail`, `sendPasswordChangedEmail`, `sendPasswordResetEmail`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquiryUpdateNotification]], [[MessageNotification]], [[PostInterestNotification]], [[User]].

Referenciado por: [[EmailServiceImpl]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>), líneas 1–26.

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

    void sendInquiryUpdateEmail(InquiryUpdateNotification notification, Locale locale);

    void sendMessageEmail(MessageNotification notification, Locale locale);

    void sendPasswordChangedEmail(User user, Locale locale);

    void sendPasswordResetEmail(User user, String token, Locale locale);
}
```
