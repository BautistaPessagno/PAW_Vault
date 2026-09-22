---
title: "PostService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java"]
---

# PostService

Public detail lookup, owner-checked edit lookup, paged search, search suggestions, a publisher's paged listing, publish, update and delete. Publisher arguments are account IDs taken from [[AuthenticatedUser]]. Contact and inbox behavior belong to [[InquiryService]]. The comment above delete still mentions a returned count, but the method returns void.

## Connections

Project types referenced: [[Condition]], [[Genre]], [[Post]], [[PostPage]], [[PostSearchCriteria]], [[PostSummary]], [[SearchResult]], [[SearchSuggestion]].

Referenced by: [[LandingController]], [[PostController]], [[PostServiceImpl]], [[ProfileController]], [[PublishController]], [[SearchSuggestionController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java, lines 1–37](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;

import java.util.List;

public interface PostService {

    PostSummary findById(long postId);

    PostSummary findEditableById(long postId, long publisherId);

    SearchResult search(PostSearchCriteria criteria, int pageNumber);

    List<SearchSuggestion> findSearchSuggestions(String query);

    PostPage findByPublisherId(long publisherId, int pageNumber);

    Post publish(long publisherId, String title, String artistName, int releaseYear,
                 Genre genre, int price, String description, Condition condition, Integer pressingYear,
                 String zone, String coverContentType, byte[] coverData);

    PostSummary update(long postId, long publisherId, String title, String artistName, int releaseYear,
                       Genre genre, int price, String description, Condition condition, Integer pressingYear,
                       String zone, String coverContentType, byte[] coverData);

    // Devuelve cuantas consultas quedaron desenganchadas de la publicacion eliminada.
    void delete(long postId, long publisherId);

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
