---
title: "SearchText"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/SearchText.java"]
---

# SearchText

Normalización compartida de búsqueda: minúsculas, sin diacríticos y con separadores reducidos a un espacio (`phrase`), o sin espacios (`compact`). Persistence la usa para llenar `search_phrase` y los services para normalizar lo que se teclea. Ver [[Landing flow]].

## Guía de lectura

Datos y dependencias declaradas: `DIACRITICS`, `SEPARATORS`.

Operaciones para localizar en la fuente: `phrase`, `compact`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AlbumJdbcDao]], [[ArtistJdbcDao]], [[ArtistServiceImpl]], [[PostServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/SearchText.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchText.java>), líneas 1–36.

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
