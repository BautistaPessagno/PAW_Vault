---
title: "SearchText"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchText.java"]
---

# SearchText

Shared search normalizer in the models module. phrase lowercases with Locale.ROOT, strips combining diacritics after NFD decomposition and collapses every run of non-letter/digit characters into one space; compact removes those spaces. DAOs persist phrase() in artists.search_phrase and albums.search_phrase, while services compare compact() queries. schema.sql repeats an approximate SQL backfill with TRANSLATE, so changing the rule requires rebuilding those columns.

## Connections

Project types referenced: none.

Referenced by: [[AlbumJdbcDao]], [[ArtistJdbcDao]], [[ArtistServiceImpl]], [[PostServiceImpl]].

## Exact source

[models/src/main/java/ar/edu/itba/paw/models/SearchText.java, lines 1–36](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchText.java>)

```java
package ar.edu.itba.paw.models;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

// Normalizacion compartida para busqueda: minusculas, sin diacriticos y con cada
// corrida de separadores reducida a un espacio. La usan los services para normalizar
// lo que teclea el usuario y el modulo persistence para llenar las columnas
// search_phrase. Si cambia la regla hay que reconstruir esas columnas, porque la
// comparacion se hace contra el valor ya guardado.
public final class SearchText {

    private static final Pattern DIACRITICS = Pattern.compile("\\p{M}+");
    private static final Pattern SEPARATORS = Pattern.compile("[^\\p{L}\\p{N}]+");

    private SearchText() {
    }

    // Forma con espacios: es la que se persiste y la que permite reconocer el
    // comienzo de cada palabra.
    public static String phrase(final String value) {
        if (value == null) {
            return "";
        }
        final String withoutDiacritics = DIACRITICS.matcher(
                Normalizer.normalize(value, Normalizer.Form.NFD)).replaceAll("");
        return SEPARATORS.matcher(withoutDiacritics.toLowerCase(Locale.ROOT)).replaceAll(" ").trim();
    }

    // Forma sin espacios: es contra la que se comparan las consultas, para que
    // "sodastereo" y "soda stereo" busquen lo mismo.
    public static String compact(final String value) {
        return phrase(value).replace(" ", "");
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
