---
title: "Validation and errors"
categories: ["Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/VerifyEmailForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java"]
---

# Validation and errors

Spring binds form values before Bean Validation. Controllers with BindingResult redisplay field and global errors. Security filters authenticate and validate CSRF before the protected controller action. Publish, edit and contact identity come from the principal.

| Input | Source rules |
|---|---|
| Publish/edit title and artist | Required, at most 255 characters |
| Release year / optional pressing year | Integer 1000–9999 |
| Genre, condition | Required enum values (new in this range) |
| Price | Required integer 1–99,999,999 |
| Optional zone / description | At most 100 / 1000 characters |
| Optional contact message | CRLF normalized to LF and trimmed; at most 500 characters |
| Registration / recovery email | Trimmed, required, email format, at most 100 characters |
| Verification | Nonblank token and username up to 100; password rules below |
| Profile username | Required, at most 100; trimmed by the service |
| Passwords (verify, reset, change) | [[ValidPassword]]: required, 12–72 characters, an ASCII letter and a digit; [[MatchingPasswords]] reports a mismatch on the confirmation field |
| Current password (change) | Required; checked against the stored hash by the service |
| Cover | Optional; allowed MIME label and at most 5 MiB; whole request at most 6 MiB |
| Search | Query over 255 gives 400; malformed/out-of-range filters ignored; invalid page gives 404 |

The three password forms implement [[PasswordsMatching]], so one class-level validator serves them. Publish strings are not trimmed before annotation checks, while contact, email and verification username have binder normalization. Passwords are not trimmed, and @Size is a character count rather than a UTF-8 byte count. Service APIs rely on the controller for most form constraints.

| Error | HTTP or form result |
|---|---|
| InvalidImageException | Cover field error on publish or edit |
| DuplicatePostException / ConcurrentPublishException | Global publish or edit error |
| DuplicateUserException | Registration email error |
| Invalid/reused verification token | Global verification error |
| Invalid/expired/used reset token | Global reset error with a link to request another |
| InvalidCurrentPasswordException | currentPassword field error |
| UnchangedPasswordException | password field error on profile or reset |
| Multipart overflow | Redirect to /publish?coverTooLarge or /post/{id}/edit?coverTooLarge |
| Missing post/inquiry/image/account, PageNotFoundException | 404 |
| Self-contact, wrong seller, foreign post edit/delete, route denial | 403 |
| Sold contact, sold post edit/delete, invalid inquiry transition, deleted-post inquiry | 409 |
| InvalidSearchQueryException | 400 |
| Rendering/SMTP exception inside mail worker | Log and swallow |

ErrorController handles explicit 403/404 pages; web.xml forwards unmatched-route 404. Controllers select 400/403/404/409 JSPs for their own handlers. IOException while reading an upload still has no dedicated local mapping. Form inputs use escaped values, and password fields are never repopulated by ui:text-input.

[[Authentication flow]] · [[Profile flow]] · [[Password recovery flow]] · [[UI components]] · [[Known gaps and document drift]]
