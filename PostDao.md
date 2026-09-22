---
title: "PostDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java"]
---

# PostDao

Paged catalog search, search suggestions, a publisher's paged listing and count, summary and locking lookups, duplicate-pair check, create, update with or without a new image, guarded sale transition, own-image lookup and delete. Criteria, limits and offsets cross this interface without JDBC types. Locking calls require the service transaction to hold the row lock.

## Connections

Project types referenced: [[Condition]], [[Post]], [[PostSearchCriteria]], [[PostSummary]], [[SearchSuggestion]].

Referenced by: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java, lines 1–45](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchSuggestion;

import java.util.List;
import java.util.Optional;

public interface PostDao {
    List<PostSummary> search(PostSearchCriteria criteria, int limit, int offset);

    // normalizedQuery llega ya pasada por SearchText.compact: el ranking se
    // resuelve contra la columna search_phrase, sin traer la tabla entera.
    List<SearchSuggestion> findSearchSuggestions(String normalizedQuery, int limit);

    List<PostSummary> findByPublisherId(long publisherId, int limit, int offset);

    // Total de publicaciones de un publicante, para numerar las paginas del perfil.
    int countByPublisherId(long publisherId);

    Optional<PostSummary> findById(long id);

    Optional<PostSummary> findByIdForUpdate(long id);

    boolean existsByUserIdAndAlbumId(long userId, long albumId);

    Post create(long userId, long albumId, int price, String description, Condition condition,
                Integer pressingYear, String zone, Long imageId);

    boolean update(long id, long albumId, int price, String description, Condition condition,
                   Integer pressingYear, String zone);

    boolean updateWithImage(long id, long albumId, int price, String description, Condition condition,
                            Integer pressingYear, String zone, long imageId);

    boolean markSoldIfAvailable(long id);

    // Imagen propia de la publicacion, sin caer en la portada del album.
    Optional<Long> findOwnImageId(long id);

    boolean delete(long id);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
