---
title: "Validation and errors"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java"]
---

# Validation and errors

Spring binds form values before Bean Validation. Controllers with BindingResult redisplay field/global errors. Security filters authenticate and validate CSRF before the protected controller action. Publish identity and contact identity come from the principal.

| Input | Source rules |
|---|---|
| Publish title/artist | Required, at most 255 characters |
| Release year / optional pressing year | Integer 1000–9999 |
| Price | Required integer 1–99,999,999 |
| Optional zone / description | At most 100 / 1000 characters |
| Optional contact message | CRLF normalized to LF and trimmed; at most 500 characters |
| Registration email | Trimmed, required, email format, at most 100 characters |
| Verification | Nonblank token and username; username at most 100; password 12–72 characters with ASCII letter/digit and matching confirmation |
| Cover | Optional; allowed MIME label and at most 5 MiB; whole request at most 6 MiB |
| Search | Query over 255 gives 400; malformed/out-of-range filters ignored |

Publish strings are not trimmed before annotation checks, while contact/email/verification username have binder normalization. Passwords are not trimmed, and @Size is a character count rather than a UTF-8 byte count. Service APIs rely on the controller for most form constraints.

| Error | HTTP or form result |
|---|---|
| InvalidImageException | Cover field error |
| DuplicatePostException / ConcurrentPublishException | Global publish error |
| DuplicateUserException | Registration email error |
| Invalid/reused verification token | Global verification error |
| Multipart overflow | Redirect to /publish?coverTooLarge with fresh form |
| Missing post/inquiry/image | 404 |
| Self-contact / wrong seller / route denial | 403 |
| Sold contact / invalid inquiry transition | 409 |
| InvalidSearchQueryException | 400 |
| Rendering/SMTP exception inside mail worker | Log and swallow |

ErrorController handles explicit 403/404 pages; web.xml forwards unmatched-route 404. Controllers select 400/409 JSPs for their own handlers. IOException while reading an upload has no dedicated local mapping. Form inputs use escaped values, and password fields are never repopulated by ui:text-input.

[[Authentication flow]] · [[UI components]] · [[Known gaps and document drift]]
