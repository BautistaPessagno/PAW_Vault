---
title: "PostInterestNotification"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java"]
---

# PostInterestNotification

Carga del correo de "consulta nueva": publicante, quién consulta, mensaje opcional y la lista de vinilos (`InterestedPost`) con la Consulta de cada uno. El contacto manda uno; el carrito, todos los de un mismo publicante en un solo correo.

## Guía de lectura

Datos y dependencias declaradas: `publisherEmail`, `contactName`, `message`, `posts`, `postId`, `inquiryId`, `albumTitle`, `artistName`, `releaseYear`.

Operaciones para localizar en la fuente: `getPublisherEmail`, `getContactName`, `getMessage`, `getPosts`, `InterestedPost`, `getPostId`, `getInquiryId`, `getAlbumTitle`, `getArtistName`, `getReleaseYear`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java>), líneas 1–80.

```java
package ar.edu.itba.paw.services;

import java.util.List;

/*
 * Aviso al Publicante de que alguien consulto por sus vinilos: uno desde el contacto, uno o
 * varios desde el carrito, siempre en un solo correo. No lleva el correo del comprador: el
 * Publicante le responde desde la Conversacion de cada Consulta.
 */
public final class PostInterestNotification {

    private final String publisherEmail;
    private final String contactName;
    private final String message;
    private final List<InterestedPost> posts;

    public PostInterestNotification(final String publisherEmail, final String contactName, final String message,
                                    final List<InterestedPost> posts) {
        this.publisherEmail = publisherEmail;
        this.contactName = contactName;
        this.message = message;
        this.posts = List.copyOf(posts);
    }

    public String getPublisherEmail() {
        return publisherEmail;
    }

    public String getContactName() {
        return contactName;
    }

    // null cuando el interesado no dejo ningun mensaje. El carrito nunca lo trae.
    public String getMessage() {
        return message;
    }

    public List<InterestedPost> getPosts() {
        return posts;
    }

    // Un vinilo consultado y la Consulta que lo pide, a la que lleva el enlace del correo.
    public static final class InterestedPost {

        private final long postId;
        private final long inquiryId;
        private final String albumTitle;
        private final String artistName;
        private final int releaseYear;

        public InterestedPost(final long postId, final long inquiryId, final String albumTitle,
                              final String artistName, final int releaseYear) {
            this.postId = postId;
            this.inquiryId = inquiryId;
            this.albumTitle = albumTitle;
            this.artistName = artistName;
            this.releaseYear = releaseYear;
        }

        public long getPostId() {
            return postId;
        }

        public long getInquiryId() {
            return inquiryId;
        }

        public String getAlbumTitle() {
            return albumTitle;
        }

        public String getArtistName() {
            return artistName;
        }

        public int getReleaseYear() {
            return releaseYear;
        }
    }
}
```
