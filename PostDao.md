---
title: "PostDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java"]
---

# PostDao

The posts persistence contract. `findFeatured(limit)` returns joined summaries, `findById(id)` returns Optional, `existsByUserIdAndAlbumId` checks the unique pair, and `create` inserts a [[Post]]. [[PostJdbcDao]] implements it. [[PostServiceImpl]] consumes it without compiling against the JDBC implementation.

## Connections

Project types referenced: [[Post]], [[PostSummary]].

Referenced by: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java, lines 1–17](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSummary;

import java.util.List;
import java.util.Optional;

public interface PostDao {
    List<PostSummary> findFeatured(int limit);

    Optional<PostSummary> findById(long id);

    boolean existsByUserIdAndAlbumId(long userId, long albumId);

    Post create(long userId, long albumId);
}
```

## Context

[[Architecture]] · [[Domain and identity]] · [[Source inventory]]
