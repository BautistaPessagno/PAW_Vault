---
title: "PostService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java"]
---

# PostService

The controller-facing publication API. `getFeatured()` supplies the landing, `findById` supplies the contact form, `publish` returns the created [[Post]], and `notifyInterest` sends a contact notification without returning a persisted object. Its implementation [[PostServiceImpl]] owns business orchestration; controllers handle binding, views and HTTP outcomes.

## Connections

Project types referenced: [[Post]], [[PostSummary]].

Referenced by: [[LandingController]], [[PostContactController]], [[PostServiceImpl]], [[PublishController]].

Tests: no direct test source reference. See [[Testing and evidence]].

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
                 int releaseYear, Locale locale);

    void notifyInterest(long postId, String contactName, String contactEmail);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
