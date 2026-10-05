---
title: "MessageDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/MessageDao.java"]
---

# MessageDao

Contrato de mensajes de una conversación: crear y listar por consulta en orden de llegada.

## Guía de lectura

Operaciones para localizar en la fuente: `create`, `findByInquiryId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Message]].

Referenciado por: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[MessageJdbcDao]], [[MessageJdbcDaoTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/MessageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/MessageDao.java>), líneas 1–12.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Message;

import java.util.List;

public interface MessageDao {
    Message create(long inquiryId, long senderId, String body);

    // Del mas viejo al mas nuevo.
    List<Message> findByInquiryId(long inquiryId);
}
```
