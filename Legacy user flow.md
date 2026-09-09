---
title: "Legacy user flow"
categories: ["Flows"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "flows"]
---

# Legacy user flow

The original scaffold remains accessible through public routes, but the landing does not link to it.

| Route | Controller work | View/result |
|---|---|---|
| GET `/create` | Exposes [[UserForm]] as `form` | `helloworld/create` |
| POST `/create` | Validates form, calls [[UserService]].create with Locale | Redirect `/profile/{id}` |
| GET `/profile/{userId}` | Looks up User by ID | `helloworld/index` with `user` |

[[UserServiceImpl]].create inserts an email-normalized row through [[UserJdbcDao]], calls asynchronous welcome mail and returns the User. Unlike publishing's findOrCreate, this always attempts a new insert. Duplicate email exceptions are not mapped to form errors by [[HelloWorldController]]. Missing profile IDs throw [[UserNotFoundException]] with no explicit 404 translation.

The username validation is different from publishing. It requires length 8–100 when non-null and an initial lowercase ASCII letter followed by ASCII letters/digits. It has no NotBlank or NotNull annotation. Email has no Size constraint although the database column is VARCHAR(100).

These JSPs still contain English literals such as Hello, Username and Register. They do not follow the fully localized publishing/contact templates. The profile renders only the escaped username. There is no password field, authentication, editable profile or account permission mechanism.

[[Views and assets]] · [[Validation and errors]] · [[Mail delivery]]
