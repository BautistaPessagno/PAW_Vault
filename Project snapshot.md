---
title: "Project snapshot"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: []
---

# Project snapshot

quieroVinilos is the ITBA PAW 2026B group 14 project. This vault describes `40328f0a23ce3814ab62a9f0124a6ba1e6ae71be`, fetched from origin/main on 2026-09-16. The user switched the local source checkout to main during this refresh; local HEAD now matches that revision and the working tree is clean. The diff from ff96f27 contains 125 changed or added paths.

Visitors browse up to 16 available exemplars using text search, sorting and combined genre/condition/artist/year/price filters. Accounts register by email and choose credentials after following a verification link. Authenticated users publish and send persistent inquiries; sellers accept or reject inquiries in their inbox. Acceptance sells the exemplar and rejects its remaining pending inquiries. ADMIN adds access to an informational administration page.

Each publication owns its commercial details and optional image. Album identity remains artist/title/year, with a legacy album-cover fallback. The six-module application uses Java 21, Spring MVC/JDBC 5.3.33, Spring Security 5.8.16, PostgreSQL, JSP/JSTL and Thymeleaf email. The WAR is webapp/target/app.war.

There is no payment processing, pagination, multiple-unit stock workflow, edit/delete interface, password-reset flow, token expiry or durable mail queue. The persisted inquiry is an initial message and status, not a threaded conversation. The user/album uniqueness rule remains even after a sale.

[[Source inventory]] maps every tracked path. Exact excerpts and flow descriptions establish source behavior only. No application deployment, live PostgreSQL migration, HTTP smoke test or SMTP delivery was performed for this refresh. See [[Testing and evidence]] and [[Verification record]].
