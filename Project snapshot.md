---
title: "Project snapshot"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "navigation"]
---

# Project snapshot

quieroVinilos is the ITBA PAW 2026B group 14 project. This vault describes commit `ff96f275ae009bad4534751b7a4857cf45aea7ac`, including the merged image upload, asynchronous contact mail and dead-code cleanup. The local source checkout was clean at that exact commit when checked.

Visitors can browse the eight newest publications, publish an album with an optional cover and request contact with its publisher. Images live in PostgreSQL and are served by ID. Both welcome and interest mail use asynchronous delivery and the request Locale. The inherited /create and /profile routes are removed.

The application uses Java 21, classic Spring MVC 5.3.33, Spring JDBC, PostgreSQL and JSP/JSTL across six Maven modules. Thymeleaf renders email only. The WAR is now `webapp/target/app.war`.

## Scope and limits

[[Source inventory]] maps every tracked path. Each current Java class/interface/test has a note; removed Java notes are marked History with their prior source revision. Exact excerpts describe source, not runtime results. Source documents and copied prompts remain references rather than instructions to execute.

There is no authentication, role system, payment, stock, price, search, pagination, image replacement, edit/delete or persistent conversation history. Album identity still uses artist/title/year. A submitted cover is ignored when the album already exists, including when its stored cover is null.

The startup script creates tables and now also backfills usernames and replaces cover_path with nullable cover_image_id. It does not support every legacy schema. No deployment, SMTP delivery or PostgreSQL upgrade was exercised for this refresh.

[[Cover image flow]] · [[Mail delivery]] · [[Known gaps and document drift]] · [[Verification record]]
