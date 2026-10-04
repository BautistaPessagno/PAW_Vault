---
title: "PostServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java"]
---

# PostServiceImpl

Publicaciones. Busca con normalización y filtros saneados, contando antes de listar. Publica y edita artista, álbum, fotos y post en una transacción, traduciendo las carreras a errores de negocio. Elimina desenganchando las consultas. Expone bloqueo y transiciones para la venta con propagación `MANDATORY`. Ver [[Landing flow]], [[Publish flow]] y [[Edit and delete flow]].

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`, `SUGGESTION_LIMIT`, `PROFILE_PAGE_SIZE`, `CATALOG_PAGE_SIZE`, `MAX_QUERY_LENGTH`, `postDao`, `inquiryDao`, `userService`, `artistService`, `albumService`, `imageService`.

Operaciones para localizar en la fuente: `findById`, `lockById`, `lockByIds`, `reserve`, `release`, `markSold`, `findDetail`, `findPublisherId`, `findEditableById`, `findUploadedImageIds`, `leadImageThenGallery`, `findAlbumCoverImageId`, `search`, `findSearchSuggestions`, `findByPublisherId`, `findAvailableByPublisherId`, `normalize`, `validYearOrNull`, `validPriceOrNull`, `publish`, `update`, `delete`, `createImages`, `extrasOf`, `requireGallerySize`, `requireAvailable`, `requireValidPostData`, `blankToNull`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[Genre]], [[ImageRules]], [[ImageService]], [[ImageUpload]], [[InquiryDao]], [[InvalidImageException]], [[InvalidPostDataException]], [[InvalidSearchQueryException]], [[Pagination]], [[Post]], [[PostDao]], [[PostDetail]], [[PostNotFoundException]], [[PostPage]], [[PostSearchCriteria]], [[PostService]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[PostUnavailableException]], [[PublicUserProfile]], [[SearchResult]], [[SearchSuggestion]], [[SearchText]], [[User]], [[UserNotFoundException]], [[UserService]], [[VinylInputRules]].

Referenciado por: [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 1–391.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.models.ImageRules;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchText;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.VinylInputRules;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import ar.edu.itba.paw.persistence.InquiryDao;
import ar.edu.itba.paw.persistence.PostDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

@Service
public class PostServiceImpl implements PostService {

    private static final Logger LOGGER = LoggerFactory.getLogger(PostServiceImpl.class);

    private static final int SUGGESTION_LIMIT = 5;
    private static final int PROFILE_PAGE_SIZE = 15;
    private static final int CATALOG_PAGE_SIZE = 15;
    // Ningun titulo ni artista supera los 255 caracteres de su columna: una query mas larga no
    // puede matchear nada y no tiene sentido dejarla llegar al LIKE.
    private static final int MAX_QUERY_LENGTH = 255;
    private final PostDao postDao;
    private final InquiryDao inquiryDao;
    private final UserService userService;
    private final ArtistService artistService;
    private final AlbumService albumService;
    private final ImageService imageService;

    // InquiryDao y no InquiryService: InquiryService ya depende de PostService. Solo se usa para
    // desenganchar las consultas del post que se elimina.
    @Autowired
    public PostServiceImpl(final PostDao postDao, final InquiryDao inquiryDao,
                           final UserService userService,
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

    // Bloquea la fila del post dentro de la transaccion del llamador: las consultas del mismo
    // ejemplar compiten por ella y se ordenan entre si. MANDATORY porque sin una transaccion
    // de afuera el lock se soltaria apenas vuelve el metodo; lo mismo para las transiciones.
    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public PostSummary lockById(final long postId) {
        return postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public List<PostSummary> lockByIds(final Collection<Long> postIds) {
        return postDao.findByIdsForUpdate(postIds);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean reserve(final long postId) {
        return postDao.updateStatus(postId, PostStatus.AVAILABLE, PostStatus.RESERVED);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean release(final long postId) {
        return postDao.updateStatus(postId, PostStatus.RESERVED, PostStatus.AVAILABLE);
    }

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    public boolean markSold(final long postId) {
        return postDao.updateStatus(postId, PostStatus.RESERVED, PostStatus.SOLD);
    }

    @Override
    @Transactional(readOnly = true)
    public PostDetail findDetail(final long postId, final Long viewerId, final boolean moderator) {
        final PostSummary post = findById(postId);
        final PublicUserProfile seller = userService.findPublicProfileById(post.getUserId()).orElse(null);
        final boolean ownedByViewer = viewerId != null && viewerId == post.getUserId();
        return new PostDetail(post, seller, leadImageThenGallery(post.getCoverImageId(), postId), ownedByViewer,
                moderator);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Long> findPublisherId(final long postId) {
        return postDao.findById(postId).map(PostSummary::getUserId);
    }

    @Override
    @Transactional(readOnly = true)
    public PostSummary findEditableById(final long postId) {
        return requireAvailable(postDao.findById(postId).orElseThrow(PostNotFoundException::new));
    }

    @Override
    @Transactional(readOnly = true)
    public List<Long> findUploadedImageIds(final long postId) {
        return leadImageThenGallery(postDao.findOwnImageId(postId).orElse(null), postId);
    }

    private List<Long> leadImageThenGallery(final Long leadImageId, final long postId) {
        final List<Long> imageIds = new ArrayList<>();
        if (leadImageId != null) {
            imageIds.add(leadImageId);
        }
        imageIds.addAll(imageService.findGalleryImageIds(postId));
        return List.copyOf(imageIds);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Long> findAlbumCoverImageId(final long postId) {
        return postDao.findAlbumCoverImageId(postId);
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
        // Misma normalizacion que las sugerencias: lo que el autocompletado ofrece, la
        // busqueda lo encuentra. Una query sin letras ni digitos no coincide con nada.
        final String searchQuery = query == null ? null : SearchText.compact(query);
        final PostSearchCriteria normalized = normalize(criteria, searchQuery);
        final int total = searchQuery != null && searchQuery.isEmpty() ? 0 : postDao.countSearch(normalized);
        final int totalPages = Pagination.pagesFor(total, CATALOG_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, CATALOG_PAGE_SIZE, totalPages);
        final List<PostSummary> posts = total == 0
                ? List.of()
                : postDao.search(normalized, CATALOG_PAGE_SIZE, offset);
        return new SearchResult(query, normalized, new PostPage(posts, pageNumber, totalPages), total);
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

    @Override
    @Transactional(readOnly = true)
    public PostPage findAvailableByPublisherId(final long publisherId, final int pageNumber) {
        final int totalPages = Pagination.pagesFor(postDao.countAvailableByPublisherId(publisherId), PROFILE_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, PROFILE_PAGE_SIZE, totalPages);
        final List<PostSummary> posts = postDao.findAvailableByPublisherId(publisherId, PROFILE_PAGE_SIZE, offset);
        return new PostPage(posts, pageNumber, totalPages);
    }

    // Los filtros llegan de la URL, asi que pueden venir con cualquier valor. Uno fuera de
    // rango no corta la busqueda: se ignora y los demas se siguen aplicando. Sin orden
    // pedido, lo mas nuevo primero.
    private static PostSearchCriteria normalize(final PostSearchCriteria criteria, final String query) {
        final Long artistId = criteria.getArtistId() != null && criteria.getArtistId() > 0
                ? criteria.getArtistId() : null;
        final Integer releaseYear = validYearOrNull(criteria.getReleaseYear());
        final Integer minPrice = validPriceOrNull(criteria.getMinPrice());
        final Integer maxPrice = validPriceOrNull(criteria.getMaxPrice());
        // Un rango dado vuelta no deja pasar nada: se ignoran los dos extremos.
        final boolean invertedRange = !VinylInputRules.isPriceRangeOrdered(minPrice, maxPrice);
        return new PostSearchCriteria(query,
                criteria.getSort() == null ? PostSort.NEWEST : criteria.getSort(),
                criteria.getGenre(), criteria.getCondition(), artistId,
                releaseYear,
                invertedRange ? null : minPrice,
                invertedRange ? null : maxPrice);
    }

    private static Integer validYearOrNull(final Integer value) {
        return value != null && VinylInputRules.classifyYear(value) == VinylInputRules.YearValidity.VALID
                ? value : null;
    }

    private static Integer validPriceOrNull(final Integer value) {
        return value != null && VinylInputRules.classifyPrice(value) == VinylInputRules.PriceValidity.VALID
                ? value : null;
    }

    @Override
    @Transactional
    public Post publish(final long publisherId, final String title, final String artistName,
                        final int releaseYear, final Genre genre, final int price,
                        final String description, final Condition condition, final Integer pressingYear,
                        final String zone, final List<ImageUpload> images) {
        requireValidPostData(releaseYear, price, pressingYear);
        requireGallerySize(images == null ? 0 : images.size());
        try {
            final User publisher = userService.findById(publisherId).orElseThrow(UserNotFoundException::new);
            final Artist artist = artistService.findOrCreate(artistName);
            final Album album = albumService.findOrCreate(title, artist.getId(), releaseYear, genre);
            if (postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())) {
                throw new DuplicatePostException();
            }
            final List<Long> imageIds = createImages(images);
            final Long imageId = imageIds.isEmpty() ? null : imageIds.get(0);
            final Post post = postDao.create(publisher.getId(), album.getId(), price, blankToNull(description), condition,
                    pressingYear, blankToNull(zone), imageId);
            if (imageIds.size() > 1) {
                imageService.replaceGallery(post.getId(), extrasOf(imageIds));
            }
            return post;
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
    public PostSummary update(final long postId, final String title,
                              final String artistName, final int releaseYear, final Genre genre, final int price,
                              final String description, final Condition condition, final Integer pressingYear,
                              final String zone, final List<ImageUpload> images,
                              final List<Long> removedImageIds) {
        requireValidPostData(releaseYear, price, pressingYear);
        requireAvailable(postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new));
        final List<Long> oldImageIds = findUploadedImageIds(postId);
        final Set<Long> removed = removedImageIds == null ? Set.of() : new HashSet<>(removedImageIds);
        if (!oldImageIds.containsAll(removed)) {
            throw new InvalidImageException();
        }
        final List<Long> imageIds = new ArrayList<>();
        for (final Long imageId : oldImageIds) {
            if (!removed.contains(imageId)) {
                imageIds.add(imageId);
            }
        }
        requireGallerySize(imageIds.size() + (images == null ? 0 : images.size()));
        try {
            final Artist artist = artistService.resolveForEdit(artistName);
            final Album album = albumService.resolveForEdit(title, artist.getId(), releaseYear, genre);
            imageIds.addAll(createImages(images));
            final boolean galleryChanged = !removed.isEmpty() || images != null && !images.isEmpty();
            final boolean updated = galleryChanged
                    ? postDao.updateWithImage(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone), imageIds.isEmpty() ? null : imageIds.get(0))
                    : postDao.update(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone));
            if (!updated) {
                throw new PostNotFoundException();
            }
            if (galleryChanged) {
                imageService.replaceGallery(postId, extrasOf(imageIds));
                for (final Long removedId : removed) {
                    imageService.delete(removedId);
                }
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
    public int delete(final long postId) {
        requireAvailable(postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new));
        final List<Long> uploadedImageIds = findUploadedImageIds(postId);
        final int detached = inquiryDao.detachFromPost(postId);
        if (!postDao.delete(postId)) {
            throw new PostNotFoundException();
        }
        // Las filas de la galeria se van con el post (ON DELETE CASCADE): recien ahi se pueden borrar las fotos.
        for (final Long imageId : uploadedImageIds) {
            imageService.delete(imageId);
        }
        LOGGER.info("Deleted post postId={} detachedInquiries={} deletedImages={}",
                postId, detached, uploadedImageIds.size());
        return detached;
    }

    private List<Long> createImages(final List<ImageUpload> images) {
        final List<Long> imageIds = new ArrayList<>();
        if (images != null) {
            for (final ImageUpload image : images) {
                imageIds.add(imageService.create(image.getContentType(), image.getData()).getId());
            }
        }
        return imageIds;
    }

    // La primera foto es la principal y va en el post; el resto es la galeria.
    private static List<Long> extrasOf(final List<Long> imageIds) {
        return imageIds.isEmpty() ? List.of() : imageIds.subList(1, imageIds.size());
    }

    private static void requireGallerySize(final int size) {
        if (size > ImageRules.MAX_GALLERY_IMAGES) {
            throw new InvalidImageException();
        }
    }

    private static PostSummary requireAvailable(final PostSummary post) {
        if (post.getStatus() != PostStatus.AVAILABLE) {
            throw new PostUnavailableException();
        }
        return post;
    }

    private static void requireValidPostData(final int releaseYear, final int price,
                                             final Integer pressingYear) {
        final boolean invalidReleaseYear = VinylInputRules.classifyYear(releaseYear)
                != VinylInputRules.YearValidity.VALID;
        final boolean invalidPrice = VinylInputRules.classifyPrice(price)
                != VinylInputRules.PriceValidity.VALID;
        final boolean invalidPressingYear = pressingYear != null
                && VinylInputRules.classifyYear(pressingYear) != VinylInputRules.YearValidity.VALID;
        if (invalidReleaseYear || invalidPrice || invalidPressingYear
                || !VinylInputRules.isPressingYearOrdered(releaseYear, pressingYear)) {
            throw new InvalidPostDataException();
        }
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
