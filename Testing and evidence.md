---
title: "Testing and evidence"
categories: ["Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java", "persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java", "services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java", "services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java"]
---

# Testing and evidence

The source has eight DAO test suites, eight service test suites and a shared TestConfiguration, with 234 test methods in total: 126 in persistence and 108 in services, up from 108 at `40328f0`. This refresh inspects source and validates the vault; it does not report a new Maven run.

| Area | Test source |
|---|---|
| Registration, verification, profile and passwords | [[UserServiceImplTest]], [[UserJdbcDaoTest]], [[EmailVerificationTokenJdbcDaoTest]], [[PasswordResetTokenJdbcDaoTest]] cover pending/existing accounts, conditional activation, username updates, compare-and-set password change, reset requests for unknown/pending/concurrent cases, expiry, single use and after-commit mail |
| Search, suggestions, paging and posts | [[PostServiceImplTest]], [[PostJdbcDaoTest]], [[PaginationTest]] cover query normalization and limits, invalid filters, sort orders, literal wildcards, look-ahead catalog pages, profile pages with totals, suggestions ranking, edit and delete ownership/status rules, and page arithmetic |
| Inquiry, inbox and sale | [[InquiryServiceImplTest]], [[InquiryJdbcDaoTest]] cover contactability, grouped inbox pages including deleted posts, group counts, seller checks, guarded transitions, competitor rejection, detachment and acceptance mail after commit |
| Catalog and image | [[AlbumServiceImplTest]], [[AlbumJdbcDaoTest]], [[ArtistServiceImplTest]], [[ArtistJdbcDaoTest]], [[ImageServiceImplTest]], [[ImageJdbcDaoTest]] cover case-insensitive and separator-insensitive identity, required genre, metadata rewrite on edit, accent-insensitive suggestions, image bytes, delete and MIME/size rules |
| Mail | [[EmailServiceImplTest]] uses real templates with a fake sender, checking links, optional messages, addresses, English copy, the inquiries call to action, the buyer acceptance notice and swallowed failures |

DAO suites run against fresh HSQLDB schemas using Spring test transactions and fixtures. They do not execute production PostgreSQL ALTER, DO or backfill statements, and the HSQLDB schema uses an exact title constraint where PostgreSQL uses LOWER(title). Service suites use mocks and direct construction, so @Transactional and @Async proxies are absent. [[UserServiceImplTest]] and [[InquiryServiceImplTest]] initialize TransactionSynchronizationManager by hand and trigger afterCommit themselves, which checks that mail is registered for commit but not that a real rollback suppresses it. A sequence of mocked writes is not proof of rollback or concurrent locking.

No webapp test suite is tracked. There is no automated evidence for a real security filter chain, CSRF/session behavior, the logout after a password change, multipart binding and overflow redirects, JSP compilation, autocomplete or confirmation scripts, or deployed routes. PostgreSQL concurrency, the savepoint path in ArtistJdbcDao, SMTP delivery and a saturated mail pool need separate runtime checks.

Some test names still say Featured although they call the paged search, and many newer names use `Throws` where CLAUDE.md prescribes `Returns`. No test uses Mockito.verify or Mockito.spy. There is still no direct image-decode test because validation checks label and length only.

[[Verification record]] records the actual static checks and their limits. No source application changes, Maven build, database writes, server startup or SMTP call were made by this refresh.

## Evidencia local anterior, 2026-09-17

[[Audit local 2026-09-17]] ejecutó la rama `e5e926d`, anterior a `f12af08`. Sus pruebas manuales no cubren edición, borrado, paginación, perfil ni recuperación de contraseña.
