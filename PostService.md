---
title: "PostService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java"]
---

# PostService

Search by PostSearchCriteria and publish for an authenticated publisher ID with catalog, commercial and optional image data. Contact and inbox behavior now belong to [[InquiryService]].

## Connections

Project types referenced: [[Condition]], [[Genre]], [[Post]], [[PostSearchCriteria]], [[SearchResult]].

Referenced by: [[LandingController]], [[PostServiceImpl]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java, lines 1–17](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.SearchResult;

public interface PostService {

    SearchResult search(PostSearchCriteria criteria);

    Post publish(long publisherId, String title, String artistName, int releaseYear,
                 Genre genre, int price, String description, Condition condition, Integer pressingYear,
                 String zone, String coverContentType, byte[] coverData);

}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
