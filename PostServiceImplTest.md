---
title: "PostServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java"]
---

# PostServiceImplTest

Service tests with mocks or a capturing mail sender. Direct construction does not activate transaction or async proxies. Source evidence for [[PostServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException`
- `testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException`
- `testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum`
- `testPublishWhenOptionalDetailsAreBlankReturnsPostWithNullTextAndDefaultStock`
- `testPublishWhenTextDetailsHaveSurroundingSpacesReturnsPostWithTrimmedText`
- `testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery`
- `testSearchWhenQueryHasSurroundingSpacesReturnsMatchesForTrimmedQueryWithSort`
- `testSearchWhenQueryHasMaxLengthReturnsMatches`
- `testSearchWhenQueryExceedsMaxLengthReturnsInvalidSearchQueryException`
- `testSearchWhenQueryIsBlankAndSortIsGivenReturnsFeaturedPostsInThatOrder`
- `testSearchWhenFiltersAreOutOfRangeReturnsResultsWithoutApplyingThem`

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[Genre]], [[Image]], [[ImageService]], [[InvalidSearchQueryException]], [[Post]], [[PostDao]], [[PostSearchCriteria]], [[PostServiceImpl]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[SearchResult]], [[User]], [[UserRole]], [[UserService]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java, lines 1–322](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.PostDao;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.mockito.ArgumentMatchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Collections;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class PostServiceImplTest {

    private static final String USERNAME = "publisher";
    private static final String PUBLISHER_EMAIL = "publisher@example.com";
    private static final String PUBLISHER_LOCALE = "es";
    private static final long PUBLISHER_ID = 1;
    private static final String TITLE = "versus";
    private static final String ARTIST_NAME = "illya kuryaki and the valderramas";
    private static final int RELEASE_YEAR = 1997;
    private static final Genre GENRE = Genre.HIP_HOP;
    private static final Long COVER_IMAGE_ID = 1L;
    private static final String COVER_CONTENT_TYPE = "image/png";
    private static final byte[] COVER_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47};
    private static final int PRICE = 45000;
    private static final String DESCRIPTION = "Prensado japones.";
    private static final Condition CONDITION = Condition.USED;
    private static final Integer PRESSING_YEAR = 2015;
    private static final String ZONE = "Palermo";
    private static final int RESULT_LIMIT = 16;
    private static final int MAX_QUERY_LENGTH = 255;

    @Mock
    private PostDao postDao;

    @Mock
    private UserService userService;

    @Mock
    private ArtistService artistService;

    @Mock
    private AlbumService albumService;

    @Mock
    private ImageService imageService;

    private PostServiceImpl postService;

    @BeforeEach
    public void setUp() {
        postService = new PostServiceImpl(postDao, userService, artistService, albumService, imageService);
    }

    @Test
    public void testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, COVER_IMAGE_ID);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())).thenReturn(true);

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, COVER_IMAGE_ID);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(imageService.create(COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(new Image(COVER_IMAGE_ID, COVER_CONTENT_TYPE, COVER_DATA));
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR,
                ZONE, COVER_IMAGE_ID)).thenThrow(new DuplicatePostKeyException());

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostException.class, publish);
    }

    @Test
    public void testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, COVER_IMAGE_ID);
        final Post expected = new Post(2, publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, COVER_IMAGE_ID, PostStatus.AVAILABLE);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(imageService.create(COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(new Image(COVER_IMAGE_ID, COVER_CONTENT_TYPE, COVER_DATA));
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR,
                ZONE, COVER_IMAGE_ID)).thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE,
                PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertEquals(publisher.getId(), result.getUserId());
        Assertions.assertEquals(album.getId(), result.getAlbumId());
        Assertions.assertEquals(PRICE, result.getPrice());
        Assertions.assertEquals(CONDITION, result.getCondition());
        Assertions.assertEquals(ZONE, result.getZone());
        Assertions.assertEquals(COVER_IMAGE_ID, result.getImageId());
        Assertions.assertEquals(PostStatus.AVAILABLE, result.getStatus());
    }

    @Test
    public void testPublishWhenOptionalDetailsAreBlankReturnsPostWithNullTextAndDefaultStock() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, null, null);
        final Post expected = new Post(2, publisher.getId(), album.getId(), PRICE, null, null, null, null,
                null, PostStatus.AVAILABLE);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, null))
                .thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, null, null, null, null, null))
                .thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME, RELEASE_YEAR, null,
                PRICE, "   ", null, null, "", null, null);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertNull(result.getDescription());
        Assertions.assertNull(result.getZone());
        Assertions.assertNull(result.getImageId());
    }

    @Test
    public void testPublishWhenTextDetailsHaveSurroundingSpacesReturnsPostWithTrimmedText() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, COVER_IMAGE_ID);
        final Post expected = new Post(2, publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, COVER_IMAGE_ID, PostStatus.AVAILABLE);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(imageService.create(COVER_CONTENT_TYPE, COVER_DATA))
                .thenReturn(new Image(COVER_IMAGE_ID, COVER_CONTENT_TYPE, COVER_DATA));
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR,
                ZONE, COVER_IMAGE_ID)).thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE,
                PRICE, "  " + DESCRIPTION + "  ", CONDITION, PRESSING_YEAR, "  " + ZONE + " ",
                COVER_CONTENT_TYPE, COVER_DATA);

        // 3. Assert
        Assertions.assertEquals(DESCRIPTION, result.getDescription());
        Assertions.assertEquals(ZONE, result.getZone());
    }

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"", "   "})
    public void testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery(final String query) {
        // 1. Arrange
        final PostSummary featured = new PostSummary(1, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class), ArgumentMatchers.eq(RESULT_LIMIT)))
                .thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(criteria(query, null));

        // 3. Assert
        Assertions.assertNull(result.getQuery());
        Assertions.assertEquals(1, result.getPosts().size());
        Assertions.assertSame(featured, result.getPosts().get(0));
    }

    @Test
    public void testSearchWhenQueryHasSurroundingSpacesReturnsMatchesForTrimmedQueryWithSort() {
        // 1. Arrange
        final PostSummary match = new PostSummary(2, 2, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class), ArgumentMatchers.eq(RESULT_LIMIT)))
                .thenReturn(Collections.singletonList(match));

        // 2. Exercise
        final SearchResult result = postService.search(criteria("  versus  ", PostSort.PRICE_ASC));

        // 3. Assert
        Assertions.assertEquals("versus", result.getQuery());
        Assertions.assertEquals(1, result.getPosts().size());
        Assertions.assertSame(match, result.getPosts().get(0));
    }

    @Test
    public void testSearchWhenQueryHasMaxLengthReturnsMatches() {
        // 1. Arrange
        final String query = "a".repeat(MAX_QUERY_LENGTH);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class), ArgumentMatchers.eq(RESULT_LIMIT)))
                .thenReturn(Collections.emptyList());

        // 2. Exercise
        final SearchResult result = postService.search(criteria(query, PostSort.NEWEST));

        // 3. Assert
        Assertions.assertEquals(query, result.getQuery());
        Assertions.assertTrue(result.getPosts().isEmpty());
    }

    @Test
    public void testSearchWhenQueryExceedsMaxLengthReturnsInvalidSearchQueryException() {
        // 1. Arrange
        final String query = "a".repeat(MAX_QUERY_LENGTH + 1);

        // 2. Exercise
        final Executable search = () -> postService.search(criteria(query, PostSort.NEWEST));

        // 3. Assert
        Assertions.assertThrows(InvalidSearchQueryException.class, search);
    }

    @Test
    public void testSearchWhenQueryIsBlankAndSortIsGivenReturnsFeaturedPostsInThatOrder() {
        // 1. Arrange
        final PostSummary cheapest = new PostSummary(3, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 2,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class), ArgumentMatchers.eq(RESULT_LIMIT)))
                .thenReturn(Collections.singletonList(cheapest));

        // 2. Exercise
        final SearchResult result = postService.search(criteria("", PostSort.PRICE_ASC));

        // 3. Assert
        Assertions.assertEquals(1, result.getPosts().size());
        Assertions.assertSame(cheapest, result.getPosts().get(0));
    }

    @Test
    public void testSearchWhenFiltersAreOutOfRangeReturnsResultsWithoutApplyingThem() {
        // 1. Arrange
        final PostSummary featured = new PostSummary(4, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        final PostSearchCriteria outOfRange = new PostSearchCriteria(
                null, null, null, null, 0L, 999, 50_000, 40_000);
        Mockito.when(postDao.search(ArgumentMatchers.argThat(PostServiceImplTest::ignoresEveryFilter),
                ArgumentMatchers.eq(RESULT_LIMIT))).thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(outOfRange);

        // 3. Assert
        Assertions.assertEquals(1, result.getPosts().size());
        Assertions.assertSame(featured, result.getPosts().get(0));
    }

    // El service no devuelve los criterios ya normalizados, asi que la unica forma de
    // observarlos es stubbear el DAO solo para los que tiene que recibir: un artista no
    // positivo, un anio fuera del catalogo y un rango de precios dado vuelta se ignoran,
    // y sin orden pedido queda el default.
    private static boolean ignoresEveryFilter(final PostSearchCriteria criteria) {
        return criteria.getSort() == PostSort.NEWEST && criteria.getArtistId() == null
                && criteria.getReleaseYear() == null && criteria.getMinPrice() == null
                && criteria.getMaxPrice() == null;
    }

    private static User user(final long id, final String username, final String email) {
        return new User(id, username, email, "$2a$12$hash", UserRole.USER, true, "es");
    }

    private static PostSearchCriteria criteria(final String query, final PostSort sort) {
        return new PostSearchCriteria(query, sort, null, null, null, null, null, null);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
