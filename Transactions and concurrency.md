---
title: "Transactions and concurrency"
categories: ["Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Transactions and concurrency

WebConfig enables transactional proxies with DataSourceTransactionManager. DAO calls made within a proxied service transaction share its connection; unchecked exceptions trigger rollback. Directly constructed service unit tests do not activate this behavior.

| Operation | Transaction and ordering |
|---|---|
| PostServiceImpl.search | Read-only summary query, limit 16 |
| PostServiceImpl.publish | Account lookup, artist/album resolution, duplicate check, optional image and post insert in one transaction |
| UserServiceImpl.register | Create/reuse pending account, store token, request verification mail |
| UserServiceImpl.verifyEmail | Conditional activation, token deletion and welcome dispatch |
| InquiryServiceImpl.submit | Lock post, validate buyer/status, create inquiry, request interest mail |
| InquiryServiceImpl.accept | Lock post, authorize seller, sell post, accept chosen pending inquiry, reject competitors |
| InquiryServiceImpl.reject | Lock post, authorize seller, reject pending inquiry |
| Lookup/list/image reads | Read-only service transactions where declared in linked code notes |

Unique constraints arbitrate account email, artist name, album artist/title/year and post user/album. SELECT-before-INSERT does not make those sequences atomic. The publish service translates DuplicatePostKeyException specifically; other integrity errors receive ConcurrentPublishException without inspecting the violated constraint. That broad error does not prove a retry will succeed.

PostJdbcDao first issues SELECT id ... FOR UPDATE, then reads the joined summary. All inquiry mutations use this post lock. Conditional updates provide an additional state guard. If accepting an already closed inquiry follows a successful SOLD update, the service exception relies on transaction rollback to restore the post.

User activation uses WHERE enabled=FALSE; an already activated account cannot have its credentials overwritten through a second link. Re-registration does not delete previous pending tokens. Publication uniqueness also remains after sale.

All three mail triggers occur before the service transaction commits. An async worker may send a message before a subsequent rollback. No after-commit listener or outbox is present. CallerRunsPolicy can execute mail on the calling thread when the bounded pool is saturated. [[Mail delivery]] explains the failure handling.

[[Inquiry and sale flow]] · [[Database schema]] · [[Testing and evidence]]
