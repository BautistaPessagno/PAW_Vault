---
title: "History and specifications"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "history"]
sources: ["docs/adr/0001-establish-quiero-vinilos-domain.md", "docs/adr/0002-own-the-album-catalog-locally.md", "docs/issues/01-mostrar-primer-album-en-landing.md", "docs/issues/02-completar-catalogo-inicial.md", "docs/issues/03-terminar-landing-editorial-responsive.md", "docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md", "docs/issues/publicacion-albumes/02-publicar-album-nuevo.md", "docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md", "docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md", "docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md", "docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md", "docs/setup.md", "docs/specs/feature_contacto-post_20260904.md", "docs/specs/feature_publicacion-albumes_20260904.md", "docs/specs/landing-quiero-vinilos.md", "TODO.md"]
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
| [docs/specs/feature_contacto-post_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) | Historical requested behavior. Feature Specification: Contacto con publicante por Post. Compare with current flow notes and document-drift register. |
| [docs/specs/feature_publicacion-albumes_20260904.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>) | Updated to User-linked Posts, multipart publishing, optional Image storage and PostSummary. Some old no-Post-list and constraint assumptions remain; see [[Known gaps and document drift]]. |
| [docs/specs/landing-quiero-vinilos.md](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>) | Now acknowledges PostDao and deleted scaffold routes; old no-action/gallery criteria remain in the body. |

## Changes through ff96f27

The merge includes optional cover storage and retrieval, WAR/log naming changes, asynchronous localized interest mail with home CTA, and cleanup of the scaffold and unused album listing. [[AlbumSummary]], [[HelloWorldController]], [[UserForm]], [[UserNotFoundException]] and [[EmailDeliveryException]] remain as historical notes with pinned pre-removal excerpts.

TODO.md now marks image handling covered and says database access/upload procedure are known, while the first course deployment remains pending validation. Its admin-bootstrap discussion is future design guidance, not an implemented listener, role or authenticated session.

The contact specification and recovery issue still require synchronous Spanish delivery, HTTP 503 and retained form input. Those requirements conflict with the new async source and deleted recovery path. Their done/ready labels and test-coverage claims are historical document assertions, not current runtime evidence.

No document instructions were executed. [[Known gaps and document drift]] records the remaining contradictions; [[Verification record]] records only checks performed for this vault refresh.
