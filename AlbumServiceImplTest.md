---
title: "AlbumServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java"]
---

# AlbumServiceImplTest

Uses MockitoExtension, mocked dependencies and InjectMocks to exercise service logic directly. These tests check the assertions listed in the exact source below. They do not create a Spring transaction or async proxy and therefore do not establish real rollback or scheduling behavior.

Production connections: [[Album]], [[AlbumDao]], [[AlbumServiceImpl]].

## Test cases

- `testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbum`

## Exact test source

[services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java, lines 1–45](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
public class AlbumServiceImplTest {

    @Mock
    private AlbumDao albumDao;

    @InjectMocks
    private AlbumServiceImpl albumService;

    @Test
    public void testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbum() {
        // 1. Arrange
        final String title = "  VERSUS  ";
        final String normalizedTitle = "versus";
        final long artistId = 1;
        final int releaseYear = 1997;
        final String defaultCoverPath = "/images/covers/versus.png";
        final String storedCoverPath = "/images/covers/original.png";
        final Album expected = new Album(1, normalizedTitle, artistId, releaseYear, storedCoverPath);
        Mockito.when(albumDao.findOrCreate(normalizedTitle, artistId, releaseYear, defaultCoverPath))
                .thenReturn(expected);

        // 2. Exercise
        final Album result = albumService.findOrCreate(title, artistId, releaseYear);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(normalizedTitle, result.getTitle());
        Assertions.assertEquals(artistId, result.getArtistId());
        Assertions.assertEquals(releaseYear, result.getReleaseYear());
        Assertions.assertEquals(storedCoverPath, result.getCoverPath());
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
