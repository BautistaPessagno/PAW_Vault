---
title: "Message"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Message.java"]
---

# Message

Un texto de la conversación de una Consulta: autor, cuerpo y fecha. No se edita ni se borra. Ver [[Conversation flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `inquiryId`, `senderId`, `body`, `createdAt`.

Operaciones para localizar en la fuente: `getId`, `getInquiryId`, `getSenderId`, `getBody`, `getCreatedAt`, `getSentAt`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[EmailServiceImplTest]], [[InquiryDetail]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryService]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]], [[MessageDao]], [[MessageJdbcDao]], [[MessageJdbcDaoTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/Message.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Message.java>), líneas 1–34.

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

// Un texto que una de las dos partes escribio en la Conversacion de una Consulta. No se edita ni se borra.
public final class Message {
    private final long id;
    private final long inquiryId;
    private final long senderId;
    private final String body;
    private final LocalDateTime createdAt;

    public Message(final long id, final long inquiryId, final long senderId, final String body,
                   final LocalDateTime createdAt) {
        this.id = id;
        this.inquiryId = inquiryId;
        this.senderId = senderId;
        this.body = body;
        this.createdAt = createdAt;
    }

    public long getId() { return id; }
    public long getInquiryId() { return inquiryId; }
    public long getSenderId() { return senderId; }
    public String getBody() { return body; }
    public LocalDateTime getCreatedAt() { return createdAt; }

    // fmt:formatDate solo acepta java.util.Date: copia nueva en cada llamada, el modelo sigue inmutable.
    public Date getSentAt() {
        return Date.from(createdAt.atZone(ZoneId.systemDefault()).toInstant());
    }
}
```
