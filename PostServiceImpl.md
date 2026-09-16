---
title: "PostServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java"]
---

# PostServiceImpl

Search trims blank query to null, rejects more than 255 characters, defaults sort to NEWEST and limits results to 16. Invalid numeric filters are ignored; an inverted valid price range drops both bounds. Publishing loads the existing account, resolves Artist/Album, rejects duplicate user/album pairs, creates an optional exemplar image and inserts the Post in one transaction. Optional description/zone become trimmed text or null. DuplicatePostKeyException maps to DuplicatePostException; other DataIntegrityViolationException values map broadly to ConcurrentPublishException.

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[ConcurrentPublishException]], [[Condition]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[Genre]], [[ImageService]], [[InvalidSearchQueryException]], [[Post]], [[PostDao]], [[PostSearchCriteria]], [[PostService]], [[PostSort]], [[SearchResult]], [[User]], [[UserNotFoundException]], [[UserService]].

Referenced by: [[PostServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, lines 1–121](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import org.springframework.dao.DataIntegrityViolationException;
import ar.edu.itba.paw.persistence.PostDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
public class PostServiceImpl implements PostService {

    // Mientras no haya paginacion, con o sin busqueda se muestra el mismo punado de publicaciones.
    private static final int RESULT_LIMIT = 16;
    // Ningun titulo ni artista supera los 255 caracteres de su columna: una query mas larga no
    // puede matchear nada y no tiene sentido dejarla llegar al LIKE.
    private static final int MAX_QUERY_LENGTH = 255;
    // Limites del catalogo: un filtro fuera de estos valores no puede tener resultados.
    private static final int MIN_YEAR = 1000;
    private static final int MAX_YEAR = 9999;
    private static final int MIN_PRICE = 1;
    private static final int MAX_PRICE = 99_999_999;

    private final PostDao postDao;
    private final UserService userService;
    private final ArtistService artistService;
    private final AlbumService albumService;
    private final ImageService imageService;

    @Autowired
    public PostServiceImpl(final PostDao postDao, final UserService userService,
                           final ArtistService artistService, final AlbumService albumService,
                           final ImageService imageService) {
        this.postDao = postDao;
        this.userService = userService;
        this.artistService = artistService;
        this.albumService = albumService;
        this.imageService = imageService;
    }

    // Una busqueda vacia no filtra nada: se muestra lo mismo que la landing sin buscar,
    // pero respetando el orden pedido.
    @Override
    @Transactional(readOnly = true)
    public SearchResult search(final PostSearchCriteria criteria) {
        final String query = blankToNull(criteria.getQuery());
        if (query != null && query.length() > MAX_QUERY_LENGTH) {
            throw new InvalidSearchQueryException();
        }
        return new SearchResult(query, postDao.search(normalize(criteria, query), RESULT_LIMIT));
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
