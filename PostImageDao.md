---
title: "PostImageDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostImageDao.java"]
---

# PostImageDao

Contrato de la galería: ids de las fotos adicionales en orden, agregar una en una posición y borrar las de un post.

## Guía de lectura

Operaciones para localizar en la fuente: `findImageIdsByPostId`, `add`, `deleteByPostId`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[ImageServiceImpl]], [[ImageServiceImplTest]], [[PostImageJdbcDao]], [[PostImageJdbcDaoTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostImageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostImageDao.java>), líneas 1–12.

```java
package ar.edu.itba.paw.persistence;

import java.util.List;

public interface PostImageDao {

    List<Long> findImageIdsByPostId(long postId);

    long add(long postId, long imageId, int position);

    int deleteByPostId(long postId);
}
```
