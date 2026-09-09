---
title: "PostServiceImpl"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java"]
---

# PostServiceImpl

`getFeatured` reads the eight newest post IDs, and `findById` returns a read-only transactional Optional. `publish` resolves User → Artist → Album, rejects an existing user/album pair, and creates the Post inside one transaction. A [[DuplicatePostKeyException]] becomes [[DuplicatePostException]]. Any Spring DataIntegrityViolationException caught by publish becomes [[ConcurrentPublishException]], so the label is broader than proven concurrency. `notifyInterest` deliberately has no transaction: it reads one summary, throws [[PostNotFoundException]] if absent, trims the contact name, normalizes the contact email, constructs [[PostInterestNotification]], then sends synchronous mail. See [[Publish flow]] and [[Contact flow]].

## Connections

Project types referenced: [[Album]], [[AlbumService]], [[Artist]], [[ArtistService]], [[ConcurrentPublishException]], [[DuplicatePostException]], [[DuplicatePostKeyException]], [[EmailService]], [[Post]], [[PostDao]], [[PostInterestNotification]], [[PostNotFoundException]], [[PostService]], [[PostSummary]], [[User]], [[UserService]].

Referenced by: no other production Java type directly references this name; Spring discovers implementations through scanning.

Tests: [[PostServiceImplTest]]. See [[Testing and evidence]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, lines 1–87](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>)

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
                        final String artistName, final int releaseYear, final Locale locale) {
        try {
            final User publisher = userService.findOrCreate(username, publisherEmail, locale);
            final Artist artist = artistService.findOrCreate(artistName);
            final Album album = albumService.findOrCreate(title, artist.getId(), releaseYear);
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

    // Sin @Transactional a proposito: la entrega SMTP puede tardar hasta 15 segundos entre timeouts
    // de conexion y de lectura, y no hay razon para retener una conexion a la base mientras tanto.
    @Override
    public void notifyInterest(final long postId, final String contactName, final String contactEmail) {
        final PostSummary post = postDao.findById(postId).orElseThrow(PostNotFoundException::new);
        final PostInterestNotification notification = new PostInterestNotification(
                post.getId(), post.getPublisherEmail(), contactName.trim(),
                contactEmail.trim().toLowerCase(Locale.ROOT), post.getTitle(), post.getArtistName(),
                post.getReleaseYear());

        emailService.sendPostInterestEmail(notification);
    }
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
