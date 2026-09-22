---
title: "PostServiceImplTest"
categories: ["Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java"]
---

# PostServiceImplTest

Service tests with mocks or a capturing mail sender. Direct construction does not activate transaction or async proxies. Source evidence for [[PostServiceImpl]]; no new Maven execution is claimed.

Test methods in this revision:

- `testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException`
- `testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException`
- `testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum`
- `testPublishWhenOptionalTextDetailsAreBlankReturnsPostWithNullTextAndRequiredValues`
- `testPublishWhenTextDetailsHaveSurroundingSpacesReturnsPostWithTrimmedText`
- `testFindEditableByIdWhenPublisherOwnsAvailablePostReturnsPost`
- `testFindEditableByIdWhenAnotherUserOwnsPostThrowsForbiddenOperationException`
- `testFindEditableByIdWhenPostIsSoldThrowsPostUnavailableException`
- `testUpdateWhenPublisherOwnsPostReturnsUpdatedPostAndPreservesCover`
- `testUpdateWhenAnotherUserOwnsPostThrowsForbiddenOperationException`
- `testUpdateWhenPostIsSoldThrowsPostUnavailableException`
- `testDeleteWhenPublisherOwnsAvailablePostReturnsWithoutError`
- `testDeleteWhenAnotherUserOwnsPostThrowsForbiddenOperationException`
- `testDeleteWhenPostIsSoldThrowsPostUnavailableException`
- `testDeleteWhenPostDoesNotExistThrowsPostNotFoundException`
- `testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery`
- `testSearchWhenFirstPageHasSixteenRowsReturnsFifteenWithNextPage`
- `testSearchWhenSecondPageHasRowsReturnsPageWithPreviousAndCorrectOffset`
- `testSearchWhenLaterPageIsEmptyThrowsPageNotFoundException`
- `testSearchWhenPageCannotProduceAValidOffsetThrowsPageNotFoundException`
- `testFindSearchSuggestionsWhenQueryHasSeparatorsSearchesWithNormalizedText`
- `testFindSearchSuggestionsWhenQueryHasNoLettersOrDigitsReturnsEmptyList`
- `testFindByPublisherIdWhenSecondPageOfTwentyFivePostsReturnsPageWithTotal`
- `testFindByPublisherIdWhenTotalIsAMultipleOfThePageSizeReturnsLastPageWithoutNext`
- `testFindByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException`
- `testFindByPublisherIdWhenPublisherHasNoPostsReturnsEmptyFirstPage`
- `testSearchWhenQueryHasSurroundingSpacesReturnsMatchesForTrimmedQueryWithSort`
- `testSearchWhenQueryHasMaxLengthReturnsMatches`
- `testSearchWhenQueryExceedsMaxLengthReturnsInvalidSearchQueryException`
- `testSearchWhenQueryIsBlankAndSortIsGivenReturnsFeaturedPostsInThatOrder`
- `testSearchWhenFiltersAreOutOfRangeReturnsResultsWithoutApplyingThem`

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[ForbiddenOperationException]], [[Genre]], [[Image]], [[ImageService]], [[InquiryDao]], [[InvalidSearchQueryException]], [[PageNotFoundException]], [[Post]], [[PostDao]], [[PostNotFoundException]], [[PostPage]], [[PostSearchCriteria]], [[PostServiceImpl]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[SearchResult]], [[SearchSuggestion]], [[SearchSuggestionType]], [[User]], [[UserRole]], [[UserService]].

Referenced by: none.

## Exact source

