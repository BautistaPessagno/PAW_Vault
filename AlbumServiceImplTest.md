---
title: "AlbumServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java"]
---

# AlbumServiceImplTest

Four Mockito tests cover preserving an existing album cover, storing a cover for a new album, and new albums with null or empty bytes. These compare returned values with mocked persistence; they do not exercise database rollback or image validation under a Spring proxy.

## Test methods

- `testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbumWithItsCover`
- `testFindOrCreateWhenAlbumIsNewAndCoverProvidedReturnsAlbumWithStoredCover`
- `testFindOrCreateWhenAlbumIsNewAndCoverIsNullReturnsAlbumWithoutCover`
- `testFindOrCreateWhenAlbumIsNewAndCoverIsEmptyReturnsAlbumWithoutCover`

These are source assertions, not a fresh passing test run.

## Connections

Project types referenced: [[Album]], [[AlbumDao]], [[AlbumServiceImpl]], [[Image]], [[ImageService]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java, lines 1–110](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Image;
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

    private static final String TITLE = "  VERSUS  ";
    private static final String NORMALIZED_TITLE = "versus";
    private static final long ARTIST_ID = 1;
    private static final int RELEASE_YEAR = 1997;
    private static final String COVER_CONTENT_TYPE = "image/png";
    private static final byte[] COVER_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47};

    @Mock
    private AlbumDao albumDao;

    @Mock
    private ImageService imageService;

    @InjectMocks
    private AlbumServiceImpl albumService;

    @Test
    public void testFindOrCreateWhenIdentityMatchesExistingAlbumReturnsStoredAlbumWithItsCover() {
        // 1. Arrange
        final Long storedCoverImageId = 5L;
        final Album expected = new Album(1, NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, storedCoverImageId);
        Mockito.when(albumDao.findByArtistTitleYear(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.of(expected));

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR,
                COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(NORMALIZED_TITLE, result.getTitle());
        Assertions.assertEquals(ARTIST_ID, result.getArtistId());
        Assertions.assertEquals(RELEASE_YEAR, result.getReleaseYear());
        Assertions.assertEquals(storedCoverImageId, result.getCoverImageId());
    }

    @Test
    public void testFindOrCreateWhenAlbumIsNewAndCoverProvidedReturnsAlbumWithStoredCover() {
        // 1. Arrange
        final Image storedCover = new Image(7, COVER_CONTENT_TYPE, COVER_DATA);
        final Album expected = new Album(2, NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, storedCover.getId());
        Mockito.when(albumDao.findByArtistTitleYear(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.empty());
        Mockito.when(imageService.create(COVER_CONTENT_TYPE, COVER_DATA)).thenReturn(storedCover);
        Mockito.when(albumDao.create(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, storedCover.getId()))
                .thenReturn(expected);

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR,
                COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(storedCover.getId(), result.getCoverImageId());
    }

    @Test
    public void testFindOrCreateWhenAlbumIsNewAndCoverIsNullReturnsAlbumWithoutCover() {
        // 1. Arrange
        final Album expected = new Album(2, NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, null);
        Mockito.when(albumDao.findByArtistTitleYear(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.empty());
        Mockito.when(albumDao.create(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, null))
                .thenReturn(expected);

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR, null, null);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertNull(result.getCoverImageId());
    }

    @Test
    public void testFindOrCreateWhenAlbumIsNewAndCoverIsEmptyReturnsAlbumWithoutCover() {
        // 1. Arrange
        final byte[] emptyCover = {};
        final Album expected = new Album(2, NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, null);
        Mockito.when(albumDao.findByArtistTitleYear(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR))
                .thenReturn(Optional.empty());
        Mockito.when(albumDao.create(NORMALIZED_TITLE, ARTIST_ID, RELEASE_YEAR, null))
                .thenReturn(expected);

        // 2. Exercise
        final Album result = albumService.findOrCreate(TITLE, ARTIST_ID, RELEASE_YEAR,
                COVER_CONTENT_TYPE, emptyCover);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertNull(result.getCoverImageId());
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
