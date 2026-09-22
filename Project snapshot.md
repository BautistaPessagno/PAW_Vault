---
title: "Project snapshot"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: []
---

# Project snapshot

quieroVinilos is the ITBA PAW 2026B group 14 project. This vault describes `f12af080cf6a27101160f005102a20f436574cf7`, the merge of PR #33 on 2026-09-22 and the head of the local main branch, which matches the local origin/main ref; no fetch was performed. The working tree was clean. The diff from `40328f0` contains 101 commits and 168 changed, added or deleted paths.

Visitors browse available exemplars 15 per page using a header search with autocomplete, sorting, and combined genre/condition/year/price filters, and open a public detail page for any publication. Accounts register by email and choose credentials after following a verification link; they can later change username and password from their profile or recover a forgotten password through a one-hour emailed link. Authenticated users publish with a live preview, edit or delete their AVAILABLE publications, and send persistent inquiries. The inbox is split into received and sent views grouped by publication. Sellers accept an inquiry after a confirmation dialog, which sells the exemplar, rejects the remaining pending inquiries and emails the buyer. ADMIN adds access to an informational administration page.

Each publication owns its commercial details and optional image; genre, condition and a positive price are now required. Artist identity ignores case and punctuation while keeping the typed display name, and album identity compares titles case-insensitively. Mail is sent only after the originating transaction commits. The six-module application uses Java 21, Spring MVC/JDBC 5.3.33, Spring Security 5.8.16, PostgreSQL, JSP/JSTL and Thymeleaf email. The WAR is webapp/target/app.war, and a `pampero` Maven profile packages course-server configuration.

There is no payment processing, multi-unit stock, reply thread, durable mail queue, verification-token expiry or logout of other sessions after a password change. The persisted inquiry is an initial message and status. The user/album uniqueness rule remains even after a sale, and editing a post can rewrite shared artist and album display data.

[[Source inventory]] maps every tracked path. Exact excerpts and flow descriptions establish source behavior only. No application deployment, live PostgreSQL migration, HTTP smoke test, Maven run or SMTP delivery was performed for this refresh. See [[Testing and evidence]], [[Known gaps and document drift]] and [[Verification record]].
