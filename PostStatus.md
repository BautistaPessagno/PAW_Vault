---
title: "PostStatus"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostStatus.java"]
---

# PostStatus

Estado de la publicación: `AVAILABLE`, `RESERVED` (hay una venta en curso) o `SOLD`. Las transiciones las hace [[PostServiceImpl]] con guarda de estado.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartItemDao]], [[CartItemJdbcDao]], [[CartItemJdbcDaoTest]], [[CartServiceImplTest]], [[ContactRules]], [[ContactRulesTest]], [[InquiryGroup]], [[InquiryJdbcDao]], [[InquiryJdbcDaoTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[InquirySummary]], [[Post]], [[PostController]], [[PostDao]], [[PostDetail]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PostStatus.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostStatus.java>), líneas 1–7.

```java
package ar.edu.itba.paw.models;

public enum PostStatus {
    AVAILABLE,
    RESERVED,
    SOLD
}
```
