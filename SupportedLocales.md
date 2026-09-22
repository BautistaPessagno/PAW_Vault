---
title: "SupportedLocales"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java"]
---

# SupportedLocales

Package-private locale utility for persisted preferences and mail recipients. Supports es/en/fr, defaulting null or unsupported languages to Spanish. It resolves the seller's language for interest mail and the buyer's for acceptance mail. Request UI locale resolution is configured separately in [[WebConfig]].

## Connections

Project types referenced: none.

Referenced by: [[InquiryServiceImpl]], [[UserServiceImpl]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java, lines 1–35](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
