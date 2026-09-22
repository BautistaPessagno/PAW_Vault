---
title: "AlbumServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java"]
---

# AlbumServiceImplTest

Service tests with mocks or a capturing mail sender. Direct construction does not activate transaction or async proxies. Source evidence for [[AlbumServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbumWithItsCover`
- `testFindOrCreateWhenAlbumIsNewReturnsAlbumWithoutExemplarImage`
- `testResolveForEditWhenMetadataChangesReturnsUpdatedAlbum`

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumServiceImpl]], [[Genre]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java, lines 1–88](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.persistence.AlbumDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class AlbumServiceImplTest {

    private static final String TITLE = "  Versus  ";
    private static final String TRIMMED_TITLE = "Versus";
    private static final long ARTIST_ID = 1;
    private static final int RELEASE_YEAR = 1997;
    private static final Genre GENRE = Genre.HIP_HOP;

    @Mock
    private AlbumDao albumDao;

    @InjectMocks
    private AlbumServiceImpl albumService;

    @Test
    public void testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbumWithItsCover() {
        // 1. Arrange
        final Long storedCoverImageId = 5L;
        final Album expected = new Album(1, TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR, GENRE, storedCoverImageId);
        Mockito.when(albumDao.findByArtistTitleYear(TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.of(expected));

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR, GENRE);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(TRIMMED_TITLE, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(RELEASE_YEAR, result.getReleaseYear());
        Assertions.assertEquals(storedCoverImageId, result.getCoverImageId());
    }

    @Test
    public void testFindOrCreateWhenAlbumIsNewReturnsAlbumWithoutExemplarImage() {
        // 1. Arrange
        final Album expected = new Album(2, TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR, GENRE, null);
        Mockito.when(albumDao.findByArtistTitleYear(TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.empty());
        Mockito.when(albumDao.create(TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR, GENRE))
                .thenReturn(expected);

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR, GENRE);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertNull(result.getCoverImageId());
    }

    @Test
    public void testResolveForEditWhenMetadataChangesReturnsUpdatedAlbum() {
        // 1. Arrange
        final Genre updatedGenre = Genre.SOUL_FUNK;
        final Album existing = new Album(1, "versus", ARTIST_ID, RELEASE_YEAR, GENRE, 5L);
        final Album updated = new Album(1, TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR, updatedGenre, 5L);
        Mockito.when(albumDao.findByArtistTitleYear(TRIMMED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.of(existing));
        Mockito.when(albumDao.updateMetadata(existing.getId(), TRIMMED_TITLE, updatedGenre))
                .thenReturn(updated);

        // 2. Exercise
        final Album result = albumService.resolveForEdit(TITLE, ARTIST_ID, RELEASE_YEAR, updatedGenre);

        // 3. Assert
        Assertions.assertEquals(existing.getId(), result.getId());
        Assertions.assertEquals(TRIMMED_TITLE, result.getTitle());
        Assertions.assertEquals(updatedGenre, result.getGenre());
        Assertions.assertEquals(existing.getCoverImageId(), result.getCoverImageId());
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
