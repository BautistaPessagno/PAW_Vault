---
title: "ArtistServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java"]
---

# ArtistServiceImplTest

Uses MockitoExtension, mocked dependencies and InjectMocks to exercise service logic directly. These tests check the assertions listed in the exact source below. They do not create a Spring transaction or async proxy and therefore do not establish real rollback or scheduling behavior.

Production connections: [[Artist]], [[ArtistDao]], [[ArtistServiceImpl]].

## Test cases

- `testFindOrCreateWhenNameMatchesExistingArtistReturnsNormalizedArtist`

## Exact test source

[services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java>)

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

@ExtendWith(MockitoExtension.class)
public class ArtistServiceImplTest {

    @Mock
    private ArtistDao artistDao;

    @InjectMocks
    private ArtistServiceImpl artistService;

    @Test
    public void testFindOrCreateWhenNameMatchesExistingArtistReturnsNormalizedArtist() {
        // 1. Arrange
        final String name = "  ILLYA KURYAKI AND THE VALDERRAMAS  ";
        final String normalizedName = "illya kuryaki and the valderramas";
        final Artist expected = new Artist(1, normalizedName);
        Mockito.when(artistDao.findOrCreate(normalizedName)).thenReturn(expected);

        // 2. Exercise
        final Artist result = artistService.findOrCreate(name);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(normalizedName, result.getName());
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
