---
title: "Publish flow"
categories: ["Flows", "Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# Publish flow

GET /publish requires a session and renders the album and exemplar form. Publisher identity comes from [[AuthenticatedUser]], not posted username/email. The form requires title, artist, release year and price. Genre, physical condition, pressing year, zone, description and photo are optional; stock is absent.

POST /publish passes multipart parsing and CSRF validation before MVC validation. The controller passes the principal ID and form data into one transaction in [[PostServiceImpl]]. It loads the account, resolves normalized artist/title/year, checks the user/album uniqueness rule, optionally stores a new Image, then inserts an AVAILABLE Post with stock=1. Existing albums retain their genre; each new publication can have its own image.

DuplicatePostException and ConcurrentPublishException become global form errors. InvalidImageException becomes a cover field error. The controller rebuilds enum options on redisplay; success redirects to /. Validation preserves ordinary values but a browser file input must be reselected. An oversized multipart request redirects to /publish?coverTooLarge and loses submitted values.

The uniqueness check includes sold publications, so the same account cannot publish another exemplar of the same album through this flow. Publishing does not create an account or send welcome mail. [[Authentication flow]] owns registration and welcome dispatch.

[[Cover image flow]] · [[Validation and errors]] · [[Transactions and concurrency]]
