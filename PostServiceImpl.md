---
title: "PostServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java"]
---

# PostServiceImpl

Search trims the query, rejects more than 255 characters, normalizes filters and fetches 16 rows for a 15-item page to detect a next page. Suggestions compact the query and return five. The profile listing pages 12 posts with a counted total. Publish resolves artist and album, rejects duplicates, stores an optional image and inserts the post. Update and delete lock the post and require the owner and AVAILABLE status. Update resolves catalog identity for editing and may store a new image; delete detaches inquiries, deletes the post and its own image, and logs the result.

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[ForbiddenOperationException]], [[Genre]], [[ImageService]], [[InquiryDao]], [[InvalidSearchQueryException]], [[PageNotFoundException]], [[Pagination]], [[Post]], [[PostDao]], [[PostNotFoundException]], [[PostPage]], [[PostSearchCriteria]], [[PostService]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[SearchResult]], [[SearchSuggestion]], [[SearchText]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenced by: [[PostServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, lines 1–246](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchText;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.InquiryDao;
import org.springframework.dao.DataIntegrityViolationException;
import ar.edu.itba.paw.persistence.PostDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;


@Service
public class PostServiceImpl implements PostService {

    private static final Logger LOGGER = LoggerFactory.getLogger(PostServiceImpl.class);

    private static final int SUGGESTION_LIMIT = 5;
    private static final int PROFILE_PAGE_SIZE = 12;
    private static final int CATALOG_PAGE_SIZE = 15;
    // Ningun titulo ni artista supera los 255 caracteres de su columna: una query mas larga no
    // puede matchear nada y no tiene sentido dejarla llegar al LIKE.
    private static final int MAX_QUERY_LENGTH = 255;
    // Limites del catalogo: un filtro fuera de estos valores no puede tener resultados.
    private static final int MIN_YEAR = 1000;
    private static final int MAX_YEAR = 9999;
    private static final int MIN_PRICE = 1;
    private static final int MAX_PRICE = 99_999_999;

    private final PostDao postDao;
    private final InquiryDao inquiryDao;
    private final UserService userService;
    private final ArtistService artistService;
    private final AlbumService albumService;
    private final ImageService imageService;

    @Autowired
    public PostServiceImpl(final PostDao postDao, final InquiryDao inquiryDao, final UserService userService,
                           final ArtistService artistService, final AlbumService albumService,
                           final ImageService imageService) {
        this.postDao = postDao;
        this.inquiryDao = inquiryDao;
        this.userService = userService;
        this.artistService = artistService;
        this.albumService = albumService;
        this.imageService = imageService;
    }

    @Override
    @Transactional(readOnly = true)
    public PostSummary findById(final long postId) {
        return postDao.findById(postId).orElseThrow(PostNotFoundException::new);
    }

    @Override
    @Transactional(readOnly = true)
    public PostSummary findEditableById(final long postId, final long publisherId) {
        return requireAvailable(requireOwner(
                postDao.findById(postId).orElseThrow(PostNotFoundException::new), publisherId));
    }

    // Una busqueda vacia no filtra nada: se muestra lo mismo que la landing sin buscar,
    // pero respetando el orden pedido.
    @Override
    @Transactional(readOnly = true)
    public SearchResult search(final PostSearchCriteria criteria, final int pageNumber) {
        final String query = blankToNull(criteria.getQuery());
        if (query != null && query.length() > MAX_QUERY_LENGTH) {
            throw new InvalidSearchQueryException();
        }
        final int offset = Pagination.offsetFor(pageNumber, CATALOG_PAGE_SIZE);
        final List<PostSummary> rows = postDao.search(
                normalize(criteria, query), CATALOG_PAGE_SIZE + 1, offset);
        return new SearchResult(query, toPage(rows, pageNumber, CATALOG_PAGE_SIZE));
    }

    @Override
    @Transactional(readOnly = true)
    public List<SearchSuggestion> findSearchSuggestions(final String query) {
        if (query != null && query.length() > MAX_QUERY_LENGTH) {
            return List.of();
        }
        final String normalizedQuery = SearchText.compact(query);
        if (normalizedQuery.isEmpty()) {
            return List.of();
        }
        return postDao.findSearchSuggestions(normalizedQuery, SUGGESTION_LIMIT);
    }

    @Override
    @Transactional(readOnly = true)
    public PostPage findByPublisherId(final long publisherId, final int pageNumber) {
        final int totalPages = Pagination.pagesFor(postDao.countByPublisherId(publisherId), PROFILE_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, PROFILE_PAGE_SIZE, totalPages);
        final List<PostSummary> posts = postDao.findByPublisherId(publisherId, PROFILE_PAGE_SIZE, offset);
        return new PostPage(posts, pageNumber, totalPages);
    }

    private static PostPage toPage(final List<PostSummary> rows, final int pageNumber, final int pageSize) {
        if (pageNumber > 1 && rows.isEmpty()) {
            throw new PageNotFoundException();
        }
        final boolean hasNext = rows.size() > pageSize;
        final List<PostSummary> posts = hasNext ? rows.subList(0, pageSize) : rows;
        return new PostPage(posts, pageNumber, pageNumber > 1, hasNext);
    }

    // Los filtros llegan de la URL, asi que pueden venir con cualquier valor. Uno fuera de
    // rango no corta la busqueda: se ignora y los demas se siguen aplicando. Sin orden
    // pedido, lo mas nuevo primero.
    private static PostSearchCriteria normalize(final PostSearchCriteria criteria, final String query) {
        final Long artistId = criteria.getArtistId() != null && criteria.getArtistId() > 0
                ? criteria.getArtistId() : null;
        final Integer minPrice = insideRange(criteria.getMinPrice(), MIN_PRICE, MAX_PRICE);
        final Integer maxPrice = insideRange(criteria.getMaxPrice(), MIN_PRICE, MAX_PRICE);
        // Un rango dado vuelta no deja pasar nada: se ignoran los dos extremos.
        final boolean invertedRange = minPrice != null && maxPrice != null && minPrice > maxPrice;
        return new PostSearchCriteria(query,
                criteria.getSort() == null ? PostSort.NEWEST : criteria.getSort(),
                criteria.getGenre(), criteria.getCondition(), artistId,
                insideRange(criteria.getReleaseYear(), MIN_YEAR, MAX_YEAR),
                invertedRange ? null : minPrice,
                invertedRange ? null : maxPrice);
    }

    private static Integer insideRange(final Integer value, final int min, final int max) {
        return value != null && value >= min && value <= max ? value : null;
    }

    @Override
    @Transactional
    public Post publish(final long publisherId, final String title, final String artistName,
                        final int releaseYear, final Genre genre, final int price,
                        final String description, final Condition condition, final Integer pressingYear,
                        final String zone, final String coverContentType, final byte[] coverData) {
        try {
            final User publisher = userService.findById(publisherId).orElseThrow(UserNotFoundException::new);
            final Artist artist = artistService.findOrCreate(artistName);
            final Album album = albumService.findOrCreate(title, artist.getId(), releaseYear, genre);
            if (postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())) {
                throw new DuplicatePostException();
            }
            final Long imageId = coverData == null || coverData.length == 0
                    ? null : imageService.create(coverContentType, coverData).getId();
            return postDao.create(publisher.getId(), album.getId(), price, blankToNull(description), condition,
                    pressingYear, blankToNull(zone), imageId);
        } catch (final DuplicatePostKeyException e) {
            throw new DuplicatePostException();
        } catch (final DataIntegrityViolationException e) {
            // Otra publicacion simultanea creo el mismo artista o album.
            // PostgreSQL ya aborto esta transaccion, asi que no se puede releer desde
            // aca: solo traducimos. Su transaccion ya commiteo, asi que reintentar anda.
            throw new ConcurrentPublishException();
        }
    }

    @Override
    @Transactional
    public PostSummary update(final long postId, final long publisherId, final String title,
                              final String artistName, final int releaseYear, final Genre genre, final int price,
                              final String description, final Condition condition, final Integer pressingYear,
                              final String zone, final String coverContentType, final byte[] coverData) {
        requireAvailable(requireOwner(
                postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new), publisherId));
        try {
            final Artist artist = artistService.resolveForEdit(artistName);
            final Album album = albumService.resolveForEdit(title, artist.getId(), releaseYear, genre);
            final boolean updated = coverData == null || coverData.length == 0
                    ? postDao.update(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone))
                    : postDao.updateWithImage(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone),
                            imageService.create(coverContentType, coverData).getId());
            if (!updated) {
                throw new PostNotFoundException();
            }
            return postDao.findById(postId).orElseThrow(PostNotFoundException::new);
        } catch (final DuplicatePostKeyException e) {
            throw new DuplicatePostException();
        } catch (final DataIntegrityViolationException e) {
            throw new ConcurrentPublishException();
        }
    }

    // Solo se elimina lo que todavia esta a la venta: un ejemplar vendido es el registro de
    // la compra. Las consultas sobreviven desenganchadas del post para que el comprador
    // siga viendo que pregunto y que la publicacion ya no existe. La foto propia de la
    // publicacion se va con ella; la portada del album es del album y queda.
    @Override
    @Transactional
    public void delete(final long postId, final long publisherId) {
        requireAvailable(requireOwner(
                postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new), publisherId));
        final Long ownImageId = postDao.findOwnImageId(postId).orElse(null);
        final int detached = inquiryDao.detachFromPost(postId);
        if (!postDao.delete(postId)) {
            throw new PostNotFoundException();
        }
        if (ownImageId != null) {
            imageService.delete(ownImageId);
        }
        LOGGER.info("Deleted post postId={} publisherId={} detachedInquiries={} ownImageId={}",
                postId, publisherId, detached, ownImageId);
    }

    private static PostSummary requireOwner(final PostSummary post, final long publisherId) {
        if (post.getUserId() != publisherId) {
            throw new ForbiddenOperationException();
        }
        return post;
    }

    private static PostSummary requireAvailable(final PostSummary post) {
        if (post.getStatus() != PostStatus.AVAILABLE) {
            throw new PostUnavailableException();
        }
        return post;
    }

    // Los campos de texto opcionales llegan como "" cuando el form los deja vacios; en la base van como NULL.
    private static String blankToNull(final String value) {
        if (value == null) {
            return null;
        }
        final String trimmed = value.trim();
        return trimmed.isEmpty() ? null : trimmed;
    }

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
