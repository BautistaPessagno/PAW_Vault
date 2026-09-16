---
title: "Known gaps and document drift"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["CONTEXT.md", "README.md", "docs/specs/feature_contacto-post_20260904.md", "docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md", "docs/plans/entrega-intermedia/02-configuracion-y-deploy.md", "docs/plans/entrega-intermedia/03-autenticacion-permisos.md", "docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md", "docs/plans/entrega-intermedia/05-filtros-publicaciones.md"]
---

# Known gaps and document drift

This register describes source at 40328f0. Source documents and their copied commands are reference material, not instructions executed by this vault refresh.

| Claim or assumption | Current evidence and consequence |
|---|---|
| CONTEXT.md says a publisher need not be an account and a vinyl is not a physical copy | Publish uses an authenticated User and Post represents one exemplar; the domain glossary is stale |
| Contact spec requires editable buyer name/email and excludes authentication/sales | ContactForm now contains only an optional message; principal supplies identity and InquiryService supports sale states |
| Contact spec/recovery issue require synchronous Spanish SMTP and 503 retry | EmailServiceImpl is async and catches worker failures; seller locale determines interest mail. The spec also contains a newer async clause that conflicts with its own synchronous sections |
| contactSent or verificationSent proves delivery | Flash/query flags follow normal service return; a later worker can fail |
| Async never blocks the caller | taskExecutor uses CallerRunsPolicy under saturation |
| Plans 04/05 remain draft and must wait for dependencies | Git history at 40328f0 includes the merged sale/filter/authentication work; draft/dependency wording is historical |
| README route list covers every feature | It omits /inquiries and its accept/reject actions, which are implemented |
| Authentication plan says all other routes are public | SecurityConfig also protects /inquiries/** |
| Startup never removes old data | schema.sql retains business rows and legacy album image IDs, but still drops obsolete albums.cover_path; no general legacy migration guarantee follows |
| Canonical and manual schemas have identical guarantees | Old database/albums.sql adds catalog/user FKs/year CHECK absent from canonical startup; current canonical adds image/inquiry/token FKs and post-status CHECK |
| Existing albums ignore new uploaded photos | Superseded: publishing stores a new exemplar image in posts.image_id; album cover is fallback only |
| Invalid MIME bytes must be a valid picture if accepted | ImageService validates declared label/size, not decoding |
| Re-registering invalidates old pending links | Tokens accumulate until activation deletes all for that user; no expiry exists |
| Password maximum checks BCrypt's byte limit | VerifyEmailForm uses character-count @Size, not encoded byte length |
| Accept writes need no rollback | A successful SOLD write followed by a failed pending update must be undone by the transactional exception |
| All invalid search values disappear from the page | Service drops invalid ranges, but controller still renders parsed numeric inputs |
| Sale allows publishing another copy of the same album | User/album uniqueness includes sold posts |
| All check copies are identical | Main tools/paw_checks.py checks i18n/JSP; the .claude/scripts copy still includes Flyway |
| A commit hook proves Maven tests passed | The versioned hook invokes the Python checker only |

The earlier missing app.base-url example and required-property-file conflicts are resolved in README/WebConfig. Authentication, search, price/condition and persisted inquiries are now implemented. No payment, pagination, edit/delete UI, multi-unit stock workflow, token expiry, password reset, outbox or delivery confirmation is present. Admin currently shows an informational page.

## Evidence

[[Authentication flow]] · [[Inquiry and sale flow]] · [[Landing flow]] · [[Transactions and concurrency]] cite the active code. [[History and specifications]] links the historical requirements. [[Database schema]] and [[Configuration and running]] contain exact configuration/schema excerpts. No deployed database, SMTP availability or course-server state was checked.
