---
title: "Testing and evidence"
categories: ["Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "testing"]
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java", "services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# Testing and evidence

The source contains five persistence DAO suites, six service suites and one shared TestConfiguration. Each has a linked source note. This refresh inspects their assertions; it does not report a new Maven run.

| Area | Source evidence |
|---|---|
| [[ImageJdbcDaoTest]] | Binary read, missing ID and insert |
| [[AlbumJdbcDaoTest]] | Identity lookup, uniqueness, different year and nullable image reference |
| [[PostJdbcDaoTest]] | Summary image-ID mapping, lookup, duplicate pair and second publisher |
| [[ArtistJdbcDaoTest]], [[UserJdbcDaoTest]] | Existing identity and insertion/lookup paths |
| [[ImageServiceImplTest]] | Wrong MIME, empty/oversize bytes and valid labeled bytes |
| [[AlbumServiceImplTest]] | Existing cover retained; new album with provided/null/empty cover |
| [[PostServiceImplTest]] | Duplicate branches, catalog reuse and contact lookup paths with Locale |
| [[EmailServiceImplTest]] | Addresses/body, English copy, absolute CTA, and swallowed welcome/contact failures |
| [[UserServiceImplTest]], [[ArtistServiceImplTest]] | Identity normalization and reuse |

Persistence tests use fresh HSQLDB schemas, Spring injection and rollback. They do not execute PostgreSQL’s production ALTER/UPDATE statements. Service tests use direct objects with mocks or a capturing sender, so transaction and @Async proxies are inactive. Email tests render real templates but use a StaticMessageSource and fake SMTP sender.

## What remains unverified

There are no webapp tests for multipart binding, oversized requests, file-input retry behavior, cover Content-Type/cache/404, JSP compilation, contact redirects or locale propagation through a real async proxy. There is no pool-saturation, durable delivery or actual PostgreSQL concurrency test. No test demonstrates a real upload can be decoded; ImageService checks MIME labels and byte size only.

The normal contact service test asserts no exception rather than the normalized notification payload. No ConcurrentPublishException test exists. The second-publisher DAO test inserts user ID 2 without a corresponding users row, matching the lack of foreign-key enforcement in that test schema.

[[Verification record]] records vault/source checks and the actual static checker results. No server, database mutation, SMTP call, Maven build or test run was performed in this refresh.
