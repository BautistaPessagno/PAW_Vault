---
title: "PostServiceImplTest"
categories: ["Services", "Testing"]
type: "test"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java"]
---

# PostServiceImplTest

Tests de `PostServiceImpl` en `services`: 52 casos declarados. Cubre: normalización de la búsqueda, filtros inválidos, paginación, publicar, editar con galería, eliminar y bloqueos. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `USERNAME`, `PUBLISHER_EMAIL`, `PUBLISHER_LOCALE`, `PUBLISHER_ID`, `TITLE`, `ARTIST_NAME`, `RELEASE_YEAR`, `GENRE`, `COVER_IMAGE_ID`, `COVER_CONTENT_TYPE`, `COVER_DATA`, `PNG_DATA`, `PRICE`, `DESCRIPTION`, `CONDITION`, `PRESSING_YEAR`, `ZONE`, `PROFILE_PAGE_SIZE`, `CATALOG_PAGE_SIZE`, `MAX_QUERY_LENGTH`, `postDao`, `userService`, `artistService`, `albumService`, `imageService`, `inquiryDao`, `postService`.

Operaciones para localizar en la fuente: `setUp`, `testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery`, `testSearchWhenPageCannotProduceAValidOffsetThrowsPageNotFoundException`, `ignoresEveryFilter`, `pngUpload`, `user`, `summary`, `criteria`.

Casos declarados: 52.

