---
title: "DuplicatePostKeyException"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java"]
---

# DuplicatePostKeyException

Marca de persistencia: el `INSERT` o `UPDATE` de un post violó la unicidad `(user_id, album_id)`. [[PostServiceImpl]] la traduce a [[DuplicatePostException]]. Existe para que services no dependa de la excepción de Spring.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java>), líneas 1–4.

```java
package ar.edu.itba.paw.persistence;

public class DuplicatePostKeyException extends RuntimeException {
}
```
