---
title: "Contact flow"
categories: ["Flows", "Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java"]
---

# Contact flow

GET /post/{postId}/contact requires authentication. [[InquiryServiceImpl]] loads the summary and rejects a missing post with 404, a sold post with 409 or self-contact with 403. The page shows a compact card and an optional message of at most 500 characters. Name and reply address come from the account principal.

On POST the controller normalizes CRLF to LF and trims the message before validation. The service locks the publication row, checks contactability again, inserts a PENDING Inquiry and requests an interest email with authenticated buyer identity. The seller's persisted preferred locale determines the mail language.

Success redirects to / with contactSent. The inquiry transaction is independent of eventual SMTP delivery, so the seller can read the request in /inquiries even if the worker logs a mail failure. Dispatch occurs before commit, however; there is no outbox or after-commit guarantee. The success message establishes normal service completion, not receipt of email.

The submit-once script reduces accidental duplicate clicks on this form. There is no unique buyer/post constraint or server idempotency key, so repeated valid requests may create separate inquiries. They are initial requests with statuses, not a reply thread.

[[Inquiry and sale flow]] · [[Mail delivery]] · [[Transactions and concurrency]]
