---
title: "InquiryEvent"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryEvent.java"]
---

# InquiryEvent

Los seis cambios de una Consulta que disparan correo: `ACCEPTED`, `RECEIPT_UPLOADED`, `RECEIPT_REQUESTED`, `CONFIRMED`, `CANCELLED` y `REJECTED`. El evento elige las keys de i18n del asunto, el título y el texto.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquiryUpdateNotification]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryEvent.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryEvent.java>), líneas 1–10.

```java
package ar.edu.itba.paw.services;

public enum InquiryEvent {
    ACCEPTED,
    RECEIPT_UPLOADED,
    RECEIPT_REQUESTED,
    CONFIRMED,
    CANCELLED,
    REJECTED
}
```
