---
title: "Inquiry and sale flow"
categories: ["Flows", "Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java"]
---

# Inquiry and sale flow

Authenticated GET /inquiries lists the principal's received and sent inquiries, newest first. The joined [[InquirySummary]] includes the buyer/seller display names, album, optional message and inquiry/post states. The view offers accept/reject only for received PENDING inquiries whose publication is AVAILABLE.

POST /inquiries/{id}/accept verifies ownership in [[InquiryServiceImpl]]. It reads the inquiry, locks its post with FOR UPDATE and compares post.userId with the principal ID. In the same transaction it changes AVAILABLE to SOLD, changes the chosen PENDING inquiry to ACCEPTED and rejects the other PENDING inquiries. If either guarded single-row write fails, an exception rolls the transaction back and the controller returns 409.

POST /inquiries/{id}/reject uses the same publication lock and ownership check, then conditionally changes that inquiry from PENDING to REJECTED. Missing inquiry/post returns 404; another owner's request returns 403. The service reject method guards inquiry state but does not separately require AVAILABLE post status. The UI applies that extra visibility condition.

```mermaid
flowchart LR
    A[AVAILABLE post and PENDING inquiry] -->|Owner accepts| S[SOLD post]
    A -->|Owner accepts| I[Chosen inquiry ACCEPTED]
    A -->|Owner accepts| R[Other pending inquiries REJECTED]
    P[PENDING inquiry] -->|Owner rejects| X[REJECTED inquiry]
```

Submission, acceptance and rejection serialize on the same post row under service transactions. Sold posts disappear from search and reject new contact requests. Accept/reject redirect to the inbox with a flash message. There is no payment, stock decrement, reopen/cancel operation or acceptance email in these methods.

This describes transaction declarations and guarded SQL, not a fresh concurrent PostgreSQL test. See [[Transactions and concurrency]], [[InquiryServiceImplTest]] and [[InquiryJdbcDaoTest]].
