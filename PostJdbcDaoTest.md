---
title: "PostJdbcDaoTest"
categories: ["Persistence", "Testing"]
type: "test"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java"]
---

# PostJdbcDaoTest

Tests de `PostJdbcDao` en `persistence`: 65 casos declarados. Cubre: búsqueda con filtros, órdenes, comodines literales, conteo, sugerencias, bloqueo, cambio de estado con guarda, edición y borrado. No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].

## Guía de lectura

Datos y dependencias declaradas: `USERS_TABLE`, `ARTISTS_TABLE`, `ALBUMS_TABLE`, `POSTS_TABLE`, `CART_ITEMS_TABLE`, `POST_ID`, `USER_ID`, `PUBLISHER_EMAIL`, `PUBLISHER_LOCALE`, `ALBUM_ID`, `ALBUM_TITLE`, `ARTIST_NAME`, `RELEASE_YEAR`, `GENRE`, `COVER_IMAGE_ID`, `PRICE`, `DETAILED_POST_ID`, `DETAILED_USER_ID`, `DETAILED_PRICE`, `DETAILED_DESCRIPTION`, `DETAILED_CONDITION`, `DETAILED_PRESSING_YEAR`, `DETAILED_ZONE`, `LIMIT`, `OTHER_POST_ID`, `SOLD_POST_ID`, `OTHER_ALBUM_ID`, `AVAILABLE_PAGE_SIZE`, `postDao`, `dataSource`, `jdbcTemplate`.

Operaciones para localizar en la fuente: `setUp`, `assertSuggestion`, `criteria`, `ids`.

Casos declarados: 65.

