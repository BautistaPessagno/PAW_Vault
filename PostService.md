---
title: "PostService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java"]
---

# PostService

Business contract for eight-featured-post policy through the implementation, Optional summary lookup, publishing and contact notification. publish accepts cover MIME type and bytes along with the five textual/numeric values and Locale. notifyInterest also receives Locale. See [[Publish flow]] and [[Contact flow]].

## Connections

Project types referenced: [[Post]], [[PostSummary]].

Referenced by: [[LandingController]], [[PostContactController]], [[PostServiceImpl]], [[PublishController]].

## Exact source

[services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java, lines 1–19](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>)

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;

import java.util.List;
import java.util.Locale;
import java.util.Optional;

public interface PostService {
    List<PostSummary> getFeatured();

    Optional<PostSummary> findById(long postId);

    Post publish(String username, String publisherEmail, String title, String artistName,
                 int releaseYear, String coverContentType, byte[] coverData, Locale locale);

    void notifyInterest(long postId, String contactName, String contactEmail, Locale locale);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
