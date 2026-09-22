---
title: "History and specifications"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["CONTEXT.md", "README.md", "TODO.md", "docs/adr/0001-establish-quiero-vinilos-domain.md", "docs/adr/0002-own-the-album-catalog-locally.md", "docs/issues/01-mostrar-primer-album-en-landing.md", "docs/issues/02-completar-catalogo-inicial.md", "docs/issues/03-terminar-landing-editorial-responsive.md", "docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md", "docs/issues/publicacion-albumes/02-publicar-album-nuevo.md", "docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md", "docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md", "docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md", "docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md", "docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md", "docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md", "docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md", "docs/plans/entrega-intermedia/02-configuracion-y-deploy.md", "docs/plans/entrega-intermedia/03-autenticacion-permisos.md", "docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md", "docs/plans/entrega-intermedia/05-filtros-publicaciones.md", "docs/plans/entrega-intermedia/06-selling-flow.md", "docs/plans/perfil-consultas-ui.md", "docs/setup.md", "docs/specs/feature_cambio-contrasena_20260920.md", "docs/specs/feature_contacto-post_20260904.md", "docs/specs/feature_perfil-consultas-ui_20260921.md", "docs/specs/feature_publicacion-albumes_20260904.md", "docs/specs/landing-quiero-vinilos.md"]
---

# History and specifications

The repository documents several stages of the application. Dates and done/ready labels below come from those files, not a live project board. Source behavior takes precedence for this codemap. Requirements remain requirements even when written in imperative language.

The two ADRs establish the quieroVinilos domain and its locally owned catalog/assets. The earlier landing plan describes an editorial album gallery. Later publication work introduces Artist identity and Posts. The code then represents publishers through User rows, adds accounts, persisted inquiries and single-exemplar sales, and in this range a public detail page, editing, deletion, paging, a profile and password management.

## Document register

| Source | Meaning and current relationship |
|---|---|
| [docs/adr/0001-establish-quiero-vinilos-domain.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/adr/0001-establish-quiero-vinilos-domain.md>) | Decision record. Establish quieroVinilos as the project domain |
| [docs/adr/0002-own-the-album-catalog-locally.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>) | Decision record. Own the album catalog locally |
| [docs/issues/01-mostrar-primer-album-en-landing.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/01-mostrar-primer-album-en-landing.md>) | 01: Mostrar el primer álbum real en `/`. **Status:** done — implementada y verificada en el browser contra localhost. El diseño editorial queda para la issue 03. |
| [docs/issues/02-completar-catalogo-inicial.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/02-completar-catalogo-inicial.md>) | 02: Completar el catálogo inicial de ocho álbumes. **Status:** ready-for-agent |
| [docs/issues/03-terminar-landing-editorial-responsive.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/03-terminar-landing-editorial-responsive.md>) | 03: Terminar la landing editorial responsive. **Status:** ready-for-agent |
| [docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md>) | 01: Convertir Artist en entidad sin romper el catálogo. **Status:** done — implementada en `08a5de1` y verificada por el usuario contra PostgreSQL y la landing. |
| [docs/issues/publicacion-albumes/02-publicar-album-nuevo.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/02-publicar-album-nuevo.md>) | 02: Publicar un álbum nuevo desde /publish. **Status:** done — implementada en `fe32671` y `30251a2`, y verificada por el usuario en localhost. |
| [docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md>) | 03: Reutilizar artistas y álbumes entre publicaciones. **Status:** done |
| [docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md>) | 04: Rechazar Posts duplicados dentro del formulario. **Status:** done |
| [docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md>) | 01: Contactar al publicante desde un Post. **Status:** done |
| [docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md>) | 02: Recuperarse de un fallo de entrega de contacto. **Status:** ready-for-agent |
| [docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md>) | 01: Seguimiento de consultas por publicación. **Status:** implemented; pending end-to-end manual test. Groups inquiries by publication and sends the buyer to the inbox after contacting. |
| [docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md>) | 02: Confirmar la venta de un ejemplar único. **Status:** implemented; pending end-to-end manual test. In-page confirmation before accept. |
| [docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md>) | 03: Avisar al comprador cuya consulta fue aceptada. **Status:** implemented; pending end-to-end manual test. Acceptance email and inquiries call to action. |
| [docs/plans/entrega-intermedia/02-configuracion-y-deploy.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/02-configuracion-y-deploy.md>) | Configuration and deploy plan; now also describes the `pampero` Maven profile and `mvn clean package -Ppampero`. The first Pampero deploy is still listed as a pending step. |
| [docs/plans/entrega-intermedia/03-autenticacion-permisos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/03-autenticacion-permisos.md>) | Authentication and permissions plan; implemented before 40328f0. Its route list predates the profile, edit/delete and recovery routes. |
| [docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md>) | Single-exemplar sale plan; now states it was integrated into main by PR #20 and points to 06-selling-flow.md for the inbox, confirmation and acceptance email increment. |
| [docs/plans/entrega-intermedia/05-filtros-publicaciones.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/05-filtros-publicaciones.md>) | Combined filters plan; implemented before 40328f0. It does not cover the later pagination or the removal of the artist filter control. |
| [docs/plans/entrega-intermedia/06-selling-flow.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/06-selling-flow.md>) | Selling-flow plan dated 2026-09-17, marked implemented and pending a manual end-to-end walk-through; merged as PR #25. |
| [docs/plans/perfil-consultas-ui.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/perfil-consultas-ui.md>) | Task-by-task agent plan for the profile, inbox and detail redesign (inline account rows, inbox paginated by post, icons, state markers, notices). Implemented through PR #34; its checkboxes are plan text, not evidence. |
| [docs/setup.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/setup.md>) | Setup now documents Pampero properties and the profile build, and says the local setup script applies the canonical schema and the separate seed script loads demo data. Dependency-centralization claims still differ from the POMs. |
| [docs/specs/feature_cambio-contrasena_20260920.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_cambio-contrasena_20260920.md>) | Password change specification. Still labelled lista para implementar although implemented by PR #30 (ddff7ec). |
| [docs/specs/feature_contacto-post_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) | Now marked historical and implemented from the public detail page. It says POST contact redirects to /inquiries, while the code redirects to /inquiries/sent. Older synchronous-delivery sections remain in the body. |
| [docs/specs/feature_perfil-consultas-ui_20260921.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_perfil-consultas-ui_20260921.md>) | Profile, inbox and detail redesign specification. Still labelled lista para implementar although implemented by PR #34. |
| [docs/specs/feature_publicacion-albumes_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>) | Updated to User-linked Posts, multipart publishing, optional Image storage and PostSummary. Some old no-Post-list and constraint assumptions remain; see [[Known gaps and document drift]]. |
| [docs/specs/landing-quiero-vinilos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>) | Now acknowledges PostDao and deleted scaffold routes; old no-action/gallery criteria remain in the body. |