- `testFindFeaturedWhenPostsExistReturnsNewestByPublishDateWithMappedDetails`
- `testFindFeaturedWhenLimitIsSmallerThanPostsReturnsOnlyFirstOnes`
- `testSearchWhenOffsetIsGivenReturnsTheFollowingStableSlice`
- `testFindFeaturedWhenSortIsOldestReturnsOldestPublishDateFirst`
- `testFindFeaturedWhenPostIsCreatedReturnsItFirstByNewest`
- `testFindFeaturedWhenSortIsPriceAscReturnsCheapestFirst`
- `testFindFeaturedWhenSortIsPriceDescReturnsMostExpensiveFirst`
- `testFindFeaturedWhenSortIsTitleAscReturnsAlphabeticalThenNewest`
- `testFindFeaturedWhenSortIsTitleDescReturnsReverseAlphabetical`
- `testFindFeaturedWhenSortIsArtistAscReturnsAlphabeticalByArtist`
- `testFindFeaturedWhenSortIsArtistDescReturnsReverseAlphabeticalByArtist`
- `testFindFeaturedWhenSortIsReleaseYearDescReturnsLatestAlbumFirst`
- `testFindFeaturedWhenSortIsReleaseYearAscReturnsEarliestAlbumFirst`
- `testFindByIdWhenOptionalDetailsAreAbsentReturnsSummaryWithRequiredFields`
- `testFindByIdWhenPostDoesNotExistReturnsEmpty`
- `testExistsByUserIdAndAlbumIdWhenPostExistsReturnsTrue`
- `testCreateWhenPublisherAlreadyPostedSameAlbumReturnsDuplicatePostKeyExceptionWithoutChanges`
- `testCreateWhenAnotherPublisherPostsSameAlbumReturnsIndependentPostWithDetails`
- `testCreateWhenOptionalTextDetailsAreNullReturnsPostWithRequiredCondition`
- `testCreateWhenPriceIsNotPositiveThrowsDataIntegrityViolationWithoutPersistingPost`
- `testCreateWhenConditionIsNullThrowsDataIntegrityViolationWithoutPersistingPost`
- `testCreateWhenConditionIsUnknownThrowsDataIntegrityViolationWithoutPersistingPost`
- `testUpdateWhenPostExistsReturnsTrueAndPersistsEditableFields`
- `testUpdateWithoutImageWhenAlbumHasCoverPreservesPostImageId`
- `testUpdateWithNullImageWhenOwnPhotoIsRemovedReturnsNoOwnImage`
- `testUpdateWhenPostDoesNotExistReturnsFalse`
- `testUpdateWhenConditionIsNullThrowsDataIntegrityViolationWithoutChangingPost`
- `testUpdateStatusWhenPostIsInExpectedStateReturnsTrue`
- `testUpdateStatusWhenPostIsInAnotherStateReturnsFalse`
- `testSearchWhenPostIsReservedReturnsWithoutIt`
- `testFindFeaturedWhenAPostIsSoldReturnsOnlyTheAvailableOnes`
- `testFindByIdForUpdateWhenPostExistsReturnsPost`
- `testFindByIdsForUpdateWhenOneIdDoesNotExistReturnsTheOthersOrderedById`
- `testSearchWhenQueryMatchesPartOfAlbumTitleReturnsNewestFirst`
- `testSearchWhenSortIsPriceDescReturnsMatchesOrderedByPrice`
- `testSearchWhenQueryMatchesArtistNameReturnsPosts`
- `testSearchWhenQueryOmitsSpacesReturnsArtistPosts`
- `testSearchWhenLimitIsSmallerThanMatchesReturnsOnlyNewest`
- `testCountSearchWhenFilterMatchesSomePostsReturnsTheirCount`
- `testSearchWhenQueryMatchesNothingReturnsEmpty`
- `testSearchWhenQueryContainsWildcardsReturnsEmptyInsteadOfMatchingEverything`
- `testSearchWhenGenreIsGivenReturnsOnlyMatchingPosts`
- `testSearchWhenConditionIsGivenReturnsOnlyMatchingPosts`
- `testSearchWhenArtistAndYearAreGivenReturnsOnlyMatchingPosts`
- `testSearchWhenPriceRangeIsGivenReturnsOnlyPricedPostsInsideRange`
- `testSearchWhenAllFiltersAreCombinedReturnsIntersectionInRequestedOrder`
- `testFindSearchSuggestionsWhenQueryMatchesPrefixAndContentReturnsRankedResults`
- `testFindSearchSuggestionsWhenQueryOmitsSpacesReturnsExactMatch`
- `testFindSearchSuggestionsWhenQueryMatchesWordStartReturnsAlbumAndArtist`
- `testFindSearchSuggestionsWhenOnlySoldPostsMatchReturnsEmptyList`
- `testFindByPublisherIdWhenPostsExistReturnsRequestedOwnersSliceWithAllStatusesNewestFirst`
- `testFindAvailableByPublisherIdWhenFirstPageReturnsNewestAvailablePost`
- `testFindAvailableByPublisherIdWhenSecondPageReturnsOlderAvailablePostSkippingSold`
- `testFindAvailableByPublisherIdWhenPageIsPastTheLastOneReturnsEmptyList`
- `testCountAvailableByPublisherIdWhenOwnerHasSoldPostReturnsOnlyAvailable`
- `testFindByPublisherIdWhenUserHasNoPostsReturnsEmptyList`
- `testCountByPublisherIdWhenUserHasPostsReturnsTotal`
- `testCountByPublisherIdWhenUserHasNoPostsReturnsZero`
- `testFindSearchSuggestionsWhenLimitIsBelowMatchCountReturnsBestRanked`
- `testFindOwnImageIdWhenPostHasOwnImageReturnsImageId`
- `testFindOwnImageIdWhenPostOnlyHasAlbumCoverReturnsEmpty`
- `testFindAlbumCoverImageIdWhenAlbumHasCoverReturnsFallbackImage`
- `testDeleteWhenPostExistsReturnsTrueAndRemovesRow`
- `testDeleteWhenPostIsInACartReturnsTrueAndRemovesItsCartItems`
- `testDeleteWhenPostDoesNotExistReturnsFalse`

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[DuplicatePostKeyException]], [[Genre]], [[Post]], [[PostDao]], [[PostSearchCriteria]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[SearchSuggestion]], [[SearchSuggestionType]], [[TestConfiguration]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java>), líneas 1–1001.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchSuggestionType;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.function.Executable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.jdbc.JdbcTestUtils;
import org.springframework.transaction.annotation.Transactional;

