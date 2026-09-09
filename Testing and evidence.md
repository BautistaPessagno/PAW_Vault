---
title: "Testing and evidence"
categories: ["Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "testing"]
---

# Testing and evidence

Tests live in persistence and services. There are four DAO suites, five service suites and a shared persistence TestConfiguration. Each suite has its own linked note with exact source and test method names.

## Persistence suites

- [[ArtistJdbcDaoTest]] checks reuse and insertion.
- [[AlbumJdbcDaoTest]] checks projection mapping, unchanged cover on reuse and distinct release year.
- [[PostJdbcDaoTest]] checks summary mapping, missing lookup, existence, duplicate protection and a second publisher insert.
- [[UserJdbcDaoTest]] checks ID lookup, missing lookup and normalized email reuse/insertion.
- [[TestConfiguration]] wires HSQLDB and the fixture scripts.

## Service suites

- [[ArtistServiceImplTest]] checks normalized artist resolution.
- [[AlbumServiceImplTest]] checks normalized title and default-cover input while preserving returned stored cover.
- [[UserServiceImplTest]] checks normalized creation and existing/new user paths.
- [[PostServiceImplTest]] checks duplicate branches, reuse, missing contact and delivery exception propagation.
- [[EmailServiceImplTest]] uses actual templates and a capturing mail sender to inspect messages and failure policy.

Persistence tests run HSQLDB with PostgreSQL syntax compatibility, Spring injection and rollback. They use a different schema resource from production. Service tests use direct instances with Mockito or a fake sender, so @Transactional and @Async are not active.

## What is not established

No webapp test suite exists. There is no automated controller check for 503 status and retained form values, 404 routing, JSP compilation, binding errors or redirect flash behavior. The real PostgreSQL publish transaction, identity races and startup on legacy schemas are not covered by mock-based service tests. The second-publisher DAO test uses an absent user ID, illustrating the missing foreign-key enforcement. The successful interest test asserts no exception, not the actual normalized payload. No ConcurrentPublishException test is present.

## Verification for this documentation

The codemap was checked against source and static reference inventories. Repository deterministic checks and vault validation results are recorded in [[Verification record]]. No Maven build, live database mutation, server launch or real SMTP delivery was required or performed for this documentation-only change. Test source presence and prior issue claims are not presented as a fresh passing test run.

To run project tests separately, the source repository documents `mvn test`. Module-specific runs need sibling dependencies available; the full reactor avoids stale installed sibling artifacts. [[Development tools]] describes the deterministic checks and their limits.