## Changes through f12af08

The range from `40328f0` to `f12af08` has 101 commits and changes 168 paths. The merged pull requests, in order:

| PR | Date | Branch | Result in code |
|---|---|---|---|
| #23 | 2026-09-16 | e-tormakh/boton-volver | Back navigation on views without an exit (later reworked into ui:back-link and Cancel buttons) |
| #25 | 2026-09-19 | feature/selling-flow, stacked on redesign-header-filtros | Merged first and brought the #24 commits with it, plus the inbox split into received and sent grouped by post, sale confirmation dialog, acceptance email, mail after commit, non-blocking mail pool, logo and auth screens, and the Pampero profile |
| #24 | 2026-09-19 | redesign-header-filtros | Compact header with global search, filter sidebar, public post detail, case-preserving titles and artists, cookie-only sessions; its own merge added the shared password validator refactor |
| — | 2026-09-19 to 20 | Local merges of catalog, profile and pagination branches | Normalized artists and suggestions, required genre/condition/positive price with backfills, post editing with preview, first profile panel, catalog and profile pagination, demo catalog seed |
| #30 | 2026-09-21 | b-pessagno/cambio-contrasena | Password change from the profile with logout and notice email; shared password validators |
| #29, #32 | 2026-09-21 to 22 | b-pessagno/ui-fixes | Icons, unified badges and confirmation dialog, compact cards, suggestion query in one statement |
| #31 | 2026-09-21 | l-mendez/delete-own-posts | Owner deletion with detached inquiries and own-image removal |
| #34 | 2026-09-22 | l-mendez/rework-profile-page-navigation | One-column profile with inline editing, numbered profile pagination, inbox as a flat list paginated by post, state markers, publish/edit notices |
| #33 | 2026-09-22 | feature/password-reset | Forgot/reset password with one-hour single-use links |

Source behavior is traced in [[Post detail flow]], [[Edit and delete flow]], [[Profile flow]], [[Password recovery flow]], [[Search suggestions flow]] and the updated older flows. [[Paginated listings]] summarizes the three paged views.

The specifications written for password change and the profile redesign still say they are ready to implement, and the selling-flow issues still wait for a manual end-to-end test. README now lists every current route, credentials, the Pampero build and the demo seed; its /inquiries row describes both inbox halves although that route shows received inquiries only. CONTEXT.md gained the Cuenta and password vocabulary but still says recovery does not exist. TODO.md keeps its 09/09 heading and blockers alongside new known-debt entries about sessions and post deletion. These are recorded in [[Known gaps and document drift]].

## Changes through 40328f0

The earlier merge added authenticated accounts with email verification, persistent inquiries and seller actions, single-exemplar sale states, per-post photos, commercial details and combined catalog search/filter/sort. The plans under docs/plans/entrega-intermedia describe that work; their draft/dependency labels are historical.

The removed [[AlbumSummary]], [[HelloWorldController]], [[UserForm]], [[Legacy UserNotFoundException]] and [[EmailDeliveryException]] preserve their pinned historical code. The newer [[UserNotFoundException]] belongs to services-contracts and is a separate class.

[[Known gaps and document drift]] · [[Verification record]]
