---
title: "PostServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
sources: ["services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java"]
---

# PostServiceImplTest

Uses MockitoExtension, mocked dependencies and InjectMocks to exercise service logic directly. These tests check the assertions listed in the exact source below. They do not create a Spring transaction or async proxy and therefore do not establish real rollback or scheduling behavior. The successful notifyInterest test only asserts no exception; it does not assert the normalized notification fields. Missing-post and delivery-failure tests assert exceptions. No test here exercises the ConcurrentPublishException branch with a real database race.

Production connections: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[EmailDeliveryException]], [[EmailService]], [[Post]], [[PostDao]], [[PostNotFoundException]], [[PostServiceImpl]], [[PostSummary]], [[User]], [[UserService]].

## Test cases

- `testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException`
- `testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException`
- `testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum`
- `testNotifyInterestWhenPostExistsReturnsNormally`
- `testNotifyInterestWhenPostDoesNotExistReturnsPostNotFoundExceptionWithoutEmail`
- `testNotifyInterestWhenDeliveryFailsReturnsEmailDeliveryException`

## Exact test source

[services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java, lines 1–162](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.PostDao;
import ar.edu.itba.paw.services.exceptions.EmailDeliveryException;
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
    private static final String COVER_PATH = "/images/covers/versus.png";
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
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_PATH);
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR)).thenReturn(album);
        Mockito.when(postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())).thenReturn(true);

        // 2. Exercise
        final Executable publish = () -> postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException() {
        // 1. Arrange
        final User publisher = new User(1, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_PATH);
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR)).thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId()))
                .thenThrow(new DuplicatePostKeyException());

        // 2. Exercise
        final Executable publish = () -> postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, LOCALE);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum() {
        // 1. Arrange
        final User publisher = new User(1, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, COVER_PATH);
        final Post expected = new Post(2, publisher.getId(), album.getId());
        Mockito.when(userService.findOrCreate(USERNAME, PUBLISHER_EMAIL, LOCALE)).thenReturn(publisher);
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR)).thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId())).thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(
                USERNAME, PUBLISHER_EMAIL, TITLE, ARTIST_NAME, RELEASE_YEAR, LOCALE);

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
                "illya kuryaki and the valderramas", 1997, "/images/covers/versus.png");
        Mockito.when(postDao.findById(postId)).thenReturn(Optional.of(post));

        // 2. Exercise
        final Executable notifyInterest =
                () -> postService.notifyInterest(postId, "  Tadeo Gorganchian  ", "  Tadeo@Example.COM  ");

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
                () -> postService.notifyInterest(missingPostId, "Tadeo", "tadeo@example.com");

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, notifyInterest);
    }

    @Test
    public void testNotifyInterestWhenDeliveryFailsReturnsEmailDeliveryException() {
        // 1. Arrange
        final long postId = 1;
        final PostSummary post = new PostSummary(postId, 1, "publisher@example.com", 1,
                "versus", "illya kuryaki and the valderramas", 1997,
                "/images/covers/versus.png");
        Mockito.when(postDao.findById(postId)).thenReturn(Optional.of(post));
        Mockito.doThrow(new EmailDeliveryException("delivery failed", new RuntimeException()))
                .when(emailService).sendPostInterestEmail(Mockito.any());

        // 2. Exercise
        final Executable notifyInterest =
                () -> postService.notifyInterest(postId, "Tadeo", "tadeo@example.com");

        // 3. Assert
        Assertions.assertThrows(EmailDeliveryException.class, notifyInterest);
    }
}
```

[[Testing and evidence]] · [[Source inventory]]
