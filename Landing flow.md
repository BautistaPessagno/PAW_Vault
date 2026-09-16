---
title: "Landing flow"
categories: ["Flows", "Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java"]
---

# Landing flow

Public GET / uses one search contract for an empty catalog query and all combinations of filters. [[LandingController]] binds the URL, [[PostServiceImpl]] normalizes it, and [[PostJdbcDao]] returns at most 16 AVAILABLE publications. The controller separately loads the artist options once. No per-card lookup is performed.

| Parameter | Behavior |
|---|---|
| q | Trimmed; blank means no text filter; over 255 characters returns 400 |
| sort | Ten [[PostSort]] values; missing/invalid becomes NEWEST |
| genre, condition | Fixed enum values; case-insensitive binding, invalid becomes absent |
| artistId | Positive ID; malformed/nonpositive ignored |
| year | Release year 1000–9999; invalid ignored |
| minPrice, maxPrice | Inclusive bounds 1–99,999,999; invalid bounds ignored; inverted valid range drops both |

All applied filters combine with AND. Text searches case-insensitive title or artist substrings and treats percent, underscore and backslash literally through escaped LIKE parameters. Enum sort choices map to fixed SQL fragments. Price sorts put legacy null prices last. Newest uses created_at DESC then id DESC; oldest uses both ascending. Other sorts break ties by newest.

The JSP submits a GET form, preserving selected values in the URL. Clear removes query/filters and retains a nondefault sort. It distinguishes no publications, no text matches and no filter matches. Cards link to protected contact pages. There is no total count or pagination.

The controller exposes parsed numeric filters to the view before service normalization. Consequently an out-of-range value can remain visible even though it is ignored by SQL. [[Known gaps and document drift]] records this source distinction.

[[Views and assets]] · [[PostSearchCriteria]] · [[SearchResult]] · [[PostJdbcDaoTest]]
