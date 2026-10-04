---
title: "MessageNotification"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/MessageNotification.java"]
---

# MessageNotification

Carga del correo de "mensaje nuevo": consulta, destinatario, quién escribió, el texto y los datos del álbum.

## Guía de lectura

Datos y dependencias declaradas: `inquiryId`, `recipientEmail`, `senderUsername`, `body`, `albumTitle`, `artistName`, `releaseYear`.

Operaciones para localizar en la fuente: `getInquiryId`, `getRecipientEmail`, `getSenderUsername`, `getBody`, `getAlbumTitle`, `getArtistName`, `getReleaseYear`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/MessageNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/MessageNotification.java>), líneas 1–32.

```java
package ar.edu.itba.paw.services;

// Un Mensaje nuevo para la otra parte de la Consulta.
public final class MessageNotification {
    private final long inquiryId;
    private final String recipientEmail;
    private final String senderUsername;
    private final String body;
    private final String albumTitle;
    private final String artistName;
    private final int releaseYear;

    public MessageNotification(final long inquiryId, final String recipientEmail,
                               final String senderUsername, final String body, final String albumTitle,
                               final String artistName, final int releaseYear) {
        this.inquiryId = inquiryId;
        this.recipientEmail = recipientEmail;
        this.senderUsername = senderUsername;
        this.body = body;
        this.albumTitle = albumTitle;
        this.artistName = artistName;
        this.releaseYear = releaseYear;
    }

    public long getInquiryId() { return inquiryId; }
    public String getRecipientEmail() { return recipientEmail; }
    public String getSenderUsername() { return senderUsername; }
    public String getBody() { return body; }
    public String getAlbumTitle() { return albumTitle; }
    public String getArtistName() { return artistName; }
    public int getReleaseYear() { return releaseYear; }
}
```
