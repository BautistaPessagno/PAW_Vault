---
title: "ValidCatalogFilters"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidCatalogFilters.java"]
---

# ValidCatalogFilters

Anotación de clase que aplica [[CatalogFilterValidator]].

## Guía de lectura

Operaciones para localizar en la fuente: `message`, `groups`, `payload`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[CatalogFilterValidator]].

Referenciado por: [[CatalogFilterForm]], [[CatalogFilterValidator]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidCatalogFilters.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidCatalogFilters.java>), líneas 1–23.

```java
package ar.edu.itba.paw.webapp.validation;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.TYPE;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Documented
@Constraint(validatedBy = CatalogFilterValidator.class)
@Target(TYPE)
@Retention(RUNTIME)
public @interface ValidCatalogFilters {

    String message() default "{validation.form.invalid}";

    Class<?>[] groups() default { };

    Class<? extends Payload>[] payload() default { };
}
```
