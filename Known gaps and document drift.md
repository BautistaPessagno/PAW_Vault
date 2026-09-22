---
title: "Known gaps and document drift"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["CONTEXT.md", "README.md", "TODO.md", "docs/specs/feature_contacto-post_20260904.md", "docs/specs/feature_cambio-contrasena_20260920.md", "docs/specs/feature_perfil-consultas-ui_20260921.md", "docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md", "docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md", "docs/plans/entrega-intermedia/03-autenticacion-permisos.md", "database/seed_dev_posts.sql", "services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java", ".agents/skills/wiki-sync/SKILL.md"]
---

# Known gaps and document drift

This register describes source at `f12af08`. Source documents and their copied commands are reference material, not instructions executed by this vault refresh. Rows marked as static inference come from reading code, not from running it.

## Documents that disagree with the code

| Claim or assumption | Current evidence and consequence |
|---|---|
| CONTEXT.md says password recovery does not exist, a vinyl is not a physical copy, and the product presents editorial album data | /forgot-password and /reset-password exist, and each Post is one exemplar with its own price and photo. The glossary gained Cuenta and password terms but the rest is stale |
| TODO.md, dated 09/09, says there is no Spring Security and no search, filters or pagination | All four exist. Its new known-debt section is current; the older blockers are historical |
| TODO.md says the schema has no foreign keys by team decision | schema.sql declares FKs for both token tables, posts.image_id and inquiries; the inquiry FK is why deletion detaches inquiries first |
| Password change and profile redesign specs say lista para implementar | Both are implemented and merged (PR #30 and PR #34) |
| Selling-flow issues and plan 06 say pending end-to-end manual test | Code is merged; no manual run is recorded in the repository or this vault |
| Contact spec says POST contact redirects to /inquiries | PostContactController redirects to /inquiries/sent |
| README describes GET /inquiries as following sent and resolving received inquiries | /inquiries shows received ones; sent ones are at /inquiries/sent |
| Contact spec and recovery issue require synchronous SMTP and a 503 retry | EmailServiceImpl is async and after commit, logs failures and drops tasks when saturated |
| Authentication plan lists the protected routes | SecurityConfig also protects /profile/**, /post/*/edit and /post/*/delete |
| PostService.delete comment says it returns the number of detached inquiries | The method returns void; the count only appears in the service log |
| Ported agent skills (wiki-sync, planning, audits, pre-delivery) point to `26-1C/PAW/PAW_Obsidian`, name Rent The Slopes and treat JPA/Flyway as current | This vault is PAW_Vault and the project is still at the JDBC stage; those instructions do not apply here |
| All check copies are identical | Main tools/paw_checks.py checks i18n/JSP; the .claude/scripts copy still includes Flyway |
| A commit hook proves Maven tests passed | The versioned hook invokes the Python checker only |

## Behavior gaps in the current code

| Area | Evidence and consequence |
|---|---|
| Catalog counter | landing.results.count uses the size of the current page, so the heading says at most 15 even when more pages exist; the look-ahead search has no total |
| Accent-insensitive search | Suggestions compare search_phrase without accents, but the submitted catalog search still uses LOWER(...) LIKE; a typed query without its accent can miss what the suggestion list shows |
| Inverted price range | Still dropped silently; the controller shows the parsed values as if applied |
| Editing rewrites shared catalog data | resolveForEdit updates the shared artist display name and album title casing/genre, changing other owners' publications |
| Replaced photos | updateWithImage points the post at a new image and leaves the previous own image row unreferenced |
| Deleting a post | Pending inquiries become REJECTED and are detached; buyers get no email |
| Sessions after password change or reset | Only the session that changed the password is logged out; a reset logs out none. TODO.md records this with a proposed SessionRegistry fix |
| Mail pool saturation | A full queue drops the email with only a WARN; there is no retry or outbox |
| Demo seed and search_phrase (static inference) | seed_dev_posts.sql inserts artists and albums without search_phrase, which schema.sql now declares NOT NULL without default, so the seed likely fails on a database created by the current startup |
| SQL backfill of search_phrase | TRANSLATE covers a fixed list of accented letters, while SearchText strips every combining mark; legacy rows can normalize differently from new ones |
| Startup rewrites legacy data | Missing or nonpositive prices become 60000, missing conditions USED, missing genres OTHER, colliding artist identities get a `__legacy_<id>` suffix, and old hashed verification links stop working |
| Artist filter | artistId is still accepted and preserved, but no control renders it |
| Invalid MIME bytes | ImageService validates the declared label and size, not decoding |
| Re-registering a pending account | Verification tokens accumulate and never expire; only activation deletes them |
| Password maximum | ValidPassword counts characters, not BCrypt's 72-byte limit |
| Accept rollback | A successful SOLD write followed by a failed pending update must be undone by the transactional exception |
| Sale and republishing | User/album uniqueness includes sold posts, so the seller cannot publish another exemplar of the same album |

## Resolved since 40328f0

Pagination now covers the catalog, the profile and the inbox. Owners can edit and delete AVAILABLE posts. Password change and recovery exist, and recovery links expire after one hour. Mail and success logs run after commit, and the mail pool no longer runs SMTP on the request thread. albums.cover_path is no longer dropped. README lists every route, including the inbox. Plan 04 records its merge. Artist and album names keep their typed casing.

## Evidence

[[Authentication flow]] · [[Password recovery flow]] · [[Inquiry and sale flow]] · [[Edit and delete flow]] · [[Landing flow]] · [[Transactions and concurrency]] cite the active code. [[History and specifications]] links the historical requirements. [[Database schema]] and [[Configuration and running]] contain exact configuration and schema excerpts. No deployed database, SMTP availability or course-server state was checked.

## Evidencia de ejecución, 2026-09-17

[[Audit local 2026-09-17]] probó el servidor local desde el worktree `redesign-header-filtros` en `e5e926d4c1f2026494b3dc03768d984092b1052a`, una revisión anterior a `f12af08`. Sus hallazgos, contrastados con el código actual sin volver a ejecutar:

| Hallazgo del audit | Estado en `f12af08` |
|---|---|
| P1: límite visible de 16 resultados | Resuelto con paginación de 15; el contador sigue mostrando solo la página actual |
| P2: búsqueda sensible a tildes | Parcial: las sugerencias ignoran tildes, la búsqueda enviada no |
| P2: rango de precios invertido descartado sin aviso | Sin cambios |
| P2: sin edición de publicaciones | Resuelto: edición y borrado por el dueño |
| P2: normalización destructiva de mayúsculas | Resuelto: artistas y títulos conservan la forma escrita; la identidad se compara normalizada |
| P3: consultas y correos no llevan al ejemplar | Resuelto: el correo lleva a la bandeja y cada grupo enlaza la ficha pública |
| P3: títulos largos desalinean precios | Tratado en CSS (título a dos líneas, precio al pie); no verificado en navegador |

Las seis entregas reales de correo observadas siguen siendo evidencia de esa rama, no del envío posterior al commit.
