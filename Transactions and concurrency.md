---
title: "Transactions and concurrency"
categories: ["Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "services"]
---

# Transactions and concurrency

[[WebConfig]] enables Spring transaction interception and provides DataSourceTransactionManager. A transaction belongs to the database connection used by cooperating JdbcTemplate calls. A RuntimeException escaping a transactional service causes rollback under the default Spring rules.

| Method | Declared transaction | Consequence |
|---|---|---|
| [[PostServiceImpl]].publish | Read/write | User, Artist, Album and Post changes share one transaction |
| PostServiceImpl.getFeatured/findById | Read-only | Bounded read operation |
| PostServiceImpl.notifyInterest | None | Lookup completes without a service transaction held during SMTP |
| [[UserServiceImpl]].create/findOrCreate | Read/write | Joins outer publish transaction or starts its own |
| UserServiceImpl.findById | Read-only | User lookup boundary |
| [[ArtistServiceImpl]].findOrCreate | Read/write | Joins publish when invoked there |
| [[AlbumServiceImpl]].findOrCreate | Read/write | Joins publish when invoked there |
| AlbumServiceImpl.getFeatured | None | Actual code differs from the general read-only guidance |

UserServiceImpl's call from findOrCreate to its own create does not cross a Spring proxy. It remains transactional because findOrCreate already has a transaction. Mockito tests construct services directly, so annotations are inactive in those tests.

## Why the database constraint is necessary

Two requests can both read “missing” before either writes. A preliminary existence query therefore cannot prevent duplicates. The unique indexes on normalized identities and the Post pair determine which insert succeeds. [[PostJdbcDao]] translates duplicate-key insert errors, and [[PostServiceImpl]] translates them again into controller-facing exceptions.

The other integrity-error catch in publish is intentionally broad. It reports a concurrent-publish message even if some different integrity problem occurred. The code does not retry internally, inspect the violated constraint or re-query after an aborted PostgreSQL transaction. A manual retry may succeed after a racing request commits, but the name alone is not proof of that situation.

## Mail and commit are separate

A new User triggers [[EmailServiceImpl]].sendWelcomeEmail through an async proxy before the outer transaction commits. Database rollback cannot undo that mail. There is no after-commit event, outbox table or transactional message broker. A welcome may therefore describe a user whose publication later failed. Contact sending avoids a long database transaction but still occupies the request while waiting for SMTP.

No live concurrency test or transaction rollback experiment was run for this documentation. [[Testing and evidence]] distinguishes mock assertions from database guarantees.