[services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java, lines 1–667](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchSuggestionType;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.InquiryDao;
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

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
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
    private static final int CATALOG_PAGE_SIZE = 15;
    private static final int CATALOG_QUERY_LIMIT = CATALOG_PAGE_SIZE + 1;
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

    @Mock
    private InquiryDao inquiryDao;

    private PostServiceImpl postService;

    @BeforeEach
    public void setUp() {
        postService = new PostServiceImpl(postDao, inquiryDao, userService, artistService, albumService,
                imageService);
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
    public void testPublishWhenOptionalTextDetailsAreBlankReturnsPostWithNullTextAndRequiredValues() {
        // 1. Arrange
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, null);
        final Post expected = new Post(2, publisher.getId(), album.getId(), PRICE, null, CONDITION, null, null,
                null, PostStatus.AVAILABLE);
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE))
                .thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, null, CONDITION, null, null, null))
                .thenReturn(expected);

        // 2. Exercise
        final Post result = postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE,
                PRICE, "   ", CONDITION, null, "", null, null);

        // 3. Assert
        Assertions.assertEquals(expected.getId(), result.getId());
        Assertions.assertNull(result.getDescription());
        Assertions.assertEquals(CONDITION, result.getCondition());
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

    @Test
    public void testFindEditableByIdWhenPublisherOwnsAvailablePostReturnsPost() {
        // 1. Arrange
        final PostSummary expected = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(expected));

        // 2. Exercise
        final PostSummary result = postService.findEditableById(1, PUBLISHER_ID);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testFindEditableByIdWhenAnotherUserOwnsPostThrowsForbiddenOperationException() {
        // 1. Arrange
        final PostSummary post = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(post));

        // 2. Exercise
        final Executable find = () -> postService.findEditableById(1, PUBLISHER_ID + 1);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, find);
    }

    @Test
    public void testFindEditableByIdWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable find = () -> postService.findEditableById(1, PUBLISHER_ID);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, find);
    }

    @Test
    public void testUpdateWhenPublisherOwnsPostReturnsUpdatedPostAndPreservesCover() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        final Artist artist = new Artist(2, "Soda Stereo");
        final Album album = new Album(2, "Dynamo", artist.getId(), 1992, Genre.ROCK, null);
        final PostSummary expected = summary(PUBLISHER_ID, album.getTitle(), artist.getName(), 60000,
                COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(artistService.resolveForEdit(artist.getName())).thenReturn(artist);
        Mockito.when(albumService.resolveForEdit(album.getTitle(), artist.getId(), album.getReleaseYear(),
                album.getGenre())).thenReturn(album);
        Mockito.when(postDao.update(1, album.getId(), 60000, DESCRIPTION, Condition.NEW,
                2022, ZONE)).thenReturn(true);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(expected));

        // 2. Exercise
        final PostSummary result = postService.update(1, PUBLISHER_ID, album.getTitle(), artist.getName(),
                album.getReleaseYear(), album.getGenre(), 60000, DESCRIPTION, Condition.NEW,
                2022, ZONE, null, null);

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertEquals(COVER_IMAGE_ID, result.getCoverImageId());
        Assertions.assertEquals("Dynamo", result.getTitle());
        Assertions.assertEquals(60000, result.getPrice());
    }

    @Test
    public void testUpdateWhenAnotherUserOwnsPostThrowsForbiddenOperationException() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));

        // 2. Exercise
        final Executable update = () -> postService.update(1, PUBLISHER_ID + 1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, null, null);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, update);
    }

    @Test
    public void testUpdateWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable update = () -> postService.update(1, PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, null, null);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, update);
    }

    @Test
    public void testDeleteWhenPublisherOwnsAvailablePostReturnsWithoutError() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.of(COVER_IMAGE_ID));
        Mockito.when(inquiryDao.detachFromPost(1)).thenReturn(3);
        Mockito.when(postDao.delete(1)).thenReturn(true);
        Mockito.when(imageService.delete(COVER_IMAGE_ID)).thenReturn(true);

        // 2. Exercise
        final Executable delete = () -> postService.delete(1, PUBLISHER_ID);

        // 3. Assert
        Assertions.assertDoesNotThrow(delete);
    }

    @Test
    public void testDeleteWhenAnotherUserOwnsPostThrowsForbiddenOperationException() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));

        // 2. Exercise
        final Executable delete = () -> postService.delete(1, PUBLISHER_ID + 1);

        // 3. Assert
        Assertions.assertThrows(ForbiddenOperationException.class, delete);
    }

    @Test
    public void testDeleteWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable delete = () -> postService.delete(1, PUBLISHER_ID);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, delete);
    }

    @Test
    public void testDeleteWhenPostDoesNotExistThrowsPostNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable delete = () -> postService.delete(1, PUBLISHER_ID);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, delete);
    }

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"", "   "})
    public void testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery(final String query) {
        // 1. Arrange
        final PostSummary featured = new PostSummary(1, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(criteria(query, null), 1);

        // 3. Assert
        Assertions.assertNull(result.getQuery());
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(featured, result.getPage().getPosts().get(0));
        Assertions.assertFalse(result.getPage().isHasPrevious());
        Assertions.assertFalse(result.getPage().isHasNext());
    }

    @Test
    public void testSearchWhenFirstPageHasSixteenRowsReturnsFifteenWithNextPage() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < CATALOG_QUERY_LIMIT; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0))).thenReturn(rows);

        // 2. Exercise
        final SearchResult result = postService.search(criteria(null, PostSort.NEWEST), 1);

        // 3. Assert
        Assertions.assertEquals(CATALOG_PAGE_SIZE, result.getPage().getPosts().size());
        Assertions.assertEquals(1, result.getPage().getPageNumber());
        Assertions.assertFalse(result.getPage().isTotalKnown());
        Assertions.assertFalse(result.getPage().isHasPrevious());
        Assertions.assertTrue(result.getPage().isHasNext());
    }

    @Test
    public void testSearchWhenSecondPageHasRowsReturnsPageWithPreviousAndCorrectOffset() {
        // 1. Arrange
        final PostSummary remaining = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(CATALOG_PAGE_SIZE)))
                .thenReturn(List.of(remaining));

        // 2. Exercise
        final SearchResult result = postService.search(criteria(null, PostSort.NEWEST), 2);

        // 3. Assert
        Assertions.assertEquals(List.of(remaining), result.getPage().getPosts());
        Assertions.assertEquals(2, result.getPage().getPageNumber());
        Assertions.assertTrue(result.getPage().isHasPrevious());
        Assertions.assertFalse(result.getPage().isHasNext());
    }

    @Test
    public void testSearchWhenLaterPageIsEmptyThrowsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(CATALOG_PAGE_SIZE)))
                .thenReturn(List.of());

        // 2. Exercise
        final Executable search = () -> postService.search(criteria(null, PostSort.NEWEST), 2);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, search);
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, Integer.MAX_VALUE})
    public void testSearchWhenPageCannotProduceAValidOffsetThrowsPageNotFoundException(final int pageNumber) {
        // 1. Arrange

        // 2. Exercise
        final Executable search = () -> postService.search(criteria(null, PostSort.NEWEST), pageNumber);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, search);
    }

    @Test
    public void testFindSearchSuggestionsWhenQueryHasSeparatorsSearchesWithNormalizedText() {
        // 1. Arrange
        final List<SearchSuggestion> expected = List.of(
                new SearchSuggestion(SearchSuggestionType.ARTIST, "Soda Stereo", null));
        Mockito.when(postDao.findSearchSuggestions("sodastereo", 5)).thenReturn(expected);

        // 2. Exercise
        final List<SearchSuggestion> result = postService.findSearchSuggestions("  Soda / Stereo ");

        // 3. Assert
        Assertions.assertEquals(expected, result);
    }

    @Test
    public void testFindSearchSuggestionsWhenQueryHasNoLettersOrDigitsReturnsEmptyList() {
        // 1. Arrange
        final String query = "   ---   ";

        // 2. Exercise
        final List<SearchSuggestion> result = postService.findSearchSuggestions(query);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByPublisherIdWhenSecondPageOfTwentyFivePostsReturnsPageWithTotal() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < 12; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(25);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, 12, 12)).thenReturn(rows);

        // 2. Exercise
        final PostPage result = postService.findByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertEquals(12, result.getPosts().size());
        Assertions.assertEquals(2, result.getPageNumber());
        Assertions.assertTrue(result.isTotalKnown());
        Assertions.assertEquals(3, result.getTotalPages());
        Assertions.assertTrue(result.isHasPrevious());
        Assertions.assertTrue(result.isHasNext());
    }

    @Test
    public void testFindByPublisherIdWhenTotalIsAMultipleOfThePageSizeReturnsLastPageWithoutNext() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < 12; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(24);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, 12, 12)).thenReturn(rows);

        // 2. Exercise
        final PostPage result = postService.findByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertEquals(12, result.getPosts().size());
        Assertions.assertEquals(2, result.getTotalPages());
        Assertions.assertFalse(result.isHasNext());
        Assertions.assertTrue(result.isHasPrevious());
    }

    @Test
    public void testFindByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(25);

        // 2. Exercise
        final Executable findPage = () -> postService.findByPublisherId(PUBLISHER_ID, 4);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindByPublisherIdWhenPublisherHasNoPostsReturnsEmptyFirstPage() {
        // 1. Arrange
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(0);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, 12, 0)).thenReturn(List.of());

        // 2. Exercise
        final PostPage result = postService.findByPublisherId(PUBLISHER_ID, 1);

        // 3. Assert
        Assertions.assertTrue(result.getPosts().isEmpty());
        Assertions.assertEquals(0, result.getTotalPages());
        Assertions.assertFalse(result.isHasPrevious());
        Assertions.assertFalse(result.isHasNext());
    }

    @Test
    public void testSearchWhenQueryHasSurroundingSpacesReturnsMatchesForTrimmedQueryWithSort() {
        // 1. Arrange
        final PostSummary match = new PostSummary(2, 2, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(match));

        // 2. Exercise
        final SearchResult result = postService.search(criteria("  versus  ", PostSort.PRICE_ASC), 1);

        // 3. Assert
        Assertions.assertEquals("versus", result.getQuery());
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(match, result.getPage().getPosts().get(0));
    }

    @Test
    public void testSearchWhenQueryHasMaxLengthReturnsMatches() {
        // 1. Arrange
        final String query = "a".repeat(MAX_QUERY_LENGTH);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.emptyList());

        // 2. Exercise
        final SearchResult result = postService.search(criteria(query, PostSort.NEWEST), 1);

        // 3. Assert
        Assertions.assertEquals(query, result.getQuery());
        Assertions.assertTrue(result.getPage().getPosts().isEmpty());
    }

    @Test
    public void testSearchWhenQueryExceedsMaxLengthReturnsInvalidSearchQueryException() {
        // 1. Arrange
        final String query = "a".repeat(MAX_QUERY_LENGTH + 1);

        // 2. Exercise
        final Executable search = () -> postService.search(criteria(query, PostSort.NEWEST), 1);

        // 3. Assert
        Assertions.assertThrows(InvalidSearchQueryException.class, search);
    }

    @Test
    public void testSearchWhenQueryIsBlankAndSortIsGivenReturnsFeaturedPostsInThatOrder() {
        // 1. Arrange
        final PostSummary cheapest = new PostSummary(3, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 2,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(cheapest));

        // 2. Exercise
        final SearchResult result = postService.search(criteria("", PostSort.PRICE_ASC), 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(cheapest, result.getPage().getPosts().get(0));
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
                ArgumentMatchers.eq(CATALOG_QUERY_LIMIT), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(outOfRange, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(featured, result.getPage().getPosts().get(0));
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

    private static PostSummary summary(final long userId, final String title, final String artistName,
                                       final int price, final Long coverImageId) {
        return summary(userId, title, artistName, price, coverImageId, PostStatus.AVAILABLE);
    }

    private static PostSummary summary(final long userId, final String title, final String artistName,
                                       final int price, final Long coverImageId, final PostStatus status) {
        return new PostSummary(1, userId, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                title, artistName, RELEASE_YEAR, GENRE, coverImageId, price, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, status);
    }

    private static PostSearchCriteria criteria(final String query, final PostSort sort) {
        return new PostSearchCriteria(query, sort, null, null, null, null, null, null);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
