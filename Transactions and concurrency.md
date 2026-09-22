---
title: "Transactions and concurrency"
categories: ["Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java"]
---

# Transactions and concurrency

WebConfig enables transactional proxies with DataSourceTransactionManager. DAO calls made within a proxied service transaction share its connection; unchecked exceptions trigger rollback. Directly constructed service unit tests do not activate this behavior, although two suites initialize transaction synchronization by hand to run after-commit callbacks.

| Operation | Transaction and ordering |
|---|---|
| PostServiceImpl.search / findSearchSuggestions / findByPublisherId | Read-only; page of 16 look-ahead rows, five suggestions, or count plus twelve rows |
| PostServiceImpl.publish | Account lookup, artist/album resolution, duplicate check, optional image and post insert |
| PostServiceImpl.update | Lock post, require owner and AVAILABLE, resolve and possibly rewrite shared artist/album, optional new image, guarded update |
| PostServiceImpl.delete | Lock post, require owner and AVAILABLE, read own image, detach inquiries, delete post, delete own image |
| UserServiceImpl.register / verifyEmail | Create or reuse pending account and token; conditional activation and token deletion; mail after commit |
| UserServiceImpl.updateUsername / changePassword | Single-row update; password change compares the hash it read |
| UserServiceImpl.requestPasswordReset / resetPassword | Purge expired, replace this account's link, insert; or check expiry, claim token, update hash; mail after commit |
| InquiryServiceImpl.submit | Lock post, validate buyer/status, create inquiry, interest mail after commit |
| InquiryServiceImpl.accept | Lock post, authorize seller, sell post, accept chosen inquiry, reject competitors, acceptance mail after commit |
| InquiryServiceImpl.reject | Lock post, authorize seller, reject pending inquiry |
| Inbox pages and counts | Read-only; count groups, then two statements per page |

Unique constraints arbitrate account email, artist normalized_name, album artist/LOWER(title)/year, post user/album and one reset token per account. SELECT-before-INSERT does not make those sequences atomic. [[ArtistJdbcDao]] now contains its own race: it inserts inside a savepoint and, on DuplicateKeyException, rolls back to the savepoint and rereads the winner, so the PostgreSQL transaction stays usable. Albums have no such handling; publish and update translate DuplicatePostKeyException specifically and other integrity errors broadly to ConcurrentPublishException. A concurrent reset request is detected by the unique user_id and ends without sending a second link.

PostJdbcDao first issues SELECT id ... FOR UPDATE, then reads the joined summary. Inquiry submission, acceptance, rejection, post editing and post deletion all take this post lock. Conditional updates provide an additional state guard. If accepting an already closed inquiry follows a successful SOLD update, the service exception relies on transaction rollback to restore the post.

User activation uses WHERE enabled=FALSE, a profile password change uses WHERE password_hash = the hash read, and a reset claims its token with a DELETE that must affect one row. Each guard makes the losing concurrent request fail instead of overwriting the winner. Re-registration still does not delete previous pending verification tokens.

## Side effects after commit

[[TransactionCallbacks]] registers a TransactionSynchronization whose afterCommit runs the action; with no active synchronization it runs immediately. Every mail trigger and the matching success log now use it, which closes the earlier gap where an async worker could send mail for a transaction that later rolled back. Delivery itself stays asynchronous and unacknowledged. The mail pool no longer uses CallerRunsPolicy: a saturated pool logs a warning and drops the task, so the request thread is never used for SMTP. [[Mail delivery]] explains the failure handling.

Deleting a post changes other users' data in the same transaction: pending inquiries become REJECTED and every inquiry is detached. Editing a post can rewrite the display name of a shared artist and the title casing and genre of a shared album, visible on other owners' publications.

[[Inquiry and sale flow]] · [[Edit and delete flow]] · [[Password recovery flow]] · [[Database schema]] · [[Testing and evidence]]
