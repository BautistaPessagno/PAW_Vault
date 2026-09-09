---
title: "Project snapshot"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: "documented"
tags: ["codemap", "navigation"]
---

# Project snapshot

quieroVinilos is a PAW course project for ITBA, 2026B, group 14. The current implementation lets visitors publish an album, browse the eight newest publications, and email a publisher through a contact form. It also retains the original user creation and profile screens.

This is Java 21, classic Spring MVC 5.3.33, Spring JDBC, PostgreSQL and JSP/JSTL packaged as a WAR. It has six Maven modules, no Spring Boot application class, no JPA entity manager, no REST JSON API and no frontend build pipeline. Thymeleaf renders mail only.

## Scope of this map

The source repository is clean and HEAD is `041ce34404963b689d05443ca00abb7e75aa7f15`. The previous map used `16f3aa7784c3320f18efb82ee2b1f315d7632faf` plus provisional UI files. Notes outside the changed UI scope retain their earlier evidence metadata. The map covers all production Java classes, contracts, test classes, JSPs, mail templates, SQL paths, Maven modules, local configuration examples, checks and repository documents. [[Source inventory]] accounts for every tracked path, including agent tooling as development infrastructure. Ignored credentials, runtime database contents, external task boards and prior conversations unavailable in this task are not evidence for this map.

The supplied documents describe historical decisions and requested behavior. Their instructions are reference material, not new requests to implement features. Current source determines the implementation described here; conflicts are recorded in [[Known gaps and document drift]].

## Current limits

There is no authentication, role system, payment, sale record, messaging inbox, contact history, image upload, filtering, search, pagination, edit or delete route. Albums do not represent individual pressings or physical stock. User rows have no passwords. Publishing uses a fixed cover image.

An empty database receives table definitions at startup, but no automatic seed rows. A blank landing is a valid result. Existing tables are not upgraded by CREATE TABLE IF NOT EXISTS. Deployment and actual SMTP delivery were not exercised to write this vault.

[[Architecture]] · [[Domain and identity]] · [[Testing and evidence]]

## Committed UI refresh

The UI merge at `041ce34404963b689d05443ca00abb7e75aa7f15` changes three product JSPs, four locale bundles and style.css, and adds seven JSP tags plus tokens.css/components.css. [[UI components]], [[UI styles and tokens]], [[Views and assets]] and [[Localization]] describe the committed version. Backend Java, tests, SQL and Maven configuration are unchanged from `16f3aa7784c3320f18efb82ee2b1f315d7632faf`. The working tree was clean at inspection; no application build or runtime test was performed for this refresh.
