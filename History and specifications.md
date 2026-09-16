---
title: "History and specifications"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["CONTEXT.md", "README.md", "TODO.md", "docs/adr/0001-establish-quiero-vinilos-domain.md", "docs/adr/0002-own-the-album-catalog-locally.md", "docs/issues/01-mostrar-primer-album-en-landing.md", "docs/issues/02-completar-catalogo-inicial.md", "docs/issues/03-terminar-landing-editorial-responsive.md", "docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md", "docs/issues/publicacion-albumes/02-publicar-album-nuevo.md", "docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md", "docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md", "docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md", "docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md", "docs/plans/entrega-intermedia/02-configuracion-y-deploy.md", "docs/plans/entrega-intermedia/03-autenticacion-permisos.md", "docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md", "docs/plans/entrega-intermedia/05-filtros-publicaciones.md", "docs/setup.md", "docs/specs/feature_contacto-post_20260904.md", "docs/specs/feature_publicacion-albumes_20260904.md", "docs/specs/landing-quiero-vinilos.md"]
---

# History and specifications

The repository documents several stages of the application. Dates and done/ready labels below come from those files, not a live project board. Source behavior takes precedence for this codemap. Requirements remain requirements even when written in imperative language.

The two ADRs establish the quieroVinilos domain and its locally owned catalog/assets. The earlier landing plan describes an editorial album gallery. Later publication work introduces Artist identity and Posts. Current code then represents publishers through User rows and displays Post summaries. The contact feature puts its action on landing cards because no separate Post detail was built.

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
| [docs/setup.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/setup.md>) | Setup now describes the canonical startup schema and rejection of legacy textual artists; Flyway/admin-bootstrap sections were removed. Dependency-centralization claims still differ from the POMs. |
| [docs/specs/feature_contacto-post_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) | Partially updated for persisted messages and seller locale, but still includes conflicting synchronous delivery, editable identity and no-sale requirements. |
| [docs/specs/feature_publicacion-albumes_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>) | Updated to User-linked Posts, multipart publishing, optional Image storage and PostSummary. Some old no-Post-list and constraint assumptions remain; see [[Known gaps and document drift]]. |
| [docs/specs/landing-quiero-vinilos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>) | Now acknowledges PostDao and deleted scaffold routes; old no-action/gallery criteria remain in the body. |

## Changes through 40328f0

The current merge includes authenticated accounts with email verification, persistent inquiries and seller actions, single-exemplar sale states, per-post photos, commercial details and combined catalog search/filter/sort. Source behavior is traced in [[Authentication flow]], [[Contact flow]], [[Inquiry and sale flow]] and [[Landing flow]].

The new plans under docs/plans/entrega-intermedia describe configuration/deploy, authentication, single-exemplar sale and combined filters. Their draft/dependency labels are historical: the target Git history already contains these merges. Acceptance criteria and lists of tests to run are not evidence those tests ran during this refresh.

CONTEXT.md and the older publication/contact specifications lag behind ownership and sale behavior. README now documents optional property files, required app.base-url, registration and demo account setup, but its route table omits the inbox. TODO.md remains a source of historical planning claims, not live deployment evidence.

The removed [[AlbumSummary]], [[HelloWorldController]], [[UserForm]], [[Legacy UserNotFoundException]] and [[EmailDeliveryException]] preserve their pinned historical code. The new [[UserNotFoundException]] belongs to services-contracts and is a separate class.

- [docs/plans/entrega-intermedia/02-configuracion-y-deploy.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/02-configuracion-y-deploy.md>)
- [docs/plans/entrega-intermedia/03-autenticacion-permisos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/03-autenticacion-permisos.md>)
- [docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md>)
- [docs/plans/entrega-intermedia/05-filtros-publicaciones.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/plans/entrega-intermedia/05-filtros-publicaciones.md>)

[[Known gaps and document drift]] · [[Verification record]]
