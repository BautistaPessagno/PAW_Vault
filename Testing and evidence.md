---
title: "Testing and evidence"
categories: ["Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java", "services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# Testing and evidence

The source has seven DAO test suites, seven service test suites and a shared TestConfiguration. This refresh inspects source and validates the vault; it does not report a new Maven run.

| Area | Test source |
|---|---|
| Registration/verification | [[UserServiceImplTest]], [[UserJdbcDaoTest]], [[EmailVerificationTokenJdbcDaoTest]] cover pending/existing accounts, normalized email, conditional activation and token deletion |
| Search/filter/sort | [[PostServiceImplTest]], [[PostJdbcDaoTest]] cover query normalization/limits, invalid filters, sort orders, combined filters, literal wildcards and available-only listings |
| Inquiry/sale | [[InquiryServiceImplTest]], [[InquiryJdbcDaoTest]] cover contactability, seller checks, guarded transitions, competitor rejection and seller locale |
| Catalog/image | [[AlbumServiceImplTest]], [[AlbumJdbcDaoTest]], [[ArtistServiceImplTest]], [[ArtistJdbcDaoTest]], [[ImageServiceImplTest]], [[ImageJdbcDaoTest]] cover identity, genre, listing, bytes and MIME/size rules |
| Mail | [[EmailServiceImplTest]] uses real templates with a fake sender, checking verification links, optional messages, addresses, English copy, home links and swallowed failures |

DAO suites run against fresh HSQLDB schemas using Spring test transactions and fixtures. They do not execute production PostgreSQL ALTER/DO upgrades. Service suites use mocks/direct construction, so @Transactional and @Async proxies are absent. A sequence of mocked writes is not proof of rollback or concurrent locking.

No webapp test suite is tracked. There is no automated evidence here for a real security filter chain, CSRF/session behavior, multipart binding/overflow, JSP compilation or deployed routes. PostgreSQL concurrency, SMTP delivery and queue saturation need separate runtime checks. The guarded-lock DAO test reads a locked row but does not establish multi-connection race behavior.

Some old test method names still say findFeatured even though they invoke the unified search API. PostServiceImplTest also retains a DefaultStock name while stock is now fixed by the DAO. The code excerpts show the actual assertions. There is no direct image-decode test because validation checks label/length only.

[[Verification record]] records the actual static checks and their limits. No source application changes, Maven build, database writes, server startup or SMTP call were made by this refresh.
