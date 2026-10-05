---
title: "ArtistServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java"]
---

# ArtistServiceImplTest

Tests de `ArtistServiceImpl` en `services`: 6 casos declarados. Cubre: identidad normalizada, edición del nombre visible y sugerencias. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `artistDao`, `artistService`.

Casos declarados: 6.

- `testFindOrCreateWhenNameHasOuterSpacesReturnsTrimmedArtist`
- `testFindOrCreateWhenNameHasDifferentSeparatorsReturnsExistingArtist`
- `testFindOrCreateWhenNameHasAccentsReturnsArtistMatchingItsNormalizedIdentity`
- `testResolveForEditWhenDisplayNameChangesReturnsUpdatedArtist`
- `testFindSuggestionsWhenQueryHasAccentsAndSeparatorsReturnsSuggestionsForNormalizedText`
- `testFindSuggestionsWhenQueryHasNoLettersOrDigitsReturnsEmptyList`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Artist]], [[ArtistDao]], [[ArtistServiceImpl]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java>), líneas 1–119.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.persistence.ArtistDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

@ExtendWith(MockitoExtension.class)
public class ArtistServiceImplTest {

    @Mock
    private ArtistDao artistDao;

    @InjectMocks
    private ArtistServiceImpl artistService;

    @Test
    public void testFindOrCreateWhenNameHasOuterSpacesReturnsTrimmedArtist() {
        // 1. Arrange
        final String name = "  Illya Kuryaki and the Valderramas  ";
        final String trimmedName = "Illya Kuryaki and the Valderramas";
        final String normalizedName = "illyakuryakiandthevalderramas";
        final Artist expected = new Artist(1, trimmedName);
        Mockito.when(artistDao.findOrCreate(trimmedName, normalizedName)).thenReturn(expected);

        // 2. Exercise
        final Artist result = artistService.findOrCreate(name);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(trimmedName, result.getName());
    }

    @Test
    public void testFindOrCreateWhenNameHasDifferentSeparatorsReturnsExistingArtist() {
        // 1. Arrange
        final String name = "  MICHAEL-JACKSON  ";
        final String displayName = "MICHAEL-JACKSON";
        final String normalizedName = "michaeljackson";
        final Artist expected = new Artist(2, "Michael Jackson");
        Mockito.when(artistDao.findOrCreate(displayName, normalizedName)).thenReturn(expected);

        // 2. Exercise
        final Artist result = artistService.findOrCreate(name);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(expected.getName(), result.getName());
    }

    @Test
    public void testFindOrCreateWhenNameHasAccentsReturnsArtistMatchingItsNormalizedIdentity() {
        // 1. Arrange
        final String name = "  Charly-García  ";
        final String displayName = "Charly-García";
        final String normalizedName = "charlygarcía";
        final Artist expected = new Artist(3, "Charly García");
        Mockito.when(artistDao.findOrCreate(displayName, normalizedName)).thenReturn(expected);

        // 2. Exercise
        final Artist result = artistService.findOrCreate(name);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(expected.getName(), result.getName());
    }

    @Test
    public void testResolveForEditWhenDisplayNameChangesReturnsUpdatedArtist() {
        // 1. Arrange
        final String requestedName = "  MICHAEL-JACKSON  ";
        final String displayName = "MICHAEL-JACKSON";
        final String normalizedName = "michaeljackson";
        final Artist existing = new Artist(2, "Michael Jackson");
        final Artist updated = new Artist(2, displayName);
        Mockito.when(artistDao.findOrCreate(displayName, normalizedName)).thenReturn(existing);
        Mockito.when(artistDao.updateDisplayName(existing.getId(), displayName))
                .thenReturn(updated);

        // 2. Exercise
        final Artist result = artistService.resolveForEdit(requestedName);

        // 3. Assert
        Assertions.assertEquals(existing.getId(), result.getId());
        Assertions.assertEquals(displayName, result.getName());
    }

    @Test
    public void testFindSuggestionsWhenQueryHasAccentsAndSeparatorsReturnsSuggestionsForNormalizedText() {
        // 1. Arrange
        final List<Artist> expected = List.of(new Artist(2, "Charly García"));
        Mockito.when(artistDao.findSuggestions("charlygarcia", 5)).thenReturn(expected);

        // 2. Exercise
        final List<Artist> result = artistService.findSuggestions("  Charly-García  ");

        // 3. Assert
        Assertions.assertEquals(expected, result);
    }

    @Test
    public void testFindSuggestionsWhenQueryHasNoLettersOrDigitsReturnsEmptyList() {
        // 1. Arrange
        final String query = "   ---   ";

        // 2. Exercise
        final List<Artist> result = artistService.findSuggestions(query);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }
}
```