- `testPublishWhenPublisherAlreadyPostedAlbumReturnsDuplicatePostException`
- `testPublishWhenConcurrentInsertDuplicatesPostReturnsDuplicatePostException`
- `testPublishWhenCatalogIdentityExistsReturnsPostForExistingAlbum`
- `testPublishWhenOptionalTextDetailsAreBlankReturnsPostWithNullTextAndRequiredValues`
- `testPublishWhenTextDetailsHaveSurroundingSpacesReturnsPostWithTrimmedText`
- `testPublishWhenReleaseYearIsFutureReturnsInvalidPostDataException`
- `testPublishWhenPriceIsNotPositiveReturnsInvalidPostDataException`
- `testPublishWhenPressingYearPrecedesReleaseYearReturnsInvalidPostDataException`
- `testPublishWhenSixImagesAreSubmittedReturnsInvalidImageException`
- `testPublishWhenSeveralPhotosAreSubmittedReturnsPostWithFirstAsLeadAndRestAsGallery`
- `testFindDetailWhenPostHasExtraImagesReturnsCoverThenExtras`
- `testFindDetailWhenPublisherViewsAvailablePostReturnsOwnedAndEditable`
- `testFindDetailWhenAnotherUserViewsAvailablePostReturnsNotOwnedAndNotEditable`
- `testFindDetailWhenModeratorViewsAnotherUsersAvailablePostReturnsEditable`
- `testFindDetailWhenModeratorViewsSoldPostReturnsNotEditable`
- `testFindDetailWhenPostDoesNotExistThrowsPostNotFoundException`
- `testFindEditableByIdWhenPostIsAvailableReturnsPost`
- `testFindEditableByIdWhenPostIsSoldThrowsPostUnavailableException`
- `testUpdateWhenPostIsAvailableReturnsUpdatedPostAndPreservesCover`
- `testUpdateWhenPostIsSoldThrowsPostUnavailableException`
- `testUpdateWhenPrimaryImageIsRemovedReturnsPromotedExtraImage`
- `testUpdateWhenImageRemovalBelongsToAnotherPostReturnsInvalidImageException`
- `testUpdateWhenAlbumFallbackIsSubmittedForRemovalReturnsInvalidImageException`
- `testUpdateWhenExistingAndNewPhotosExceedGalleryLimitReturnsInvalidImageException`
- `testUpdateWhenPriceExceedsLimitReturnsInvalidPostDataException`
- `testDeleteWhenPostIsAvailableReturnsDetachedInquiries`
- `testDeleteWhenPostHasOwnAndGalleryPhotosReturnsAndDeletesEveryUploadedPhoto`
- `testDeleteWhenPostIsReservedThrowsPostUnavailableException`
- `testDeleteWhenPostIsSoldThrowsPostUnavailableException`
- `testDeleteWhenPostDoesNotExistThrowsPostNotFoundException`
- `testSearchWhenSortIsMissingReturnsNewestAsAppliedSort`
- `testSearchWhenSortIsGivenReturnsItAsAppliedSort`
- `testSearchWhenFirstPageOfThirtyOneMatchesReturnsFifteenWithTotalPages`
- `testSearchWhenSecondPageHasRowsReturnsPageWithPreviousAndCorrectOffset`
- `testSearchWhenPageIsPastTheLastOneThrowsPageNotFoundException`
- `testFindSearchSuggestionsWhenQueryHasSeparatorsSearchesWithNormalizedText`
- `testFindSearchSuggestionsWhenQueryHasNoLettersOrDigitsReturnsEmptyList`
- `testSearchWhenQueryHasAccentsReturnsPostsMatchedByNormalizedText`
- `testSearchWhenQueryHasNoLettersOrDigitsReturnsEmptyPage`
- `testFindByPublisherIdWhenSecondPageOfFortyPostsReturnsPageWithTotal`
- `testFindAvailableByPublisherIdWhenSecondPageOfThirtyPostsReturnsLastPageWithoutNext`
- `testFindAvailableByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException`
- `testFindByPublisherIdWhenTotalIsAMultipleOfThePageSizeReturnsLastPageWithoutNext`
- `testFindByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException`
- `testFindByPublisherIdWhenPublisherHasNoPostsReturnsEmptyFirstPage`
- `testSearchWhenQueryHasSurroundingSpacesReturnsMatchesForTrimmedQueryWithSort`
- `testSearchWhenQueryHasMaxLengthReturnsMatches`
- `testSearchWhenQueryExceedsMaxLengthReturnsInvalidSearchQueryException`
- `testSearchWhenQueryIsBlankAndSortIsGivenReturnsFeaturedPostsInThatOrder`
- `testSearchWhenFiltersAreOutOfRangeReturnsResultsWithoutApplyingThem`
- `testSearchWhenPriceRangeIsExactReturnsResultsWithBothBounds`
- `testSearchWhenYearIsFutureReturnsResultsWithoutYearFilter`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[Genre]], [[Image]], [[ImageService]], [[ImageUpload]], [[InMemoryImageService]], [[InquiryDao]], [[InvalidImageException]], [[InvalidPostDataException]], [[InvalidSearchQueryException]], [[PageNotFoundException]], [[Post]], [[PostDao]], [[PostDetail]], [[PostNotFoundException]], [[PostPage]], [[PostSearchCriteria]], [[PostServiceImpl]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[PublicUserProfile]], [[SearchResult]], [[SearchSuggestion]], [[SearchSuggestionType]], [[User]], [[UserRole]], [[UserService]], [[VinylInputRules]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>), líneas 1–1061.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchSuggestionType;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.UserRole;
import ar.edu.itba.paw.models.VinylInputRules;
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
    // Un PNG completo: el InMemoryImageService aplica ImageRules como el service real.
    private static final byte[] PNG_DATA = {(byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};
    private static final int PRICE = 45000;
    private static final String DESCRIPTION = "Prensado japones.";
    private static final Condition CONDITION = Condition.USED;
    private static final Integer PRESSING_YEAR = 2015;
    private static final String ZONE = "Palermo";
    private static final int PROFILE_PAGE_SIZE = 15;
    private static final int CATALOG_PAGE_SIZE = 15;
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
                List.of(new ImageUpload(COVER_CONTENT_TYPE, COVER_DATA)));

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
                List.of(new ImageUpload(COVER_CONTENT_TYPE, COVER_DATA)));

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
                PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                List.of(new ImageUpload(COVER_CONTENT_TYPE, COVER_DATA)));

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
                PRICE, "   ", CONDITION, null, "", List.of());

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
                List.of(new ImageUpload(COVER_CONTENT_TYPE, COVER_DATA)));

        // 3. Assert
        Assertions.assertEquals(DESCRIPTION, result.getDescription());
        Assertions.assertEquals(ZONE, result.getZone());
    }

    @Test
    public void testPublishWhenReleaseYearIsFutureReturnsInvalidPostDataException() {
        // 1. Arrange
        final int futureYear = VinylInputRules.currentYear() + 1;

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                futureYear, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, List.of());

        // 3. Assert
        Assertions.assertThrows(InvalidPostDataException.class, publish);
    }

    @Test
    public void testPublishWhenPriceIsNotPositiveReturnsInvalidPostDataException() {
        // 1. Arrange
        final int invalidPrice = 0;

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, invalidPrice, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, List.of());

        // 3. Assert
        Assertions.assertThrows(InvalidPostDataException.class, publish);
    }

    @Test
    public void testPublishWhenPressingYearPrecedesReleaseYearReturnsInvalidPostDataException() {
        // 1. Arrange
        final int pressingYear = RELEASE_YEAR - 1;

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, pressingYear, ZONE, List.of());

        // 3. Assert
        Assertions.assertThrows(InvalidPostDataException.class, publish);
    }

    @Test
    public void testPublishWhenSixImagesAreSubmittedReturnsInvalidImageException() {
        // 1. Arrange
        final List<ImageUpload> uploads = Collections.nCopies(6,
                new ImageUpload(COVER_CONTENT_TYPE, COVER_DATA));

        // 2. Exercise
        final Executable publish = () -> postService.publish(PUBLISHER_ID, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, uploads);

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, publish);
    }

    @Test
    public void testPublishWhenSeveralPhotosAreSubmittedReturnsPostWithFirstAsLeadAndRestAsGallery() {
        // 1. Arrange
        final InMemoryImageService images = new InMemoryImageService(COVER_IMAGE_ID);
        final PostServiceImpl service = new PostServiceImpl(postDao, inquiryDao, userService, artistService,
                albumService, images);
        final User publisher = user(PUBLISHER_ID, USERNAME, PUBLISHER_EMAIL);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, null);
        final long postId = 2;
        Mockito.when(userService.findById(PUBLISHER_ID)).thenReturn(Optional.of(publisher));
        Mockito.when(artistService.findOrCreate(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.findOrCreate(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(postDao.create(publisher.getId(), album.getId(), PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR,
                ZONE, COVER_IMAGE_ID)).thenReturn(new Post(postId, publisher.getId(), album.getId(), PRICE,
                DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, COVER_IMAGE_ID, PostStatus.AVAILABLE));

        // 2. Exercise
        final Post result = service.publish(PUBLISHER_ID, TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, PRICE,
                DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, Collections.nCopies(3, pngUpload()));

        // 3. Assert
        Assertions.assertEquals(COVER_IMAGE_ID, result.getImageId());
        Assertions.assertEquals(List.of(COVER_IMAGE_ID + 1, COVER_IMAGE_ID + 2), images.findGalleryImageIds(postId));
    }

    @Test
    public void testFindDetailWhenPostHasExtraImagesReturnsCoverThenExtras() {
        // 1. Arrange
        final PostSummary post = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(post.getId())).thenReturn(Optional.of(post));
        Mockito.when(imageService.findGalleryImageIds(post.getId())).thenReturn(List.of(4L, 5L));

        // 2. Exercise
        final PostDetail result = postService.findDetail(post.getId(), null, false);

        // 3. Assert
        Assertions.assertEquals(List.of(COVER_IMAGE_ID, 4L, 5L), result.getGalleryImageIds());
    }

    @Test
    public void testFindDetailWhenPublisherViewsAvailablePostReturnsOwnedAndEditable() {
        // 1. Arrange
        final PostSummary post = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        final PublicUserProfile seller = new PublicUserProfile(PUBLISHER_ID, USERNAME, null);
        Mockito.when(postDao.findById(post.getId())).thenReturn(Optional.of(post));
        Mockito.when(userService.findPublicProfileById(PUBLISHER_ID)).thenReturn(Optional.of(seller));

        // 2. Exercise
        final PostDetail result = postService.findDetail(post.getId(), PUBLISHER_ID, false);

        // 3. Assert
        Assertions.assertSame(seller, result.getSeller());
        Assertions.assertTrue(result.isOwnedByViewer());
        Assertions.assertTrue(result.isEditable());
    }

    @Test
    public void testFindDetailWhenAnotherUserViewsAvailablePostReturnsNotOwnedAndNotEditable() {
        // 1. Arrange
        final PostSummary post = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(post.getId())).thenReturn(Optional.of(post));

        // 2. Exercise
        final PostDetail result = postService.findDetail(post.getId(), PUBLISHER_ID + 1, false);

        // 3. Assert
        Assertions.assertFalse(result.isOwnedByViewer());
        Assertions.assertFalse(result.isEditable());
    }

    @Test
    public void testFindDetailWhenModeratorViewsAnotherUsersAvailablePostReturnsEditable() {
        // 1. Arrange
        final PostSummary post = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(post.getId())).thenReturn(Optional.of(post));

        // 2. Exercise
        final PostDetail result = postService.findDetail(post.getId(), PUBLISHER_ID + 1, true);

        // 3. Assert
        Assertions.assertTrue(result.isEditable());
    }

    @Test
    public void testFindDetailWhenModeratorViewsSoldPostReturnsNotEditable() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID, PostStatus.SOLD);
        Mockito.when(postDao.findById(sold.getId())).thenReturn(Optional.of(sold));

        // 2. Exercise
        final PostDetail result = postService.findDetail(sold.getId(), PUBLISHER_ID + 1, true);

        // 3. Assert
        Assertions.assertFalse(result.isEditable());
    }

    @Test
    public void testFindDetailWhenPostDoesNotExistThrowsPostNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.findById(1)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable find = () -> postService.findDetail(1, null, false);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, find);
    }

    @Test
    public void testFindEditableByIdWhenPostIsAvailableReturnsPost() {
        // 1. Arrange
        final PostSummary expected = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(expected));

        // 2. Exercise
        final PostSummary result = postService.findEditableById(1);

        // 3. Assert
        Assertions.assertSame(expected, result);
    }

    @Test
    public void testFindEditableByIdWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable find = () -> postService.findEditableById(1);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, find);
    }

    @Test
    public void testUpdateWhenPostIsAvailableReturnsUpdatedPostAndPreservesCover() {
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
        final PostSummary result = postService.update(1, album.getTitle(), artist.getName(),
                album.getReleaseYear(), album.getGenre(), 60000, DESCRIPTION, Condition.NEW,
                2022, ZONE, List.of(), List.of());

        // 3. Assert
        Assertions.assertSame(expected, result);
        Assertions.assertEquals(COVER_IMAGE_ID, result.getCoverImageId());
        Assertions.assertEquals("Dynamo", result.getTitle());
        Assertions.assertEquals(60000, result.getPrice());
        Assertions.assertEquals(PUBLISHER_ID, result.getUserId());
    }

    @Test
    public void testUpdateWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable update = () -> postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE, List.of(), List.of());

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, update);
    }

    @Test
    public void testUpdateWhenPrimaryImageIsRemovedReturnsPromotedExtraImage() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        final Artist artist = new Artist(1, ARTIST_NAME);
        final Album album = new Album(1, TITLE, artist.getId(), RELEASE_YEAR, GENRE, null);
        final PostSummary updated = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, 4L);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.of(COVER_IMAGE_ID));
        Mockito.when(imageService.findGalleryImageIds(1)).thenReturn(List.of(4L));
        Mockito.when(artistService.resolveForEdit(ARTIST_NAME)).thenReturn(artist);
        Mockito.when(albumService.resolveForEdit(TITLE, artist.getId(), RELEASE_YEAR, GENRE)).thenReturn(album);
        Mockito.when(postDao.updateWithImage(1, album.getId(), PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, 4L)).thenReturn(true);
        Mockito.when(postDao.findById(1)).thenReturn(Optional.of(updated));

        // 2. Exercise
        final PostSummary result = postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                List.of(), List.of(COVER_IMAGE_ID));

        // 3. Assert
        Assertions.assertEquals(4L, result.getCoverImageId());
    }

    @Test
    public void testUpdateWhenImageRemovalBelongsToAnotherPostReturnsInvalidImageException() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.of(COVER_IMAGE_ID));

        // 2. Exercise
        final Executable update = () -> postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                List.of(), List.of(99L));

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, update);
    }

    @Test
    public void testUpdateWhenAlbumFallbackIsSubmittedForRemovalReturnsInvalidImageException() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable update = () -> postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                List.of(), List.of(COVER_IMAGE_ID));

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, update);
    }

    @Test
    public void testUpdateWhenExistingAndNewPhotosExceedGalleryLimitReturnsInvalidImageException() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.of(COVER_IMAGE_ID));
        Mockito.when(imageService.findGalleryImageIds(1)).thenReturn(List.of(4L, 5L, 6L));

        // 2. Exercise
        final Executable update = () -> postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, PRICE, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                Collections.nCopies(2, pngUpload()), List.of());

        // 3. Assert
        Assertions.assertThrows(InvalidImageException.class, update);
    }

    @Test
    public void testUpdateWhenPriceExceedsLimitReturnsInvalidPostDataException() {
        // 1. Arrange
        final int invalidPrice = VinylInputRules.MAX_PRICE + 1;

        // 2. Exercise
        final Executable update = () -> postService.update(1, TITLE, ARTIST_NAME,
                RELEASE_YEAR, GENRE, invalidPrice, DESCRIPTION, CONDITION, PRESSING_YEAR, ZONE,
                List.of(), List.of());

        // 3. Assert
        Assertions.assertThrows(InvalidPostDataException.class, update);
    }

    @Test
    public void testDeleteWhenPostIsAvailableReturnsDetachedInquiries() {
        // 1. Arrange
        final PostSummary existing = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(existing));
        Mockito.when(inquiryDao.detachFromPost(1)).thenReturn(3);
        Mockito.when(postDao.delete(1)).thenReturn(true);

        // 2. Exercise
        final int detached = postService.delete(1);

        // 3. Assert
        Assertions.assertEquals(3, detached);
    }

    @Test
    public void testDeleteWhenPostHasOwnAndGalleryPhotosReturnsAndDeletesEveryUploadedPhoto() {
        // 1. Arrange
        final InMemoryImageService images = new InMemoryImageService(COVER_IMAGE_ID);
        final PostServiceImpl service = new PostServiceImpl(postDao, inquiryDao, userService, artistService,
                albumService, images);
        final long ownImageId = images.create(COVER_CONTENT_TYPE, PNG_DATA).getId();
        final long galleryImageId = images.create(COVER_CONTENT_TYPE, PNG_DATA).getId();
        images.replaceGallery(1, List.of(galleryImageId));
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(
                summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, ownImageId)));
        Mockito.when(postDao.findOwnImageId(1)).thenReturn(Optional.of(ownImageId));
        Mockito.when(postDao.delete(1)).thenReturn(true);

        // 2. Exercise
        final int detached = service.delete(1);

        // 3. Assert
        Assertions.assertEquals(0, detached);
        Assertions.assertFalse(images.contains(ownImageId));
        Assertions.assertFalse(images.contains(galleryImageId));
    }

    @Test
    public void testDeleteWhenPostIsReservedThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary reserved = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.RESERVED);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(reserved));

        // 2. Exercise
        final Executable delete = () -> postService.delete(1);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, delete);
    }

    @Test
    public void testDeleteWhenPostIsSoldThrowsPostUnavailableException() {
        // 1. Arrange
        final PostSummary sold = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID,
                PostStatus.SOLD);
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.of(sold));

        // 2. Exercise
        final Executable delete = () -> postService.delete(1);

        // 3. Assert
        Assertions.assertThrows(PostUnavailableException.class, delete);
    }

    @Test
    public void testDeleteWhenPostDoesNotExistThrowsPostNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.findByIdForUpdate(1)).thenReturn(Optional.empty());

        // 2. Exercise
        final Executable delete = () -> postService.delete(1);

        // 3. Assert
        Assertions.assertThrows(PostNotFoundException.class, delete);
    }

    @Test
    public void testSearchWhenSortIsMissingReturnsNewestAsAppliedSort() {
        // 1. Arrange
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(0);

        // 2. Exercise
        final SearchResult result = postService.search(criteria(null, null), 1);

        // 3. Assert
        Assertions.assertEquals(PostSort.NEWEST, result.getSort());
    }

    @Test
    public void testSearchWhenSortIsGivenReturnsItAsAppliedSort() {
        // 1. Arrange
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(0);

        // 2. Exercise
        final SearchResult result = postService.search(criteria(null, PostSort.PRICE_ASC), 1);

        // 3. Assert
        Assertions.assertEquals(PostSort.PRICE_ASC, result.getSort());
    }

    @ParameterizedTest
    @NullSource
    @ValueSource(strings = {"", "   "})
    public void testSearchWhenQueryIsNullOrBlankReturnsFeaturedPostsWithoutQuery(final String query) {
        // 1. Arrange
        final PostSummary featured = new PostSummary(1, 1, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
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
    public void testSearchWhenFirstPageOfThirtyOneMatchesReturnsFifteenWithTotalPages() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < CATALOG_PAGE_SIZE; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(31);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0))).thenReturn(rows);

        // 2. Exercise
        final SearchResult result = postService.search(criteria(null, PostSort.NEWEST), 1);

        // 3. Assert
        Assertions.assertEquals(CATALOG_PAGE_SIZE, result.getPage().getPosts().size());
        Assertions.assertEquals(1, result.getPage().getPageNumber());
        Assertions.assertEquals(3, result.getPage().getTotalPages());
        Assertions.assertEquals(31, result.getTotal());
        Assertions.assertFalse(result.getPage().isHasPrevious());
        Assertions.assertTrue(result.getPage().isHasNext());
    }

    @Test
    public void testSearchWhenSecondPageHasRowsReturnsPageWithPreviousAndCorrectOffset() {
        // 1. Arrange
        final PostSummary remaining = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class)))
                .thenReturn(CATALOG_PAGE_SIZE + 1);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(CATALOG_PAGE_SIZE)))
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
    public void testSearchWhenPageIsPastTheLastOneThrowsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class)))
                .thenReturn(CATALOG_PAGE_SIZE);

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
    public void testSearchWhenQueryHasAccentsReturnsPostsMatchedByNormalizedText() {
        // 1. Arrange
        final PostSummary match = new PostSummary(2, 2, PUBLISHER_EMAIL, PUBLISHER_LOCALE, 1,
                TITLE, ARTIST_NAME, RELEASE_YEAR, GENRE, COVER_IMAGE_ID, PRICE, DESCRIPTION, CONDITION,
                PRESSING_YEAR, ZONE, PostStatus.AVAILABLE);
        Mockito.when(postDao.countSearch(ArgumentMatchers.argThat(c -> "formulavol1".equals(c.getQuery()))))
                .thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.argThat(c -> "formulavol1".equals(c.getQuery())),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(match));

        // 2. Exercise
        final SearchResult result = postService.search(criteria("Fórmula, vol. 1", null), 1);

        // 3. Assert
        Assertions.assertEquals("Fórmula, vol. 1", result.getQuery());
        Assertions.assertEquals(List.of(match), result.getPage().getPosts());
    }

    @Test
    public void testSearchWhenQueryHasNoLettersOrDigitsReturnsEmptyPage() {
        // 1. Arrange
        final String query = "%_";

        // 2. Exercise
        final SearchResult result = postService.search(criteria(query, null), 1);

        // 3. Assert
        Assertions.assertTrue(result.getPage().getPosts().isEmpty());
    }

    @Test
    public void testFindByPublisherIdWhenSecondPageOfFortyPostsReturnsPageWithTotal() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < PROFILE_PAGE_SIZE; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(40);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, PROFILE_PAGE_SIZE, PROFILE_PAGE_SIZE)).thenReturn(rows);

        // 2. Exercise
        final PostPage result = postService.findByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertEquals(PROFILE_PAGE_SIZE, result.getPosts().size());
        Assertions.assertEquals(2, result.getPageNumber());
        Assertions.assertEquals(3, result.getTotalPages());
        Assertions.assertTrue(result.isHasPrevious());
        Assertions.assertTrue(result.isHasNext());
    }

    @Test
    public void testFindAvailableByPublisherIdWhenSecondPageOfThirtyPostsReturnsLastPageWithoutNext() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < PROFILE_PAGE_SIZE; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countAvailableByPublisherId(PUBLISHER_ID)).thenReturn(2 * PROFILE_PAGE_SIZE);
        Mockito.when(postDao.findAvailableByPublisherId(PUBLISHER_ID, PROFILE_PAGE_SIZE, PROFILE_PAGE_SIZE))
                .thenReturn(rows);

        // 2. Exercise
        final PostPage result = postService.findAvailableByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertEquals(PROFILE_PAGE_SIZE, result.getPosts().size());
        Assertions.assertEquals(2, result.getTotalPages());
        Assertions.assertTrue(result.isHasPrevious());
        Assertions.assertFalse(result.isHasNext());
    }

    @Test
    public void testFindAvailableByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.countAvailableByPublisherId(PUBLISHER_ID)).thenReturn(PROFILE_PAGE_SIZE);

        // 2. Exercise
        final Executable find = () -> postService.findAvailableByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, find);
    }

    @Test
    public void testFindByPublisherIdWhenTotalIsAMultipleOfThePageSizeReturnsLastPageWithoutNext() {
        // 1. Arrange
        final List<PostSummary> rows = new ArrayList<>();
        for (int index = 0; index < PROFILE_PAGE_SIZE; index += 1) {
            rows.add(summary(PUBLISHER_ID, TITLE + index, ARTIST_NAME, PRICE, COVER_IMAGE_ID));
        }
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(PROFILE_PAGE_SIZE * 2);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, PROFILE_PAGE_SIZE, PROFILE_PAGE_SIZE)).thenReturn(rows);

        // 2. Exercise
        final PostPage result = postService.findByPublisherId(PUBLISHER_ID, 2);

        // 3. Assert
        Assertions.assertEquals(PROFILE_PAGE_SIZE, result.getPosts().size());
        Assertions.assertEquals(2, result.getTotalPages());
        Assertions.assertFalse(result.isHasNext());
        Assertions.assertTrue(result.isHasPrevious());
    }

    @Test
    public void testFindByPublisherIdWhenPageIsPastTheLastOneReturnsPageNotFoundException() {
        // 1. Arrange
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(40);

        // 2. Exercise
        final Executable findPage = () -> postService.findByPublisherId(PUBLISHER_ID, 4);

        // 3. Assert
        Assertions.assertThrows(PageNotFoundException.class, findPage);
    }

    @Test
    public void testFindByPublisherIdWhenPublisherHasNoPostsReturnsEmptyFirstPage() {
        // 1. Arrange
        Mockito.when(postDao.countByPublisherId(PUBLISHER_ID)).thenReturn(0);
        Mockito.when(postDao.findByPublisherId(PUBLISHER_ID, PROFILE_PAGE_SIZE, 0)).thenReturn(List.of());

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
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
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
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(0);

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
        Mockito.when(postDao.countSearch(ArgumentMatchers.any(PostSearchCriteria.class))).thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.any(PostSearchCriteria.class),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
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
        Mockito.when(postDao.countSearch(ArgumentMatchers.argThat(PostServiceImplTest::ignoresEveryFilter)))
                .thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.argThat(PostServiceImplTest::ignoresEveryFilter),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(outOfRange, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(featured, result.getPage().getPosts().get(0));
    }

    @Test
    public void testSearchWhenPriceRangeIsExactReturnsResultsWithBothBounds() {
        // 1. Arrange
        final PostSummary match = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        final PostSearchCriteria exactPrice = new PostSearchCriteria(
                null, PostSort.PRICE_ASC, null, null, null, null, PRICE, PRICE);
        Mockito.when(postDao.countSearch(ArgumentMatchers.argThat(criteria ->
                        Integer.valueOf(PRICE).equals(criteria.getMinPrice())
                                && Integer.valueOf(PRICE).equals(criteria.getMaxPrice()))))
                .thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.argThat(criteria ->
                        Integer.valueOf(PRICE).equals(criteria.getMinPrice())
                                && Integer.valueOf(PRICE).equals(criteria.getMaxPrice())),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(match));

        // 2. Exercise
        final SearchResult result = postService.search(exactPrice, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(match, result.getPage().getPosts().get(0));
    }

    @Test
    public void testSearchWhenYearIsFutureReturnsResultsWithoutYearFilter() {
        // 1. Arrange
        final PostSummary featured = summary(PUBLISHER_ID, TITLE, ARTIST_NAME, PRICE, COVER_IMAGE_ID);
        final PostSearchCriteria futureYear = new PostSearchCriteria(null, PostSort.NEWEST, null, null,
                null, VinylInputRules.currentYear() + 1, null, null);
        Mockito.when(postDao.countSearch(ArgumentMatchers.argThat(criteria -> criteria.getReleaseYear() == null)))
                .thenReturn(1);
        Mockito.when(postDao.search(ArgumentMatchers.argThat(criteria -> criteria.getReleaseYear() == null),
                ArgumentMatchers.eq(CATALOG_PAGE_SIZE), ArgumentMatchers.eq(0)))
                .thenReturn(Collections.singletonList(featured));

        // 2. Exercise
        final SearchResult result = postService.search(futureYear, 1);

        // 3. Assert
        Assertions.assertEquals(1, result.getPage().getPosts().size());
        Assertions.assertSame(featured, result.getPage().getPosts().get(0));
    }

    // Stubbea el DAO solo para los criterios que tiene que recibir: un artista no positivo,
    // un anio fuera del catalogo y un rango de precios dado vuelta se ignoran, y sin orden
    // pedido queda el default.
    private static boolean ignoresEveryFilter(final PostSearchCriteria criteria) {
        return criteria.getSort() == PostSort.NEWEST && criteria.getArtistId() == null
                && criteria.getReleaseYear() == null && criteria.getMinPrice() == null
                && criteria.getMaxPrice() == null;
    }

    private static ImageUpload pngUpload() {
        return new ImageUpload(COVER_CONTENT_TYPE, PNG_DATA);
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
