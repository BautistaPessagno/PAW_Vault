---
title: "Known gaps and document drift"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "history"]
---

# Known gaps and document drift

This register distinguishes current source, historical requirements and unverified runtime claims at ff96f27. None of the referenced documents authorizes implementing its instructions during a documentation task.

| Document claim or assumption | Current source evidence | Consequence |
|---|---|---|
| Contact spec requires synchronous Spanish SMTP, 503 and retained values on delivery failure | Both mail methods are @Async; Locale is passed explicitly; controller’s failure branch and exception were deleted | Old contact spec/recovery issue do not describe current behavior |
| contactSent means publisher was notified | Flash is set after submitting normal async work; worker failures are swallowed | The success copy can appear even when delivery later fails |
| Async always avoids request blocking | taskExecutor uses CallerRunsPolicy | Saturated execution can run mail on the caller |
| README says startup leaves existing data untouched | schema.sql backfills users.username and drops albums.cover_path | Startup modifies supported older databases; old paths are discarded |
| README inline mail configuration is complete | EmailServiceImpl requires app.base-url; only the committed example includes it | Use the current example file for all required settings |
| Environment values replace classpath files | WebConfig retains required @PropertySource files | Environment-only deployment is not established by the README |
| Startup and manual schema are equivalent | Canonical/test schema omit FKs/year CHECK; database/albums.sql adds them | Effective guarantees depend on how the database was created |
| All legacy databases upgrade automatically | Targeted username/cover alterations only; setup rejects textual albums.artist | No complete posts.publisher_email or textual-artist conversion path |
| Any invalid uploaded cover yields a field error | Existing albums are returned before ImageService validation | Their incoming cover is ignored, including invalid nonempty uploads within the transport limit |
| A new publisher can fill an existing album’s empty cover | findOrCreate returns the album unchanged | A null cover stays null through this workflow |
| MIME validation proves valid image content | ImageService checks the declared label and byte count, without decoding | Accepted bytes may not form an image |
| Publish spec declares FKs/year constraints and excludes Post listing | Startup schema omits those constraints; landing lists Posts | Updated spec still contains stale sections |
| Landing spec says no links/buttons | Current JSP links to publish/contact | Old editorial requirements are historical |
| Child POMs never repeat sibling versions/scopes | Actual child POMs declare them | Setup’s centralization claim remains stronger than implementation |
| All deterministic check copies are identical | tools/paw_checks.py dropped Flyway; .claude/scripts copy retained it | Main CLI and agent hook checks differ |
| Pre-commit runs Maven | Versioned hook invokes the Python checker only | A successful hook is not a test/build result |
| No deletes means no orphan references | Startup schema has no FKs; DAO test inserts a nonexistent publisher ID | INNER JOIN results can omit orphan Posts; dangling image IDs yield 404 |
| Retry message proves a uniqueness race | publish catches any DataIntegrityViolationException | Other integrity errors can receive the same retry text |

## Remaining implementation limits

No authentication, roles, payment, price/condition/stock, search/filter/pagination, edit/delete or persistent contact history exists. User rows still represent unauthenticated publishers. Welcome dispatch is not coordinated with commit; no outbox, durable mail queue, retry record or delivery confirmation exists.

The old fixed cover, inherited create/profile routes and unused album listing are removed. Optional database images and seven JSP components are implemented in source. The older provisional UI note with eleven tags is superseded.

Actual deployed database constraints, SMTP availability, remote task status and first course deployment remain unverified. Source/tests are not a live runtime check.

## Evidence paths

- [Contact requirements](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) and [recovery issue](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md>), compared with [[PostContactController]] and [[EmailServiceImpl]].
- [README](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/README.md>), compared with [[Database schema]] and [[Configuration and running]].
- [Publishing spec](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>), compared with [[Publish flow]] and [[Schema history and seeds]].

[[History and specifications]] · [[Testing and evidence]] · [[Transactions and concurrency]]
