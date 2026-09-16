---
title: "PostDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java"]
---

# PostDao

Publication search, summary lookup, locking lookup, duplicate-pair check, creation and guarded sale transition. Criteria and limits cross this interface without JDBC types. Locking calls require the service transaction to retain the row lock.

## Connections

Project types referenced: [[Condition]], [[Post]], [[PostSearchCriteria]], [[PostSummary]].

Referenced by: [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

## Exact source

[persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>)

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostSummary;

import java.util.List;
import java.util.Optional;

public interface PostDao {
    List<PostSummary> search(PostSearchCriteria criteria, int limit);

    Optional<PostSummary> findById(long id);

    Optional<PostSummary> findByIdForUpdate(long id);

    boolean existsByUserIdAndAlbumId(long userId, long albumId);

    Post create(long userId, long albumId, int price, String description, Condition condition,
                Integer pressingYear, String zone, Long imageId);

    boolean markSoldIfAvailable(long id);
}
```

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
