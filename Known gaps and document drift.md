---
title: "Known gaps and document drift"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
tags: ["codemap", "history"]
---

# Known gaps and document drift

This register separates current source facts from historical instructions, future work and unverified deployment claims.

| Document claim or potential assumption | Current source evidence | Practical implication |
|---|---|---|
| All public mail methods are async | [[EmailServiceImpl]] marks only welcome @Async | Contact intentionally waits and can return 503 |
| A running migration system initializes the app | [[WebConfig]] loads schema.sql only | V1/V2/V3 are not automatically applied |
| Setup documents an AdminBootstrap and roles | No such Java type, property or security module in source | No implemented admin bootstrap or permissions |
| Shared custom JSP tag files exist | Seven tags are committed in the UI merge | [[UI components]] documents the refreshed view composition |
| Child dependencies omit version/scope | [[Build and dependencies]] shows explicit sibling versions/runtime scopes | Read the actual POMs |
| Post stores publisher email | Current [[Post]] stores userId | Historical V2/V3 are incompatible with current DAO expectations |
| Landing shows catalog AlbumSummary sorted by year | [[LandingController]] uses PostService and newest Post IDs | Unpublished albums are absent |
| Landing has no actions | Current JSP links to publish and contact | Old editorial acceptance criteria are stale |
| All model IDs are boxed Long | Current models use primitive long | No nullable association IDs in these constructors |
| All reads are transactional | AlbumServiceImpl.getFeatured has no annotation | General instruction differs from implementation |
| All visible strings are localized | Legacy user JSPs retain English literals | New feature localization does not cover scaffold |
| Pre-commit forces Maven tests | The Git hook only runs paw_checks.py | A successful commit hook is not a Maven test result |
| Environment values alone replace property files | Required @PropertySource files remain | README deployment alternative needs configuration work |
| A schema without deletes cannot have orphans | No startup foreign keys; DAO test inserts userId 2 with no User row | External/invalid writes can disappear from INNER JOIN summaries |
| Contact recovery is wholly unimplemented | Controller already has 503 + preserved-form path | Outstanding issue asks for web-layer testing |
| Retry message proves a race | Publish catches any DataIntegrityViolationException | Other integrity errors can receive misleading retry text |

## Implementation limitations

Authentication, authorization, upload, price/condition/stock, search/filter/pagination, edit/delete, and persistent contact history are absent. New album covers all use versus.png. Name/title normalization discards original casing. No complete migration path for an old publisher_email Post schema is wired into startup. CREATE TABLE IF NOT EXISTS does not upgrade existing tables.

Welcome mail is dispatched before database commit. Contact mail lacks durable deduplication and retry history. No explicit missing-user 404 mapping exists on the inherited profile route. Form validation differs between publishing and legacy user creation. These are source-derived observations, not claims of a live exploit or failure reproduced in production.

Actual deployed database constraints, external board status, SMTP availability and course server readiness remain unverified. The vault does not replace a runtime test.

[[Transactions and concurrency]] · [[Testing and evidence]] · [[History and specifications]]

## Committed UI refresh

The UI merge at `041ce34404963b689d05443ca00abb7e75aa7f15` changes three product JSPs, four locale bundles and style.css, and adds seven JSP tags plus tokens.css/components.css. [[UI components]], [[UI styles and tokens]], [[Views and assets]] and [[Localization]] describe the committed version. Backend Java, tests, SQL and Maven configuration are unchanged from `16f3aa7784c3320f18efb82ee2b1f315d7632faf`. The working tree was clean at inspection; no application build or runtime test was performed for this refresh.

The earlier vault snapshot described four provisional tags, disabled buttons, spotlight cards and plain HTML form wrappers. The committed source omits those tags/options and uses Spring form:form with relative field paths. The current notes and excerpts replace that provisional description.

The legacy create JSP loads only style.css, whose variables are defined by tokens.css. Its appearance has not been verified in a browser. [[UI styles and tokens]] records the source-level dependency.
