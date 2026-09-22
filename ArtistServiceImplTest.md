---
title: "ArtistServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java"]
---

# ArtistServiceImplTest

Uses MockitoExtension, mocked dependencies and InjectMocks to exercise service logic directly. These tests check the assertions listed in the exact source below. They do not create a Spring transaction or async proxy and therefore do not establish real rollback or scheduling behavior.

## Connections

Project types referenced: [[Artist]], [[ArtistDao]], [[ArtistServiceImpl]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java, lines 1–119](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java>)

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
    public void testFindOrCreateWhenNameHasAccentsPreservesLettersInNormalizedIdentity() {
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
    public void testFindSuggestionsWhenQueryHasAccentsAndSeparatorsSearchesWithNormalizedText() {
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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
