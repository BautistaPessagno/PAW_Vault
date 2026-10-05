---
title: "InquiryUpdateNotification"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryUpdateNotification.java"]
---

# InquiryUpdateNotification

Carga del correo de un cambio de Consulta: evento, consulta, destinatario y datos del álbum. Reemplazó a la notificación de "aceptada".

## Guía de lectura

Datos y dependencias declaradas: `event`, `inquiryId`, `recipientEmail`, `albumTitle`, `artistName`, `releaseYear`.

Operaciones para localizar en la fuente: `getEvent`, `getInquiryId`, `getRecipientEmail`, `getAlbumTitle`, `getArtistName`, `getReleaseYear`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[InquiryEvent]].

Referenciado por: [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryUpdateNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryUpdateNotification.java>), líneas 1–27.

```java
package ar.edu.itba.paw.services;

public final class InquiryUpdateNotification {
    private final InquiryEvent event;
    private final long inquiryId;
    private final String recipientEmail;
    private final String albumTitle;
    private final String artistName;
    private final int releaseYear;

    public InquiryUpdateNotification(final InquiryEvent event, final long inquiryId, final String recipientEmail,
                                     final String albumTitle, final String artistName, final int releaseYear) {
        this.event = event;
        this.inquiryId = inquiryId;
        this.recipientEmail = recipientEmail;
        this.albumTitle = albumTitle;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
    }

    public InquiryEvent getEvent() { return event; }
    public long getInquiryId() { return inquiryId; }
    public String getRecipientEmail() { return recipientEmail; }
    public String getAlbumTitle() { return albumTitle; }
    public String getArtistName() { return artistName; }
    public int getReleaseYear() { return releaseYear; }
}
```
