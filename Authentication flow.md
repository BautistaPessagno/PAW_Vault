---
title: "Authentication flow"
categories: ["Flows", "Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java"]
---

# Authentication flow

Registration starts with email only. POST /register validates and normalizes the address, creates a disabled USER account or reuses a pending one, stores a random token and requests verification mail. An enabled account with that email receives a field error. The success redirect is /login?verificationSent, which does not prove SMTP delivery.

GET /verify?token= displays a form without changing the account. POST /verify requires CSRF, a token, username and confirmed password. [[UserServiceImpl]] looks up the token, hashes the password through [[PasswordHasher]] and conditionally activates the disabled account. It deletes all that user's tokens and requests welcome mail. Invalid/reused tokens leave the form with an error; success redirects to /login?verified.

[[EmailVerificationToken]] has no expiry. Registering a pending account again adds a link without invalidating its earlier links. Activation changes credentials only while enabled=false, so a competing activation cannot overwrite the chosen credentials. An old account with no hash can claim its existing publications through this same email flow.

[[SecurityConfig]] handles POST /login using email/password and BCrypt strength 12. [[AuthenticatedUserDetailsService]] rejects missing accounts and accounts with no hash; UserDetails supplies enabled. A saved protected request can be restored after login. POST /logout invalidates the session and deletes JSESSIONID. The servlet descriptor marks the cookie HttpOnly.

| Route | Access |
|---|---|
| /, /covers/{id}, /register, /verify, /login | Public |
| /publish/**, /post/*/contact, /inquiries/** | Authenticated |
| /admin/** | ADMIN |

ADMIN receives both common and administrative authorities. The current admin page is informational. Anonymous requests to protected pages go to login; authenticated access denial renders 403. CSRF remains enabled for state-changing requests, including anonymous registration and verification.

[[Publish flow]] · [[Contact flow]] · [[Inquiry and sale flow]] · [[Mail delivery]]