import javax.sql.DataSource;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class PostJdbcDaoTest {

    private static final String USERS_TABLE = "users";
    private static final String ARTISTS_TABLE = "artists";
    private static final String ALBUMS_TABLE = "albums";
    private static final String POSTS_TABLE = "posts";
    private static final String CART_ITEMS_TABLE = "cart_items";
    private static final long POST_ID = 1;
    private static final long USER_ID = 1;
    private static final String PUBLISHER_EMAIL = "bpessagno@itba.edu.ar";
    private static final String PUBLISHER_LOCALE = "es";
    private static final long ALBUM_ID = 1;
    private static final String ALBUM_TITLE = "versus";
    private static final String ARTIST_NAME = "illya kuryaki and the valderramas";
    private static final int RELEASE_YEAR = 1997;
    private static final Genre GENRE = Genre.HIP_HOP;
    private static final long COVER_IMAGE_ID = 1;
    private static final int PRICE = 35000;
    private static final long DETAILED_POST_ID = 2;
    private static final long DETAILED_USER_ID = 2;
    private static final int DETAILED_PRICE = 45000;
    private static final String DETAILED_DESCRIPTION = "Prensado japones, tapa con leve desgaste.";
    private static final Condition DETAILED_CONDITION = Condition.USED;
    private static final int DETAILED_PRESSING_YEAR = 2015;
    private static final String DETAILED_ZONE = "Palermo";
    // Cualquier valor mayor a la cantidad de fixtures sirve: no depende del limite que use el service.
    private static final int LIMIT = 10;
    private static final long OTHER_POST_ID = 3;
    private static final long SOLD_POST_ID = 4;
    private static final long OTHER_ALBUM_ID = 2;
    // Una publicacion por pagina: las dos disponibles del usuario 1 ocupan dos paginas.
    private static final int AVAILABLE_PAGE_SIZE = 1;

    @Autowired
    private PostDao postDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testFindFeaturedWhenPostsExistReturnsNewestByPublishDateWithMappedDetails() {
        // 1. Arrange
        final int limit = 8;

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.NEWEST), limit, 0);

        // 3. Assert
        Assertions.assertEquals(3, result.size());
        Assertions.assertEquals(OTHER_POST_ID, result.get(0).getId());
        Assertions.assertEquals(POST_ID, result.get(1).getId());
        final PostSummary detailed = result.get(2);
        Assertions.assertEquals(DETAILED_POST_ID, detailed.getId());
        Assertions.assertEquals(DETAILED_USER_ID, detailed.getUserId());
        Assertions.assertEquals(ALBUM_ID, detailed.getAlbumId());
        Assertions.assertEquals(ALBUM_TITLE, detailed.getTitle());
        Assertions.assertEquals(ARTIST_NAME, detailed.getArtistName());
        Assertions.assertEquals(RELEASE_YEAR, detailed.getReleaseYear());
        Assertions.assertEquals(GENRE, detailed.getGenre());
        Assertions.assertEquals(COVER_IMAGE_ID, detailed.getCoverImageId());
        Assertions.assertEquals(DETAILED_PRICE, detailed.getPrice());
        Assertions.assertEquals(DETAILED_DESCRIPTION, detailed.getDescription());
        Assertions.assertEquals(DETAILED_CONDITION, detailed.getCondition());
        Assertions.assertEquals(DETAILED_PRESSING_YEAR, detailed.getPressingYear());
        Assertions.assertEquals(DETAILED_ZONE, detailed.getZone());
        Assertions.assertEquals(PostStatus.AVAILABLE, detailed.getStatus());
    }

    @Test
    public void testFindFeaturedWhenLimitIsSmallerThanPostsReturnsOnlyFirstOnes() {
        // 1. Arrange
        final int limit = 1;

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.NEWEST), limit, 0);

        // 3. Assert
        Assertions.assertEquals(1, result.size());
        Assertions.assertEquals(OTHER_POST_ID, result.get(0).getId());
    }

    @Test
    public void testSearchWhenOffsetIsGivenReturnsTheFollowingStableSlice() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.NEWEST), 2, 1);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsOldestReturnsOldestPublishDateFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.OLDEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(DETAILED_POST_ID, POST_ID, OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenPostIsCreatedReturnsItFirstByNewest() {
        // 1. Arrange

        // 2. Exercise
        final Post created = postDao.create(DETAILED_USER_ID, OTHER_ALBUM_ID, DETAILED_PRICE,
                DETAILED_DESCRIPTION, DETAILED_CONDITION, DETAILED_PRESSING_YEAR, DETAILED_ZONE, null);
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(created.getId(), result.get(0).getId());
    }

    @Test
    public void testFindFeaturedWhenSortIsPriceAscReturnsCheapestFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.PRICE_ASC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID, POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsPriceDescReturnsMostExpensiveFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.PRICE_DESC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(DETAILED_POST_ID, POST_ID, OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsTitleAscReturnsAlphabeticalThenNewest() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.TITLE_ASC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID, POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsTitleDescReturnsReverseAlphabetical() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.TITLE_DESC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID, OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsArtistAscReturnsAlphabeticalByArtist() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.ARTIST_ASC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID, OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsArtistDescReturnsReverseAlphabeticalByArtist() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.ARTIST_DESC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID, POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsReleaseYearDescReturnsLatestAlbumFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.RELEASE_YEAR_DESC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID, OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindFeaturedWhenSortIsReleaseYearAscReturnsEarliestAlbumFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.RELEASE_YEAR_ASC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID, POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindByIdWhenOptionalDetailsAreAbsentReturnsSummaryWithRequiredFields() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PostSummary> result = postDao.findById(POST_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        final PostSummary post = result.get();
        Assertions.assertEquals(POST_ID, post.getId());
        Assertions.assertEquals(USER_ID, post.getUserId());
        Assertions.assertEquals(PUBLISHER_EMAIL, post.getPublisherEmail());
        Assertions.assertEquals(PUBLISHER_LOCALE, post.getPublisherLocale());
        Assertions.assertEquals(ALBUM_ID, post.getAlbumId());
        Assertions.assertEquals(ALBUM_TITLE, post.getTitle());
        Assertions.assertEquals(ARTIST_NAME, post.getArtistName());
        Assertions.assertEquals(RELEASE_YEAR, post.getReleaseYear());
        Assertions.assertEquals(GENRE, post.getGenre());
        Assertions.assertEquals(COVER_IMAGE_ID, post.getCoverImageId());
        Assertions.assertEquals(PRICE, post.getPrice());
        Assertions.assertNull(post.getDescription());
        Assertions.assertEquals(Condition.USED, post.getCondition());
        Assertions.assertNull(post.getPressingYear());
        Assertions.assertNull(post.getZone());
        Assertions.assertEquals(PostStatus.AVAILABLE, post.getStatus());
    }

    @Test
    public void testFindByIdWhenPostDoesNotExistReturnsEmpty() {
        // 1. Arrange
        final long missingPostId = POST_ID + 999;

        // 2. Exercise
        final Optional<PostSummary> result = postDao.findById(missingPostId);

        // 3. Assert
        Assertions.assertFalse(result.isPresent());
    }

    @Test
    public void testExistsByUserIdAndAlbumIdWhenPostExistsReturnsTrue() {
        // 1. Arrange

        // 2. Exercise
        final boolean result = postDao.existsByUserIdAndAlbumId(USER_ID, ALBUM_ID);

        // 3. Assert
        Assertions.assertTrue(result);
    }

    @Test
    public void testCreateWhenPublisherAlreadyPostedSameAlbumReturnsDuplicatePostKeyExceptionWithoutChanges() {
        // 1. Arrange

        // 2. Exercise
        final Executable create = () -> postDao.create(USER_ID, ALBUM_ID, DETAILED_PRICE, null,
                Condition.USED, null, null, null);

        // 3. Assert
        Assertions.assertThrows(DuplicatePostKeyException.class, create);
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, USERS_TABLE));
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenAnotherPublisherPostsSameAlbumReturnsIndependentPostWithDetails() {
        // 1. Arrange
        final long userId = 3;

        // 2. Exercise
        final Post result = postDao.create(userId, ALBUM_ID, DETAILED_PRICE, DETAILED_DESCRIPTION,
                DETAILED_CONDITION, DETAILED_PRESSING_YEAR, DETAILED_ZONE, COVER_IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result.getId() >= 0);
        Assertions.assertEquals(userId, result.getUserId());
        Assertions.assertEquals(ALBUM_ID, result.getAlbumId());
        Assertions.assertEquals(DETAILED_PRICE, result.getPrice());
        Assertions.assertEquals(DETAILED_DESCRIPTION, result.getDescription());
        Assertions.assertEquals(DETAILED_CONDITION, result.getCondition());
        Assertions.assertEquals(DETAILED_PRESSING_YEAR, result.getPressingYear());
        Assertions.assertEquals(DETAILED_ZONE, result.getZone());
        Assertions.assertEquals(COVER_IMAGE_ID, result.getImageId());
        Assertions.assertEquals(PostStatus.AVAILABLE, result.getStatus());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + result.getId() +
                        " AND user_id = " + userId +
                        " AND album_id = " + ALBUM_ID +
                        " AND price = " + DETAILED_PRICE +
                        " AND description = '" + DETAILED_DESCRIPTION + "'" +
                        " AND item_condition = '" + DETAILED_CONDITION.name() + "'" +
                        " AND pressing_year = " + DETAILED_PRESSING_YEAR +
                        " AND zone = '" + DETAILED_ZONE + "'" +
                        " AND stock = 1 AND image_id = " + COVER_IMAGE_ID +
                        " AND status = 'AVAILABLE'"));
        Assertions.assertEquals(8, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
        Assertions.assertEquals(4, JdbcTestUtils.countRowsInTable(jdbcTemplate, ARTISTS_TABLE));
        Assertions.assertEquals(3, JdbcTestUtils.countRowsInTable(jdbcTemplate, ALBUMS_TABLE));
    }

    @Test
    public void testCreateWhenOptionalTextDetailsAreNullReturnsPostWithRequiredCondition() {
        // 1. Arrange
        final long userId = 3;

        // 2. Exercise
        final Post result = postDao.create(userId, ALBUM_ID, DETAILED_PRICE, null,
                Condition.USED, null, null, null);

        // 3. Assert
        Assertions.assertNull(result.getDescription());
        Assertions.assertEquals(Condition.USED, result.getCondition());
        Assertions.assertNull(result.getPressingYear());
        Assertions.assertNull(result.getZone());
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + result.getId() +
                        " AND price = " + DETAILED_PRICE +
                        " AND description IS NULL AND item_condition = 'USED'" +
                        " AND pressing_year IS NULL AND zone IS NULL" +
                        " AND stock = 1 AND image_id IS NULL AND status = 'AVAILABLE'"));
    }

    @Test
    public void testCreateWhenPriceIsNotPositiveThrowsDataIntegrityViolationWithoutPersistingPost() {
        // 1. Arrange
        final long userId = 3;
        final int invalidPrice = 0;

        // 2. Exercise
        final Executable create = () -> postDao.create(userId, ALBUM_ID, invalidPrice,
                null, Condition.USED, null, null, null);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, create);
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
    }

    @Test
    public void testCreateWhenConditionIsNullThrowsDataIntegrityViolationWithoutPersistingPost() {
        // 1. Arrange
        final long userId = 3;

        // 2. Exercise
        final Executable create = () -> postDao.create(userId, ALBUM_ID, DETAILED_PRICE,
                null, null, null, null, null);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, create);
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
    }

    @Test
    public void testCreateWhenConditionIsUnknownThrowsDataIntegrityViolationWithoutPersistingPost() {
        // 1. Arrange
        final long userId = 3;

        // 2. Exercise
        // El enum Condition impide que el DAO mande un valor desconocido: el INSERT directo prueba
        // que el CHECK de la migracion lo rechaza igual si alguien escribe por fuera de la app.
        final Executable create = () -> jdbcTemplate.update(
                "INSERT INTO posts (user_id, album_id, price, item_condition) VALUES (?, ?, ?, ?)",
                userId, ALBUM_ID, DETAILED_PRICE, "UNKNOWN");

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, create);
        Assertions.assertEquals(7, JdbcTestUtils.countRowsInTable(jdbcTemplate, POSTS_TABLE));
    }

    @Test
    public void testUpdateWhenPostExistsReturnsTrueAndPersistsEditableFields() {
        // 1. Arrange
        final int updatedPrice = 52000;
        final String updatedDescription = "Edicion remasterizada.";
        final String updatedZone = "Belgrano";

        // 2. Exercise
        final boolean result = postDao.updateWithImage(DETAILED_POST_ID, OTHER_ALBUM_ID, updatedPrice,
                updatedDescription, Condition.NEW, 2020, updatedZone, COVER_IMAGE_ID);

        // 3. Assert
        Assertions.assertTrue(result);
        final PostSummary updated = postDao.findById(DETAILED_POST_ID).orElseThrow(AssertionError::new);
        Assertions.assertEquals(OTHER_ALBUM_ID, updated.getAlbumId());
        Assertions.assertEquals(updatedPrice, updated.getPrice());
        Assertions.assertEquals(updatedDescription, updated.getDescription());
        Assertions.assertEquals(Condition.NEW, updated.getCondition());
        Assertions.assertEquals(2020, updated.getPressingYear());
        Assertions.assertEquals(updatedZone, updated.getZone());
        Assertions.assertEquals(COVER_IMAGE_ID, updated.getCoverImageId());
        Assertions.assertEquals(PostStatus.AVAILABLE, updated.getStatus());
    }

    @Test
    public void testUpdateWithoutImageWhenAlbumHasCoverPreservesPostImageId() {
        // 1. Arrange
        final int updatedPrice = 52000;

        // 2. Exercise
        final boolean result = postDao.update(DETAILED_POST_ID, ALBUM_ID, updatedPrice,
                DETAILED_DESCRIPTION, DETAILED_CONDITION, DETAILED_PRESSING_YEAR, DETAILED_ZONE);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + DETAILED_POST_ID + " AND image_id IS NULL AND price = " + updatedPrice));
    }

    @Test
    public void testUpdateWithNullImageWhenOwnPhotoIsRemovedReturnsNoOwnImage() {
        // 1. Arrange
        final long postId = 5;

        // 2. Exercise
        final boolean updated = postDao.updateWithImage(postId, 3, PRICE,
                null, Condition.USED, null, null, null);

        // 3. Assert
        Assertions.assertTrue(updated);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + postId + " AND image_id IS NULL"));
    }

    @Test
    public void testUpdateWhenPostDoesNotExistReturnsFalse() {
        // 1. Arrange
        final long missingPostId = 999;

        // 2. Exercise
        final boolean result = postDao.update(missingPostId, ALBUM_ID, PRICE,
                null, Condition.USED, null, null);

        // 3. Assert
        Assertions.assertFalse(result);
    }

    @Test
    public void testUpdateWhenConditionIsNullThrowsDataIntegrityViolationWithoutChangingPost() {
        // 1. Arrange

        // 2. Exercise
        final Executable update = () -> postDao.update(DETAILED_POST_ID, ALBUM_ID, DETAILED_PRICE,
                DETAILED_DESCRIPTION, null, DETAILED_PRESSING_YEAR, DETAILED_ZONE);

        // 3. Assert
        Assertions.assertThrows(DataIntegrityViolationException.class, update);
        final PostSummary unchanged = postDao.findById(DETAILED_POST_ID).orElseThrow(AssertionError::new);
        Assertions.assertEquals(DETAILED_CONDITION, unchanged.getCondition());
    }

    @Test
    public void testUpdateStatusWhenPostIsInExpectedStateReturnsTrue() {
        // 1. Arrange
        final long reservedPostId = 6;

        // 2. Exercise
        final boolean result = postDao.updateStatus(reservedPostId, PostStatus.RESERVED, PostStatus.SOLD);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = 6 AND status = 'SOLD'"));
    }

    @Test
    public void testUpdateStatusWhenPostIsInAnotherStateReturnsFalse() {
        // 1. Arrange
        final long soldPostId = SOLD_POST_ID;

        // 2. Exercise
        final boolean result = postDao.updateStatus(soldPostId, PostStatus.AVAILABLE, PostStatus.RESERVED);

        // 3. Assert
        Assertions.assertFalse(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE,
                "id = " + SOLD_POST_ID + " AND status = 'SOLD'"));
    }

    @Test
    public void testSearchWhenPostIsReservedReturnsWithoutIt() {
        // 1. Arrange
        final PostSearchCriteria criteria = criteria(null, PostSort.NEWEST);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertFalse(ids(result).contains(6L));
    }

    @Test
    public void testFindFeaturedWhenAPostIsSoldReturnsOnlyTheAvailableOnes() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(null, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertFalse(ids(result).contains(SOLD_POST_ID));
    }

    @Test
    public void testFindByIdForUpdateWhenPostExistsReturnsPost() {
        // 1. Arrange

        // 2. Exercise
        final Optional<PostSummary> result = postDao.findByIdForUpdate(POST_ID);

        // 3. Assert
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals(PostStatus.AVAILABLE, result.get().getStatus());
    }

    @Test
    public void testFindByIdsForUpdateWhenOneIdDoesNotExistReturnsTheOthersOrderedById() {
        // 1. Arrange
        final List<Long> ids = List.of(6L, 999L, 1L);

        // 2. Exercise
        final List<PostSummary> result = postDao.findByIdsForUpdate(ids);

        // 3. Assert
        Assertions.assertEquals(List.of(1L, 6L), result.stream().map(PostSummary::getId).toList());
        Assertions.assertEquals(PostStatus.RESERVED, result.get(1).getStatus());
    }

    @Test
    public void testSearchWhenQueryMatchesPartOfAlbumTitleReturnsNewestFirst() {
        // 1. Arrange
        final String query = "vers";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID), ids(result));
        Assertions.assertEquals(ALBUM_TITLE, result.get(0).getTitle());
    }

    @Test
    public void testSearchWhenSortIsPriceDescReturnsMatchesOrderedByPrice() {
        // 1. Arrange
        final String query = "versus";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.PRICE_DESC), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(DETAILED_POST_ID, POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenQueryMatchesArtistNameReturnsPosts() {
        // 1. Arrange
        final String query = "kuryaki";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(2, result.size());
        Assertions.assertEquals(ARTIST_NAME, result.get(0).getArtistName());
    }

    @Test
    public void testSearchWhenQueryOmitsSpacesReturnsArtistPosts() {
        // 1. Arrange
        final String query = "sodastereo";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenLimitIsSmallerThanMatchesReturnsOnlyNewest() {
        // 1. Arrange
        final String query = "versus";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), 1, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID), ids(result));
    }

    @Test
    public void testCountSearchWhenFilterMatchesSomePostsReturnsTheirCount() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                "versus", PostSort.NEWEST, null, null, null, null, 40_000, null);

        // 2. Exercise
        final int result = postDao.countSearch(criteria);

        // 3. Assert
        Assertions.assertEquals(1, result);
    }

    @Test
    public void testSearchWhenQueryMatchesNothingReturnsEmpty() {
        // 1. Arrange
        final String query = "pinkfloyd";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testSearchWhenQueryContainsWildcardsReturnsEmptyInsteadOfMatchingEverything() {
        // 1. Arrange
        final String query = "%_";

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria(query, PostSort.NEWEST), LIMIT, 0);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testSearchWhenGenreIsGivenReturnsOnlyMatchingPosts() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                null, PostSort.NEWEST, Genre.ROCK, null, null, null, null, null);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenConditionIsGivenReturnsOnlyMatchingPosts() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                null, PostSort.NEWEST, null, Condition.USED, null, null, null, null);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID, POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenArtistAndYearAreGivenReturnsOnlyMatchingPosts() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                null, PostSort.NEWEST, null, null, 1L, RELEASE_YEAR, null, null);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenPriceRangeIsGivenReturnsOnlyPricedPostsInsideRange() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                null, PostSort.NEWEST, null, null, null, null, 40_000, 50_000);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testSearchWhenAllFiltersAreCombinedReturnsIntersectionInRequestedOrder() {
        // 1. Arrange
        final PostSearchCriteria criteria = new PostSearchCriteria(
                "versus", PostSort.PRICE_DESC, Genre.HIP_HOP, Condition.USED,
                1L, RELEASE_YEAR, 40_000, 45_000);

        // 2. Exercise
        final List<PostSummary> result = postDao.search(criteria, LIMIT, 0);

        // 3. Assert
        Assertions.assertEquals(List.of(DETAILED_POST_ID), ids(result));
    }

    @Test
    public void testFindSearchSuggestionsWhenQueryMatchesPrefixAndContentReturnsRankedResults() {
        // 1. Arrange
        final String query = "s";

        // 2. Exercise
        final List<SearchSuggestion> result = postDao.findSearchSuggestions(query, 10);

        // 3. Assert
        Assertions.assertEquals(3, result.size());
        assertSuggestion(result.get(0), SearchSuggestionType.ARTIST, "soda stereo", null);
        assertSuggestion(result.get(1), SearchSuggestionType.ARTIST,
                "illya kuryaki and the valderramas", null);
        assertSuggestion(result.get(2), SearchSuggestionType.ALBUM, "versus",
                "illya kuryaki and the valderramas");
    }

    @Test
    public void testFindSearchSuggestionsWhenQueryOmitsSpacesReturnsExactMatch() {
        // 1. Arrange
        final String query = "sodastereo";

        // 2. Exercise
        final List<SearchSuggestion> result = postDao.findSearchSuggestions(query, 10);

        // 3. Assert
        Assertions.assertEquals(1, result.size());
        assertSuggestion(result.get(0), SearchSuggestionType.ARTIST, "soda stereo", null);
    }

    @Test
    public void testFindSearchSuggestionsWhenQueryMatchesWordStartReturnsAlbumAndArtist() {
        // 1. Arrange
        final String query = "an";

        // 2. Exercise
        final List<SearchSuggestion> result = postDao.findSearchSuggestions(query, 10);

        // 3. Assert
        Assertions.assertEquals(2, result.size());
        assertSuggestion(result.get(0), SearchSuggestionType.ALBUM, "cancion animal", "soda stereo");
        assertSuggestion(result.get(1), SearchSuggestionType.ARTIST,
                "illya kuryaki and the valderramas", null);
    }

    @Test
    public void testFindSearchSuggestionsWhenOnlySoldPostsMatchReturnsEmptyList() {
        // 1. Arrange
        final String query = "sold";

        // 2. Exercise
        final List<SearchSuggestion> result = postDao.findSearchSuggestions(query, 10);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindByPublisherIdWhenPostsExistReturnsRequestedOwnersSliceWithAllStatusesNewestFirst() {
        // 1. Arrange

        // 2. Exercise
        final List<PostSummary> result = postDao.findByPublisherId(USER_ID, 2, 1);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID, 5L), ids(result));
        Assertions.assertEquals(List.of(PostStatus.AVAILABLE, PostStatus.SOLD),
                result.stream().map(PostSummary::getStatus).collect(Collectors.toList()));
        Assertions.assertTrue(result.stream().allMatch(post -> post.getUserId() == USER_ID));
    }

    @Test
    public void testFindAvailableByPublisherIdWhenFirstPageReturnsNewestAvailablePost() {
        // 1. Arrange
        final int firstPageOffset = 0;

        // 2. Exercise
        final List<PostSummary> result = postDao.findAvailableByPublisherId(USER_ID, AVAILABLE_PAGE_SIZE,
                firstPageOffset);

        // 3. Assert
        Assertions.assertEquals(List.of(OTHER_POST_ID), ids(result));
    }

    @Test
    public void testFindAvailableByPublisherIdWhenSecondPageReturnsOlderAvailablePostSkippingSold() {
        // 1. Arrange
        final int secondPageOffset = AVAILABLE_PAGE_SIZE;

        // 2. Exercise
        final List<PostSummary> result = postDao.findAvailableByPublisherId(USER_ID, AVAILABLE_PAGE_SIZE,
                secondPageOffset);

        // 3. Assert
        Assertions.assertEquals(List.of(POST_ID), ids(result));
        Assertions.assertEquals(PostStatus.AVAILABLE, result.get(0).getStatus());
    }

    @Test
    public void testFindAvailableByPublisherIdWhenPageIsPastTheLastOneReturnsEmptyList() {
        // 1. Arrange
        final int thirdPageOffset = 2 * AVAILABLE_PAGE_SIZE;

        // 2. Exercise
        final List<PostSummary> result = postDao.findAvailableByPublisherId(USER_ID, AVAILABLE_PAGE_SIZE,
                thirdPageOffset);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testCountAvailableByPublisherIdWhenOwnerHasSoldPostReturnsOnlyAvailable() {
        // 1. Arrange
        // El usuario 1 publico 1, 3 y 5; la 5 esta vendida.

        // 2. Exercise
        final int total = postDao.countAvailableByPublisherId(USER_ID);

        // 3. Assert
        Assertions.assertEquals(2, total);
    }

    @Test
    public void testFindByPublisherIdWhenUserHasNoPostsReturnsEmptyList() {
        // 1. Arrange
        final long userWithoutPosts = 999;

        // 2. Exercise
        final List<PostSummary> result = postDao.findByPublisherId(userWithoutPosts, 13, 0);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testCountByPublisherIdWhenUserHasPostsReturnsTotal() {
        // 1. Arrange

        // 2. Exercise
        final int result = postDao.countByPublisherId(USER_ID);

        // 3. Assert
        Assertions.assertEquals(3, result);
    }

    @Test
    public void testCountByPublisherIdWhenUserHasNoPostsReturnsZero() {
        // 1. Arrange
        final long userWithoutPosts = 999;

        // 2. Exercise
        final int result = postDao.countByPublisherId(userWithoutPosts);

        // 3. Assert
        Assertions.assertEquals(0, result);
    }

    @Test
    public void testFindSearchSuggestionsWhenLimitIsBelowMatchCountReturnsBestRanked() {
        // 1. Arrange
        final String query = "s";

        // 2. Exercise
        final List<SearchSuggestion> result = postDao.findSearchSuggestions(query, 2);

        // 3. Assert
        Assertions.assertEquals(2, result.size());
        assertSuggestion(result.get(0), SearchSuggestionType.ARTIST, "soda stereo", null);
        assertSuggestion(result.get(1), SearchSuggestionType.ARTIST,
                "illya kuryaki and the valderramas", null);
    }

    private static void assertSuggestion(final SearchSuggestion suggestion, final SearchSuggestionType type,
                                         final String value, final String artistName) {
        Assertions.assertEquals(type, suggestion.getType());
        Assertions.assertEquals(value, suggestion.getValue());
        Assertions.assertEquals(artistName, suggestion.getArtistName());
    }

    private static PostSearchCriteria criteria(final String query, final PostSort sort) {
        return new PostSearchCriteria(query, sort, null, null, null, null, null, null);
    }

    @Test
    public void testFindOwnImageIdWhenPostHasOwnImageReturnsImageId() {
        // 1. Arrange
        final long postId = 5;

        // 2. Exercise
        final Optional<Long> result = postDao.findOwnImageId(postId);

        // 3. Assert
        Assertions.assertEquals(Optional.of(2L), result);
    }

    @Test
    public void testFindOwnImageIdWhenPostOnlyHasAlbumCoverReturnsEmpty() {
        // 1. Arrange
        // Post 1 no tiene foto propia; su portada sale del album.

        // 2. Exercise
        final Optional<Long> result = postDao.findOwnImageId(POST_ID);

        // 3. Assert
        Assertions.assertTrue(result.isEmpty());
    }

    @Test
    public void testFindAlbumCoverImageIdWhenAlbumHasCoverReturnsFallbackImage() {
        // 1. Arrange
        // El post 1 usa el album 1, cuya portada es la imagen 1.

        // 2. Exercise
        final Optional<Long> result = postDao.findAlbumCoverImageId(POST_ID);

        // 3. Assert
        Assertions.assertEquals(Optional.of(COVER_IMAGE_ID), result);
    }

    @Test
    public void testDeleteWhenPostExistsReturnsTrueAndRemovesRow() {
        // 1. Arrange
        final long postId = 5;

        // 2. Exercise
        final boolean result = postDao.delete(postId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, POSTS_TABLE, "id = " + postId));
    }

    @Test
    public void testDeleteWhenPostIsInACartReturnsTrueAndRemovesItsCartItems() {
        // 1. Arrange
        final long postId = 5;

        // 2. Exercise
        final boolean result = postDao.delete(postId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(0, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "post_id = " + postId));
    }

    @Test
    public void testDeleteWhenPostDoesNotExistReturnsFalse() {
        // 1. Arrange
        final long missingPostId = 999;

        // 2. Exercise
        final boolean result = postDao.delete(missingPostId);

        // 3. Assert
        Assertions.assertFalse(result);
    }

    private static List<Long> ids(final List<PostSummary> posts) {
        return posts.stream().map(PostSummary::getId).collect(Collectors.toList());
    }
}
```
