---
title: "PostServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java"]
---

# PostServiceImplTest

Five Mockito tests cover pre-existing duplicate, duplicate-key race translation, reusing catalog identity, normal contact return and missing Post. Calls use the cover arguments and request Locale. The normal contact case asserts no exception, not the normalized notification payload. No ConcurrentPublishException or transaction rollback test is present.

## Test methods

- `testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException`
- `testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException`
- `testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum`
- `testNotifyInterestWhenPostExistsReturnsNormally`
- `testNotifyInterestWhenPostDoesNotExistReturnsPostNotFoundExceptionWithoutEmail`

These are source assertions, not a fresh passing test run.

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[EmailService]], [[Post]], [[PostDao]], [[PostNotFoundException]], [[PostServiceImpl]], [[PostSummary]], [[User]], [[UserService]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java, lines 1–147](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.PostDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Locale;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class PostServiceImplTest {

    private static final String USERNAME = "publisher";
    private static final String PUBLISHER_EMAIL = "publisher@example.com";
    private static final String TITLE = "versus";
    private static final String ARTIST_NAME = "illya kuryaki and the valderramas";
    private static final int RELEASE_YEAR = 1997;
    private static final Long COVER_IMAGE_ID = 1L;
    private static final String COVER_CONTENT_TYPE = "image/png";
    private static final byte[] COVER_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47};
    private static final Locale LOCALE = Locale.ENGLISH;

    @Mock
    private PostDao postDao;

    @Mock
    private UserService userService;

    @Mock
    private ArtistService artistService;

    @Mock
    private AlbumService albumService;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private PostServiceImpl postService;

    @Test
    public void testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException() {
        // 1. Arrange
        final User publisher = new User(1, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_IMAGE_ID);
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(album);
        Mockito.when(postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())).thenReturn(true);

        // 2. Exercise
        final Executable publish = () -> postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException() {
        // 1. Arrange
        final User publisher = new User(1, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_IMAGE_ID);
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId()))
                .thenThrow(new DuplicatePostKeyException());

        // 2. Exercise
        final Executable publish = () -> postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum() {
        // 1. Arrange
        final User publisher = new User(1, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_IMAGE_ID);
        final Post expected = new Post(2, publisher.getId(), album.getId());
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId())).thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, COVER_CONTENT_TYPE, COVER_DATA, LOCALE);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(publisher.getId(), result.getUserId());
        Assertions.assertEquals(album.getId(), result.getAlbumId());
    }

    @Test
    public void testNotifyInterestWhenPostExistsReturnsNormally() {
        // 1. Arrange
        final long postId = 1;
        final String publisherEmail = "publisher@example.com";
        final PostSummary post = new PostSummary(postId, 1, publisherEmail, 1, "versus",
                "illya kuryaki and the valderramas", 1997, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(postId)).thenReturn(Optional.of(post));

        // 2. Exercise
        final Executable notifyInterest =
                () -> postService.notifyInterest(postId, "  Tadeo Gorganchian  ", "  Tadeo@Example.COM  ", LOCALE);

        // 3. Assert
        Assertions.assertDoesNotThrow(notifyInterest);
    }

    @Test
    public void testNotifyInterestWhenPostDoesNotExistReturnsPostNotFoundExceptionWithoutEmail() {
        // 1. Arrange
        final long missingPostId = 404;
        Mockito.when(postDao.findById(missingPostId)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable notifyInterest =
                () -> postService.notifyInterest(missingPostId, "Tadeo", "tadeo@example.com", LOCALE);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, notifyInterest);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
