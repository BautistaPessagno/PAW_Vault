---
title: "Condition"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/Condition.java"]
---

# Condition

Estado físico del ejemplar: `NEW` o `USED`. Obligatorio al publicar; filtro del catálogo. La base lo refuerza con un `CHECK`.

## Guía de lectura

Sin campos ni métodos propios: el archivo completo está abajo.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[CartServiceImplTest]], [[CatalogFilterForm]], [[InquiryServiceImplTest]], [[LandingController]], [[Post]], [[PostDao]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostSearchCriteria]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostSummary]], [[PublishController]], [[PublishForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/Condition.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Condition.java>), líneas 1–6.

```java
package ar.edu.itba.paw.models;

public enum Condition {
    NEW,
    USED
}
```
