---
title: "LineBreakNormalizingEditor"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/LineBreakNormalizingEditor.java"]
---

# LineBreakNormalizingEditor

Editor de binding que normaliza CRLF a LF y recorta. El navegador cuenta un salto como un carácter en `maxlength` pero lo envía como dos; sin esto `@Size` rechazaría un texto válido.

## Guía de lectura

Operaciones para localizar en la fuente: `setAsText`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[MessageRules]].

Referenciado por: [[InquiryController]], [[PostContactController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/form/LineBreakNormalizingEditor.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/LineBreakNormalizingEditor.java>), líneas 1–19.

```java
package ar.edu.itba.paw.webapp.form;

import ar.edu.itba.paw.models.MessageRules;

import java.beans.PropertyEditorSupport;

/*
 * El browser mide el maxlength del textarea contando los saltos como LF, pero manda el
 * contenido con CRLF: sin normalizar, un mensaje que la UI dio por bueno llega con un
 * caracter de mas por salto de linea y @Size lo rechaza. Tambien recorta, porque el editor
 * por campo reemplaza al StringTrimmerEditor registrado para todos los String.
 */
public final class LineBreakNormalizingEditor extends PropertyEditorSupport {

    @Override
    public void setAsText(final String text) {
        setValue(MessageRules.normalize(text));
    }
}
```
