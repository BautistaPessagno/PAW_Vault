---
title: "Transactions and concurrency"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "services"]
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Transactions and concurrency

[[WebConfig]] enables transaction proxies and a DataSourceTransactionManager. Cooperating JdbcTemplate calls use the same transaction connection. Runtime exceptions leaving transactional services trigger rollback under the declared defaults.

| Method | Declared transaction | Effect |
|---|---|---|
| [[PostServiceImpl]].publish | Read/write | User, Artist, optional Image, Album and Post share one transaction |
| PostServiceImpl.getFeatured/findById | Read-only | Summary reads |
| PostServiceImpl.notifyInterest | None | Reads one summary and delegates asynchronous email |
| [[UserServiceImpl]].findOrCreate | Read/write | Private create helper participates in this transaction |
| UserServiceImpl.findById | Read-only | Publisher lookup |
| [[ArtistServiceImpl]].findOrCreate | Read/write | Joins outer publish transaction |
| [[AlbumServiceImpl]].findOrCreate | Read/write | Existing album skips cover creation; new album can store cover |
| [[ImageServiceImpl]].create/findById | Read/write / read-only | Image bytes inserted/read through ImageDao |

AlbumService.getFeatured and public UserService.create have been removed. Same-instance calls to the private create helper do not cross a proxy; the outer findOrCreate transaction already exists. Mockito service construction activates neither transactions nor async dispatch.

## Concurrent identities

SELECT then INSERT is not atomic. Unique constraints arbitrate User email, Artist name, Album artist/title/year and Post user/album. PostJdbcDao translates duplicate inserts and PostServiceImpl translates that marker to a field-level business error. Other DataIntegrityViolationException values receive the broad ConcurrentPublishException message, without inspecting the violated constraint or retrying.

A newly stored image rolls back if album/post creation later fails through the proxied publish transaction. Looking up an album before image creation avoids storing an unused image on the ordinary reuse path. This is source-derived transaction behavior; no concurrent PostgreSQL experiment was run.

## Mail is outside the commit guarantee

New-user welcome dispatch occurs before publish commit. A later database rollback cannot undo that email. There is no after-commit event or outbox. Contact mail also uses @Async and has no request-scoped delivery result. The bounded executor falls back to CallerRunsPolicy when saturated, so mail may still occupy the caller in that condition. [[Mail delivery]] describes the pool and failure handling.
