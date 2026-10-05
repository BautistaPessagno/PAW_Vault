---
title: "AvatarFormValidator"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/validation/AvatarFormValidator.java"]
---

# AvatarFormValidator

Quitar la foto no necesita archivo; cambiarla exige una imagen que cumpla [[ImageRules]].

## Guía de lectura

Operaciones para localizar en la fuente: `isValid`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AvatarForm]], [[ImageFiles]], [[ValidAvatarForm]].

Referenciado por: [[ValidAvatarForm]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/AvatarFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/AvatarFormValidator.java>), líneas 1–16.

```java
package ar.edu.itba.paw.webapp.validation;

import ar.edu.itba.paw.webapp.form.AvatarForm;
import ar.edu.itba.paw.webapp.form.ImageFiles;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

// Quitar la foto no necesita archivo; cambiarla exige una imagen que cumpla ImageRules.
public class AvatarFormValidator implements ConstraintValidator<ValidAvatarForm, AvatarForm> {

    @Override
    public boolean isValid(final AvatarForm form, final ConstraintValidatorContext context) {
        return form == null || form.isRemove() || ImageFiles.isValid(form.getAvatar());
    }
}
```
