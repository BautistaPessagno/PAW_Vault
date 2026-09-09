---
title: "PostServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java"]
---

# PostServiceImpl

getFeatured reads eight newest post IDs; findById is read-only transactional. publish resolves User, Artist and Album with optional cover data, rejects an existing user/album pair, and creates a Post in one transaction. DuplicatePostKeyException becomes DuplicatePostException; any caught DataIntegrityViolationException becomes ConcurrentPublishException. notifyInterest has no service transaction: it reloads the summary, trims contact name/email, lowercases email and passes [[PostInterestNotification]] plus Locale to asynchronous [[EmailService]].

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[ConcurrentPublishException]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[EmailService]], [[Post]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostService]], [[PostSummary]], [[User]], [[UserService]].

Referenced by: [[PostServiceImplTest]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, lines 1–90](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Album;
import ar.edu.itba.paw.models.Artist;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.persistence.DuplicatePostKeyException;
import org.springframework.dao.DataIntegrityViolationException;
import ar.edu.itba.paw.persistence.PostDao;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Locale;
import java.util.Optional;

@Service
public class PostServiceImpl implements PostService {

    private static final int FEATURED_LIMIT = 8;

    private final PostDao postDao;
    private final UserService userService;
    private final ArtistService artistService;
    private final AlbumService albumService;
    private final EmailService emailService;

    @Autowired
    public PostServiceImpl(final PostDao postDao, final UserService userService,
                           final ArtistService artistService, final AlbumService albumService,
                           final EmailService emailService) {
        this.postDao = postDao;
        this.userService = userService;
        this.artistService = artistService;
        this.albumService = albumService;
        this.emailService = emailService;
    }

    @Override
    @Transactional(readOnly = true)
    public List<PostSummary> getFeatured() {
        return postDao.findFeatured(FEATURED_LIMIT);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<PostSummary> findById(final long postId) {
        return postDao.findById(postId);
    }

    @Override
    @Transactional
    public Post publish(final String username, final String publisherEmail, final String title,
                        final String artistName, final int releaseYear, final String coverContentType,
                        final byte[] coverData, final Locale locale) {
        try {
            final User publisher = userService.findOrCreate(username, publisherEmail, locale);
            final Artist artist = artistService.findOrCreate(artistName);
            final Album album = albumService.findOrCreate(title, artist.getId(), releaseYear,
                    coverContentType, coverData);
            if (postDao.existsByUserIdAndAlbumId(publisher.getId(), album.getId())) {
                throw new DuplicatePostException();
            }
            return postDao.create(publisher.getId(), album.getId());
        } catch (final DuplicatePostKeyException e) {
            throw new DuplicatePostException();
        } catch (final DataIntegrityViolationException e) {
            // Otra publicacion simultanea creo el mismo artista, album o usuario.
            // PostgreSQL ya aborto esta transaccion, asi que no se puede releer desde
            // aca: solo traducimos. Su transaccion ya commiteo, asi que reintentar anda.
            throw new ConcurrentPublishException();
        }
    }

    // Sin @Transactional a proposito: solo lee el post y delega el envio, que ademas es @Async.
    // No hay razon para abrir una transaccion para una sola lectura.
    @Override
    public void notifyInterest(final long postId, final String contactName, final String contactEmail,
                               final Locale locale) {
        final PostSummary post = postDao.findById(postId).orElseThrow(PostNotFoundException::new);
        final PostInterestNotification notification = new PostInterestNotification(
                post.getId(), post.getPublisherEmail(), contactName.trim(),
                contactEmail.trim().toLowerCase(Locale.ROOT), post.getTitle(), post.getArtistName(),
                post.getReleaseYear());

        emailService.sendPostInterestEmail(notification, locale);
    }
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
