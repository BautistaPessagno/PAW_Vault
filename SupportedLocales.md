---
title: "SupportedLocales"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java"]
---

# SupportedLocales

Idiomas que la aplicación sabe hablar (`es`, `en`, `fr`). Normaliza antes de guardar `preferred_locale` y antes de elegir el idioma de un correo.

## Guía de lectura

Datos y dependencias declaradas: `DEFAULT_LANGUAGE`, `SUPPORTED_LANGUAGES`.

Operaciones para localizar en la fuente: `languageOf`, `localeOf`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryServiceImpl]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java>), líneas 1–35.

```java
package ar.edu.itba.paw.services;

import java.util.List;
import java.util.Locale;

/*
 * Idiomas que la aplicacion sabe hablar, los mismos que tienen bundle de i18n. Los services
 * normalizan contra esta lista antes de tocar la base, asi un idioma que no soportamos nunca
 * llega a users.preferred_locale ni al mail.
 */
final class SupportedLocales {

    private static final String DEFAULT_LANGUAGE = "es";

    private static final List<String> SUPPORTED_LANGUAGES = List.of(DEFAULT_LANGUAGE, "en", "fr");

    private SupportedLocales() {
        // Clase de utilidad.
    }

    // Idioma persistible: lo que guarda users.preferred_locale.
    static String languageOf(final Locale locale) {
        if (locale == null) {
            return DEFAULT_LANGUAGE;
        }
        final String language = locale.getLanguage();
        return SUPPORTED_LANGUAGES.contains(language) ? language : DEFAULT_LANGUAGE;
    }

    // Locale con el que se resuelven los bundles, a partir de lo guardado en la base.
    static Locale localeOf(final String languageTag) {
        final Locale locale = languageTag == null ? null : Locale.forLanguageTag(languageTag);
        return Locale.forLanguageTag(languageOf(locale));
    }
}
```
