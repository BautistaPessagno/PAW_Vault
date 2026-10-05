@title: Source inventory
@categories: Navigation
@type: index
@tags: codemap, navigation

> [!summary] En una frase
> Registro de los 472 archivos versionados en `c3e2a4c`: dónde está cada uno, qué nota del vault lo explica y en qué etapa del [[Roadmap de lectura]] se lee.

Se genera a partir de `git ls-tree`; el generador falla si un archivo no tiene nota asignada. Las 238 clases Java tienen una nota propia con su código completo. Los demás archivos se explican en una nota temática, que en muchos casos también embebe su contenido.

No se incluyen archivos ignorados (propiedades con credenciales, compilados) ni el estado interno de Git.

## Resumen

| Grupo | Archivos |
|---|---|
| (raíz) | 8 |
| .agents | 23 |
| .claude | 27 |
| .codex | 18 |
| database | 3 |
| docs | 33 |
| models | 4 |
| models · Java | 57 |
| persistence | 15 |
| persistence · Java | 13 |
| persistence · Java de test | 14 |
| persistence-contracts | 3 |
| persistence-contracts · Java | 14 |
| services | 10 |
| services · Java | 15 |
| services · Java de test | 16 |
| services-contracts | 3 |
| services-contracts · Java | 43 |
| tools | 5 |
| webapp | 82 |
| webapp · Java | 66 |
| **Total** | **472** |

## (raíz)

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [.gitignore](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.gitignore>) | [[Repository tooling]] · [[Configuration and running]] | 1 |
| [.worktreeinclude](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.worktreeinclude>) | [[Repository tooling]] | 1 |
| [AGENTS.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/AGENTS.md>) | [[Repository tooling]] | 0 |
| [CLAUDE.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/CLAUDE.md>) | [[Repository tooling]] | 0 |
| [CONTEXT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/CONTEXT.md>) | [[Domain and identity]] · [[History and specifications]] | 0 |
| [README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/README.md>) | [[Configuration and running]] · [[Known gaps and document drift]] | 0 |
| [TODO.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/TODO.md>) | [[History and specifications]] · [[Known gaps and document drift]] | 0 |
| [pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/pom.xml>) | [[Build and dependencies]] | 1 |

## .agents

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [.agents/skills/PROJECT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/PROJECT.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/README.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/bug/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/bug/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/corrector-eyes/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/corrector-eyes/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/design/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/design/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/enhancer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/enhancer/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/feature-engineering/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/feature-engineering/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/feature-engineering/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/feature-engineering/context.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/forensic-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/forensic-audit/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/frontend-analyzer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/frontend-analyzer/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/context.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/frontend-analyzer/scripts/research.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/scripts/research.py>) | [[Repository tooling]] | 15 |
| [.agents/skills/general-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/general-audit/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/good-practice/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/good-practice/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/handoff/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/handoff/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/i18n-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/i18n-sync/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/implementation/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/implementation/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/jdbc-to-jpa/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/jdbc-to-jpa/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/planning/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/planning/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/pre-delivery/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/pre-delivery/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/skillset-port/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/skillset-port/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/smoke/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/smoke/SKILL.md>) | [[Repository tooling]] | 15 |
| [.agents/skills/wiki-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/wiki-sync/SKILL.md>) | [[Repository tooling]] | 15 |

## .claude

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [.claude/hooks/commit-gate.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/commit-gate.py>) | [[Repository tooling]] | 15 |
| [.claude/hooks/db-server-guard.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/db-server-guard.py>) | [[Repository tooling]] | 15 |
| [.claude/hooks/i18n-parity-posttool.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/i18n-parity-posttool.py>) | [[Repository tooling]] | 15 |
| [.claude/hooks/skill-autolaunch.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/skill-autolaunch.py>) | [[Repository tooling]] | 15 |
| [.claude/skills/PROJECT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/PROJECT.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/README.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/bug/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/bug/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/corrector-eyes/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/corrector-eyes/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/design/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/design/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/enhancer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/enhancer/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/feature-engineering/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/feature-engineering/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/feature-engineering/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/feature-engineering/context.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/forensic-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/forensic-audit/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/frontend-analyzer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/frontend-analyzer/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/context.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/frontend-analyzer/scripts/research.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/scripts/research.py>) | [[Repository tooling]] | 15 |
| [.claude/skills/general-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/general-audit/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/good-practice/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/good-practice/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/handoff/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/handoff/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/i18n-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/i18n-sync/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/implementation/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/implementation/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/jdbc-to-jpa/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/jdbc-to-jpa/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/planning/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/planning/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/pre-delivery/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/pre-delivery/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/skillset-port/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/skillset-port/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/smoke/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/smoke/SKILL.md>) | [[Repository tooling]] | 15 |
| [.claude/skills/wiki-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/wiki-sync/SKILL.md>) | [[Repository tooling]] | 15 |

## .codex

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [.codex/prompts/bug.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/bug.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/corrector-eyes.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/corrector-eyes.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/design.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/design.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/enhancer.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/enhancer.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/feature-engineering.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/feature-engineering.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/forensic-audit.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/forensic-audit.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/frontend-analyzer.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/frontend-analyzer.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/general-audit.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/general-audit.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/good-practice.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/good-practice.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/handoff.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/handoff.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/i18n-sync.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/i18n-sync.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/implementation.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/implementation.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/jdbc-to-jpa.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/jdbc-to-jpa.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/planning.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/planning.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/pre-delivery.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/pre-delivery.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/skillset-port.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/skillset-port.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/smoke.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/smoke.md>) | [[Repository tooling]] | 15 |
| [.codex/prompts/wiki-sync.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/wiki-sync.md>) | [[Repository tooling]] | 15 |

## database

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [database/demo_posts.tsv](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/demo_posts.tsv>) | [[Schema history and seeds]] | 2 |
| [database/seed_dev_posts.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/seed_dev_posts.sql>) | [[Schema history and seeds]] | 2 |
| [database/users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/users.sql>) | [[Schema history and seeds]] | 2 |

## docs

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [docs/adr/0001-establish-quiero-vinilos-domain.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0001-establish-quiero-vinilos-domain.md>) | [[History and specifications]] | 0 |
| [docs/adr/0002-own-the-album-catalog-locally.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>) | [[History and specifications]] | 0 |
| [docs/adr/0003-conversation-inside-the-inquiry.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0003-conversation-inside-the-inquiry.md>) | [[History and specifications]] | 0 |
| [docs/adr/0004-freeze-sale-price-at-acceptance.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0004-freeze-sale-price-at-acceptance.md>) | [[History and specifications]] | 0 |
| [docs/issues/01-mostrar-primer-album-en-landing.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/01-mostrar-primer-album-en-landing.md>) | [[History and specifications]] | 16 |
| [docs/issues/02-completar-catalogo-inicial.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/02-completar-catalogo-inicial.md>) | [[History and specifications]] | 16 |
| [docs/issues/03-terminar-landing-editorial-responsive.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/03-terminar-landing-editorial-responsive.md>) | [[History and specifications]] | 16 |
| [docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md>) | [[History and specifications]] | 16 |
| [docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-albumes/02-publicar-album-nuevo.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/02-publicar-album-nuevo.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md>) | [[History and specifications]] | 16 |
| [docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md>) | [[History and specifications]] | 16 |
| [docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md>) | [[History and specifications]] | 16 |
| [docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md>) | [[History and specifications]] | 16 |
| [docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md>) | [[History and specifications]] | 16 |
| [docs/plans/carrito-consultas.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/carrito-consultas.md>) | [[History and specifications]] | 16 |
| [docs/plans/entrega-intermedia/02-configuracion-y-deploy.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/02-configuracion-y-deploy.md>) | [[History and specifications]] | 16 |
| [docs/plans/entrega-intermedia/03-autenticacion-permisos.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/03-autenticacion-permisos.md>) | [[History and specifications]] | 16 |
| [docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md>) | [[History and specifications]] | 16 |
| [docs/plans/entrega-intermedia/05-filtros-publicaciones.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/05-filtros-publicaciones.md>) | [[History and specifications]] | 16 |
| [docs/plans/entrega-intermedia/06-selling-flow.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/06-selling-flow.md>) | [[History and specifications]] | 16 |
| [docs/plans/perfil-consultas-ui.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/perfil-consultas-ui.md>) | [[History and specifications]] | 16 |
| [docs/plans/venta-con-comprobante.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/venta-con-comprobante.md>) | [[History and specifications]] | 16 |
| [docs/setup.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/setup.md>) | [[Build and dependencies]] · [[Configuration and running]] | 0 |
| [docs/specs/feature_cambio-contrasena_20260920.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_cambio-contrasena_20260920.md>) | [[History and specifications]] | 16 |
| [docs/specs/feature_contacto-post_20260904.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>) | [[History and specifications]] | 16 |
| [docs/specs/feature_perfil-consultas-ui_20260921.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_perfil-consultas-ui_20260921.md>) | [[History and specifications]] | 16 |
| [docs/specs/feature_publicacion-albumes_20260904.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>) | [[History and specifications]] | 16 |
| [docs/specs/feature_venta-con-comprobante_20260924.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_venta-con-comprobante_20260924.md>) | [[History and specifications]] | 16 |
| [docs/specs/landing-quiero-vinilos.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>) | [[History and specifications]] | 16 |

## models

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [models/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [models/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [models/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/pom.xml>) | [[Build and dependencies]] | 1 |
| [models/src/main/resources/.gitkeep](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/resources/.gitkeep>) | [[Build and dependencies]] | 1 |

## models · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [models/Address.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Address.java>) | [[Address]] | 3 |
| [models/Album.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Album.java>) | [[Album]] | 3 |
| [models/Artist.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Artist.java>) | [[Artist]] | 3 |
| [models/Cart.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Cart.java>) | [[Cart]] | 3 |
| [models/CartCheckout.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartCheckout.java>) | [[CartCheckout]] | 3 |
| [models/CartCheckoutResult.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartCheckoutResult.java>) | [[CartCheckoutResult]] | 3 |
| [models/CartItem.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartItem.java>) | [[CartItem]] | 3 |
| [models/CartSellerGroup.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/CartSellerGroup.java>) | [[CartSellerGroup]] | 3 |
| [models/Condition.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Condition.java>) | [[Condition]] | 3 |
| [models/ContactState.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ContactState.java>) | [[ContactState]] | 3 |
| [models/EmailRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailRules.java>) | [[EmailRules]] | 3 |
| [models/EmailVerificationToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java>) | [[EmailVerificationToken]] | 3 |
| [models/FilterCounts.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/FilterCounts.java>) | [[FilterCounts]] | 3 |
| [models/Genre.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Genre.java>) | [[Genre]] | 3 |
| [models/Image.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>) | [[Image]] | 3 |
| [models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>) | [[ImageRules]] | 3 |
| [models/ImageUpload.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageUpload.java>) | [[ImageUpload]] | 3 |
| [models/Inquiry.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Inquiry.java>) | [[Inquiry]] | 3 |
| [models/InquiryDetail.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryDetail.java>) | [[InquiryDetail]] | 3 |
| [models/InquiryGroup.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryGroup.java>) | [[InquiryGroup]] | 3 |
| [models/InquiryPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java>) | [[InquiryPage]] | 3 |
| [models/InquiryParties.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryParties.java>) | [[InquiryParties]] | 3 |
| [models/InquiryStatus.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryStatus.java>) | [[InquiryStatus]] | 3 |
| [models/InquiryStatusFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquiryStatusFilter.java>) | [[InquiryStatusFilter]] | 3 |
| [models/InquirySummary.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/InquirySummary.java>) | [[InquirySummary]] | 3 |
| [models/Message.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Message.java>) | [[Message]] | 3 |
| [models/MessageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/MessageRules.java>) | [[MessageRules]] | 3 |
| [models/PasswordResetToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java>) | [[PasswordResetToken]] | 3 |
| [models/PaymentInfo.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PaymentInfo.java>) | [[PaymentInfo]] | 3 |
| [models/PaymentInfoRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PaymentInfoRules.java>) | [[PaymentInfoRules]] | 3 |
| [models/Post.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>) | [[Post]] | 3 |
| [models/PostContactOptions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostContactOptions.java>) | [[PostContactOptions]] | 3 |
| [models/PostDetail.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostDetail.java>) | [[PostDetail]] | 3 |
| [models/PostPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostPage.java>) | [[PostPage]] | 3 |
| [models/PostSearchCriteria.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java>) | [[PostSearchCriteria]] | 3 |
| [models/PostSort.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSort.java>) | [[PostSort]] | 3 |
| [models/PostStatus.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostStatus.java>) | [[PostStatus]] | 3 |
| [models/PostSummary.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSummary.java>) | [[PostSummary]] | 3 |
| [models/PostView.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostView.java>) | [[PostView]] | 3 |
| [models/Province.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Province.java>) | [[Province]] | 3 |
| [models/PublicProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java>) | [[PublicProfile]] | 3 |
| [models/PublicUserProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java>) | [[PublicUserProfile]] | 3 |
| [models/Receipt.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Receipt.java>) | [[Receipt]] | 3 |
| [models/ReceiptRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java>) | [[ReceiptRules]] | 3 |
| [models/Review.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Review.java>) | [[Review]] | 3 |
| [models/ReviewPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewPage.java>) | [[ReviewPage]] | 3 |
| [models/ReviewRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewRules.java>) | [[ReviewRules]] | 3 |
| [models/ReviewStats.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java>) | [[ReviewStats]] | 3 |
| [models/ReviewSubjectRole.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewSubjectRole.java>) | [[ReviewSubjectRole]] | 3 |
| [models/SearchResult.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchResult.java>) | [[SearchResult]] | 3 |
| [models/SearchSuggestion.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java>) | [[SearchSuggestion]] | 3 |
| [models/SearchSuggestionType.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java>) | [[SearchSuggestionType]] | 3 |
| [models/SearchText.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchText.java>) | [[SearchText]] | 3 |
| [models/ShippingOptions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ShippingOptions.java>) | [[ShippingOptions]] | 3 |
| [models/User.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/User.java>) | [[User]] | 3 |
| [models/UserRole.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/UserRole.java>) | [[UserRole]] | 3 |
| [models/VinylInputRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java>) | [[VinylInputRules]] | 3 |

## persistence

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [persistence/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [persistence/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [persistence/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/pom.xml>) | [[Build and dependencies]] | 1 |
| [persistence/src/main/resources/db/migration/V10__sale_reviews.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V10__sale_reviews.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V11__carrito.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V11__carrito.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V8__post_gallery.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V8__post_gallery.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/main/resources/db/migration/V9__user_avatars.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V9__user_avatars.sql>) | [[Schema history and seeds]] · [[Database schema]] | 2 |
| [persistence/src/test/resources/populator.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/resources/populator.sql>) | [[Schema history and seeds]] · [[Testing and evidence]] | 2 |

## persistence · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [persistence/AddressJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AddressJdbcDao.java>) | [[AddressJdbcDao]] | 8 |
| [persistence/AlbumJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java>) | [[AlbumJdbcDao]] | 7 |
| [persistence/ArtistJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java>) | [[ArtistJdbcDao]] | 7 |
| [persistence/CartItemJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/CartItemJdbcDao.java>) | [[CartItemJdbcDao]] | 11 |
| [persistence/EmailVerificationTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>) | [[EmailVerificationTokenJdbcDao]] | 5 |
| [persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>) | [[ImageJdbcDao]] | 7 |
| [persistence/InquiryJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>) | [[InquiryJdbcDao]] | 9 |
| [persistence/MessageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/MessageJdbcDao.java>) | [[MessageJdbcDao]] | 9 |
| [persistence/PasswordResetTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java>) | [[PasswordResetTokenJdbcDao]] | 5 |
| [persistence/PostImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostImageJdbcDao.java>) | [[PostImageJdbcDao]] | 7 |
| [persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>) | [[PostJdbcDao]] | 4 |
| [persistence/ReviewJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java>) | [[ReviewJdbcDao]] | 10 |
| [persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>) | [[UserJdbcDao]] | 5 |

## persistence · Java de test

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [persistence/AddressJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AddressJdbcDaoTest.java>) | [[AddressJdbcDaoTest]] | 8 |
| [persistence/AlbumJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/AlbumJdbcDaoTest.java>) | [[AlbumJdbcDaoTest]] | 7 |
| [persistence/ArtistJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ArtistJdbcDaoTest.java>) | [[ArtistJdbcDaoTest]] | 7 |
| [persistence/CartItemJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java>) | [[CartItemJdbcDaoTest]] | 11 |
| [persistence/EmailVerificationTokenJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDaoTest.java>) | [[EmailVerificationTokenJdbcDaoTest]] | 5 |
| [persistence/ImageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ImageJdbcDaoTest.java>) | [[ImageJdbcDaoTest]] | 7 |
| [persistence/InquiryJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/InquiryJdbcDaoTest.java>) | [[InquiryJdbcDaoTest]] | 9 |
| [persistence/MessageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/MessageJdbcDaoTest.java>) | [[MessageJdbcDaoTest]] | 9 |
| [persistence/PasswordResetTokenJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDaoTest.java>) | [[PasswordResetTokenJdbcDaoTest]] | 5 |
| [persistence/PostImageJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostImageJdbcDaoTest.java>) | [[PostImageJdbcDaoTest]] | 7 |
| [persistence/PostJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/PostJdbcDaoTest.java>) | [[PostJdbcDaoTest]] | 4 |
| [persistence/ReviewJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/ReviewJdbcDaoTest.java>) | [[ReviewJdbcDaoTest]] | 10 |
| [persistence/TestConfiguration.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>) | [[TestConfiguration]] | 2 |
| [persistence/UserJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/UserJdbcDaoTest.java>) | [[UserJdbcDaoTest]] | 5 |

## persistence-contracts

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [persistence-contracts/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [persistence-contracts/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [persistence-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/pom.xml>) | [[Build and dependencies]] | 1 |

## persistence-contracts · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [persistence/AddressDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AddressDao.java>) | [[AddressDao]] | 8 |
| [persistence/AlbumDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/AlbumDao.java>) | [[AlbumDao]] | 7 |
| [persistence/ArtistDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ArtistDao.java>) | [[ArtistDao]] | 7 |
| [persistence/CartItemDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/CartItemDao.java>) | [[CartItemDao]] | 11 |
| [persistence/DuplicatePostKeyException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/DuplicatePostKeyException.java>) | [[DuplicatePostKeyException]] | 7 |
| [persistence/EmailVerificationTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java>) | [[EmailVerificationTokenDao]] | 5 |
| [persistence/ImageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java>) | [[ImageDao]] | 7 |
| [persistence/InquiryDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/InquiryDao.java>) | [[InquiryDao]] | 9 |
| [persistence/MessageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/MessageDao.java>) | [[MessageDao]] | 9 |
| [persistence/PasswordResetTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java>) | [[PasswordResetTokenDao]] | 5 |
| [persistence/PostDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>) | [[PostDao]] | 4 |
| [persistence/PostImageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostImageDao.java>) | [[PostImageDao]] | 7 |
| [persistence/ReviewDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ReviewDao.java>) | [[ReviewDao]] | 10 |
| [persistence/UserDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>) | [[UserDao]] | 5 |

## services

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [services/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [services/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [services/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/pom.xml>) | [[Build and dependencies]] | 1 |
| [services/src/main/resources/mail/email-verification.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/email-verification.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/inquiry-message.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/inquiry-message.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/inquiry-update.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/inquiry-update.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/password-changed.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/password-changed.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/password-reset.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/password-reset.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/post-interest.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>) | [[Mail delivery]] | 6 |
| [services/src/main/resources/mail/welcome.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/welcome.html>) | [[Mail delivery]] | 6 |

## services · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [services/AddressServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AddressServiceImpl.java>) | [[AddressServiceImpl]] | 8 |
| [services/AlbumServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>) | [[AlbumServiceImpl]] | 7 |
| [services/ArtistServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>) | [[ArtistServiceImpl]] | 7 |
| [services/CartServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/CartServiceImpl.java>) | [[CartServiceImpl]] | 11 |
| [services/ContactRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ContactRules.java>) | [[ContactRules]] | 8 |
| [services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) | [[EmailServiceImpl]] | 6 |
| [services/ImageServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>) | [[ImageServiceImpl]] | 7 |
| [services/InquiryServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>) | [[InquiryServiceImpl]] | 9 |
| [services/Pagination.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>) | [[Pagination]] | 4 |
| [services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>) | [[PostServiceImpl]] | 4 |
| [services/PublicProfileServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java>) | [[PublicProfileServiceImpl]] | 10 |
| [services/ReviewServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ReviewServiceImpl.java>) | [[ReviewServiceImpl]] | 10 |
| [services/SupportedLocales.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/SupportedLocales.java>) | [[SupportedLocales]] | 6 |
| [services/TransactionCallbacks.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>) | [[TransactionCallbacks]] | 6 |
| [services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) | [[UserServiceImpl]] | 5 |

## services · Java de test

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [services/AddressServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AddressServiceImplTest.java>) | [[AddressServiceImplTest]] | 8 |
| [services/AlbumServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/AlbumServiceImplTest.java>) | [[AlbumServiceImplTest]] | 7 |
| [services/ArtistServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ArtistServiceImplTest.java>) | [[ArtistServiceImplTest]] | 7 |
| [services/CartServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java>) | [[CartServiceImplTest]] | 11 |
| [services/ContactRulesTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ContactRulesTest.java>) | [[ContactRulesTest]] | 8 |
| [services/EmailServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/EmailServiceImplTest.java>) | [[EmailServiceImplTest]] | 6 |
| [services/ImageServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ImageServiceImplTest.java>) | [[ImageServiceImplTest]] | 7 |
| [services/InMemoryImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java>) | [[InMemoryImageService]] | 7 |
| [services/InquiryServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryServiceImplTest.java>) | [[InquiryServiceImplTest]] | 9 |
| [services/InquiryStatusFilterTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InquiryStatusFilterTest.java>) | [[InquiryStatusFilterTest]] | 9 |
| [services/PaginationTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PaginationTest.java>) | [[PaginationTest]] | 4 |
| [services/PostServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PostServiceImplTest.java>) | [[PostServiceImplTest]] | 4 |
| [services/PublicProfileServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/PublicProfileServiceImplTest.java>) | [[PublicProfileServiceImplTest]] | 10 |
| [services/ReceiptTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ReceiptTest.java>) | [[ReceiptTest]] | 9 |
| [services/ReviewServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/ReviewServiceImplTest.java>) | [[ReviewServiceImplTest]] | 10 |
| [services/UserServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/UserServiceImplTest.java>) | [[UserServiceImplTest]] | 5 |

## services-contracts

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [services-contracts/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [services-contracts/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [services-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/pom.xml>) | [[Build and dependencies]] | 1 |

## services-contracts · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [services/AddressLimitExceededException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressLimitExceededException.java>) | [[AddressLimitExceededException]] | 8 |
| [services/AddressNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressNotFoundException.java>) | [[AddressNotFoundException]] | 8 |
| [services/AddressService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AddressService.java>) | [[AddressService]] | 8 |
| [services/AlbumService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/AlbumService.java>) | [[AlbumService]] | 7 |
| [services/ArtistService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ArtistService.java>) | [[ArtistService]] | 7 |
| [services/CartAddRejectedException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/CartAddRejectedException.java>) | [[CartAddRejectedException]] | 11 |
| [services/CartService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/CartService.java>) | [[CartService]] | 11 |
| [services/ConcurrentPublishException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ConcurrentPublishException.java>) | [[ConcurrentPublishException]] | 7 |
| [services/DuplicatePostException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicatePostException.java>) | [[DuplicatePostException]] | 7 |
| [services/DuplicateUserException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/DuplicateUserException.java>) | [[DuplicateUserException]] | 5 |
| [services/EmailService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/EmailService.java>) | [[EmailService]] | 6 |
| [services/ForbiddenOperationException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ForbiddenOperationException.java>) | [[ForbiddenOperationException]] | 9 |
| [services/ImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java>) | [[ImageService]] | 7 |
| [services/InquiryEvent.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryEvent.java>) | [[InquiryEvent]] | 6 |
| [services/InquiryNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryNotFoundException.java>) | [[InquiryNotFoundException]] | 9 |
| [services/InquiryService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryService.java>) | [[InquiryService]] | 9 |
| [services/InquiryUpdateNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InquiryUpdateNotification.java>) | [[InquiryUpdateNotification]] | 6 |
| [services/InvalidCurrentPasswordException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidCurrentPasswordException.java>) | [[InvalidCurrentPasswordException]] | 5 |
| [services/InvalidImageException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidImageException.java>) | [[InvalidImageException]] | 7 |
| [services/InvalidInquiryStateException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidInquiryStateException.java>) | [[InvalidInquiryStateException]] | 9 |
| [services/InvalidMessageException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidMessageException.java>) | [[InvalidMessageException]] | 9 |
| [services/InvalidPaymentInfoException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPaymentInfoException.java>) | [[InvalidPaymentInfoException]] | 8 |
| [services/InvalidPostDataException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidPostDataException.java>) | [[InvalidPostDataException]] | 7 |
| [services/InvalidReceiptException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidReceiptException.java>) | [[InvalidReceiptException]] | 9 |
| [services/InvalidReviewException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidReviewException.java>) | [[InvalidReviewException]] | 10 |
| [services/InvalidSearchQueryException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/InvalidSearchQueryException.java>) | [[InvalidSearchQueryException]] | 4 |
| [services/MessageNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/MessageNotification.java>) | [[MessageNotification]] | 6 |
| [services/MissingPaymentInfoException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/MissingPaymentInfoException.java>) | [[MissingPaymentInfoException]] | 8 |
| [services/NothingToSendException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/NothingToSendException.java>) | [[NothingToSendException]] | 11 |
| [services/OpenInquiryExistsException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/OpenInquiryExistsException.java>) | [[OpenInquiryExistsException]] | 8 |
| [services/PageNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PageNotFoundException.java>) | [[PageNotFoundException]] | 4 |
| [services/PasswordHasher.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java>) | [[PasswordHasher]] | 5 |
| [services/PaymentInfoRequiredException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PaymentInfoRequiredException.java>) | [[PaymentInfoRequiredException]] | 8 |
| [services/PostInterestNotification.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostInterestNotification.java>) | [[PostInterestNotification]] | 6 |
| [services/PostNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostNotFoundException.java>) | [[PostNotFoundException]] | 4 |
| [services/PostService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>) | [[PostService]] | 4 |
| [services/PostUnavailableException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostUnavailableException.java>) | [[PostUnavailableException]] | 7 |
| [services/PublicProfileService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java>) | [[PublicProfileService]] | 10 |
| [services/ReceiptNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ReceiptNotFoundException.java>) | [[ReceiptNotFoundException]] | 9 |
| [services/ReviewService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ReviewService.java>) | [[ReviewService]] | 10 |
| [services/UnchangedPasswordException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UnchangedPasswordException.java>) | [[UnchangedPasswordException]] | 5 |
| [services/UserNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserNotFoundException.java>) | [[UserNotFoundException]] | 5 |
| [services/UserService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>) | [[UserService]] | 5 |

## tools

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [tools/git-hooks/pre-commit](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/git-hooks/pre-commit>) | [[Development tools]] | 15 |
| [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>) | [[Development tools]] | 15 |
| [tools/seed_local_data.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/seed_local_data.sh>) | [[Schema history and seeds]] · [[Development tools]] | 2 |
| [tools/setup_local_postgres.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/setup_local_postgres.sh>) | [[Configuration and running]] · [[Development tools]] | 2 |
| [tools/sql/demo-users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/sql/demo-users.sql>) | [[Schema history and seeds]] | 2 |

## webapp

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [webapp/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/.mvn/jvm.config>) | [[Repository tooling]] | 1 |
| [webapp/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/.mvn/maven.config>) | [[Repository tooling]] | 1 |
| [webapp/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/pom.xml>) | [[Build and dependencies]] | 1 |
| [webapp/src/main/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/database.properties.example>) | [[Configuration and running]] | 1 |
| [webapp/src/main/resources/i18n/messages.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>) | [[Localization]] | 14 |
| [webapp/src/main/resources/i18n/messages_en.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>) | [[Localization]] | 14 |
| [webapp/src/main/resources/i18n/messages_es.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>) | [[Localization]] | 14 |
| [webapp/src/main/resources/i18n/messages_fr.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>) | [[Localization]] | 14 |
| [webapp/src/main/resources/logback-test.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>) | [[Logging]] | 1 |
| [webapp/src/main/resources/logback.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback.xml>) | [[Logging]] | 1 |
| [webapp/src/main/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>) | [[Configuration and running]] | 1 |
| [webapp/src/main/webapp/WEB-INF/tags/account-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/address-fields.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address-fields.tag>) | [[UI components]] | 8 |
| [webapp/src/main/webapp/WEB-INF/tags/address.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address.tag>) | [[UI components]] | 8 |
| [webapp/src/main/webapp/WEB-INF/tags/avatar.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/avatar.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/back-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/back-link.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/brand.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/brand.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/button.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/h1.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/h3.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/head.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/icon.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/icon.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/input-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/input-control.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag>) | [[UI components]] | 9 |
| [webapp/src/main/webapp/WEB-INF/tags/p.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag>) | [[UI components]] | 4 |
| [webapp/src/main/webapp/WEB-INF/tags/pagination.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination.tag>) | [[UI components]] | 4 |
| [webapp/src/main/webapp/WEB-INF/tags/post-badge.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/post-badge.tag>) | [[UI components]] | 4 |
| [webapp/src/main/webapp/WEB-INF/tags/rating.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/rating.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag>) | [[UI components]] | 5 |
| [webapp/src/main/webapp/WEB-INF/tags/review-content.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/review-content.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/select-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select-control.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/select.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/span.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/text-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/textarea.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/textarea.tag>) | [[UI components]] | 13 |
| [webapp/src/main/webapp/WEB-INF/tags/user-byline.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/user-byline.tag>) | [[UI components]] | 10 |
| [webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>) | [[UI components]] | 4 |
| [webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/auth/login.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/auth/register.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>) | [[Views and assets]] · [[Authentication flow]] | 5 |
| [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>) | [[Views and assets]] · [[Cart flow]] | 11 |
| [webapp/src/main/webapp/WEB-INF/views/error/400.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/400.jsp>) | [[Views and assets]] · [[Validation and errors]] | 12 |
| [webapp/src/main/webapp/WEB-INF/views/error/403.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/403.jsp>) | [[Views and assets]] · [[Validation and errors]] | 12 |
| [webapp/src/main/webapp/WEB-INF/views/error/404.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/404.jsp>) | [[Views and assets]] · [[Validation and errors]] | 12 |
| [webapp/src/main/webapp/WEB-INF/views/error/409.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/409.jsp>) | [[Views and assets]] · [[Validation and errors]] | 12 |
| [webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp>) | [[Views and assets]] · [[Inquiry and sale flow]] | 9 |
| [webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp>) | [[Views and assets]] · [[Inquiry and sale flow]] | 9 |
| [webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp>) | [[Views and assets]] · [[Inquiry and sale flow]] | 9 |
| [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>) | [[Views and assets]] · [[Landing flow]] | 4 |
| [webapp/src/main/webapp/WEB-INF/views/post/contact.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>) | [[Views and assets]] · [[Post detail flow]] | 8 |
| [webapp/src/main/webapp/WEB-INF/views/post/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp>) | [[Views and assets]] · [[Post detail flow]] | 8 |
| [webapp/src/main/webapp/WEB-INF/views/profile/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/index.jsp>) | [[Views and assets]] · [[Profile flow]] | 10 |
| [webapp/src/main/webapp/WEB-INF/views/profile/public.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/public.jsp>) | [[Views and assets]] · [[Profile flow]] | 10 |
| [webapp/src/main/webapp/WEB-INF/views/publish/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>) | [[Views and assets]] · [[Publish flow]] | 7 |
| [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>) | [[Startup and dependency injection]] · [[Security and authorization]] | 1 |
| [webapp/src/main/webapp/css/components.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/components.css>) | [[UI styles and tokens]] | 13 |
| [webapp/src/main/webapp/css/style.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/style.css>) | [[UI styles and tokens]] | 13 |
| [webapp/src/main/webapp/css/tokens.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/tokens.css>) | [[UI styles and tokens]] | 13 |
| [webapp/src/main/webapp/images/covers/placeholder.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/covers/placeholder.svg>) | [[Views and assets]] | 7 |
| [webapp/src/main/webapp/images/logo.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/logo.svg>) | [[Views and assets]] | 13 |
| [webapp/src/main/webapp/js/account-edit.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/account-edit.js>) | [[Views and assets]] | 10 |
| [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>) | [[Views and assets]] | 4 |
| [webapp/src/main/webapp/js/catalog.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>) | [[Views and assets]] | 4 |
| [webapp/src/main/webapp/js/confirm-action.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>) | [[Views and assets]] | 9 |
| [webapp/src/main/webapp/js/post-gallery.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/post-gallery.js>) | [[Views and assets]] | 8 |
| [webapp/src/main/webapp/js/publish-preview.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/publish-preview.js>) | [[Views and assets]] | 7 |
| [webapp/src/main/webapp/js/sale-detail.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/sale-detail.js>) | [[Views and assets]] | 9 |
| [webapp/src/main/webapp/js/submit-once.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>) | [[Views and assets]] | 9 |
| [webapp/src/pampero/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/database.properties.example>) | [[Configuration and running]] | 1 |
| [webapp/src/pampero/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/mail.properties.example>) | [[Configuration and running]] | 1 |

## webapp · Java

| Archivo | Nota del vault | Etapa |
|---|---|---|
| [config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>) | [[SecurityConfig]] | 5 |
| [config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) | [[WebConfig]] | 1 |
| [controller/ArtistSuggestionController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java>) | [[ArtistSuggestionController]] | 4 |
| [controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>) | [[AuthenticationController]] | 5 |
| [controller/CartController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartController.java>) | [[CartController]] | 11 |
| [controller/CartCountAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartCountAdvice.java>) | [[CartCountAdvice]] | 11 |
| [controller/CartExceptionAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java>) | [[CartExceptionAdvice]] | 11 |
| [controller/ErrorController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java>) | [[ErrorController]] | 12 |
| [controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>) | [[ErrorResponseAdvice]] | 12 |
| [controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>) | [[ImageController]] | 7 |
| [controller/InquiryController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>) | [[InquiryController]] | 9 |
| [controller/LandingController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>) | [[LandingController]] | 4 |
| [controller/ListingQueries.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java>) | [[ListingQueries]] | 4 |
| [controller/PostContactController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostContactController.java>) | [[PostContactController]] | 8 |
| [controller/PostController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostController.java>) | [[PostController]] | 8 |
| [controller/PostOrigin.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java>) | [[PostOrigin]] | 4 |
| [controller/ProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java>) | [[ProfileController]] | 10 |
| [controller/PublicProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java>) | [[PublicProfileController]] | 10 |
| [controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>) | [[PublishController]] | 7 |
| [controller/SearchSuggestionController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java>) | [[SearchSuggestionController]] | 4 |
| [dto/ArtistSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java>) | [[ArtistSuggestionDto]] | 4 |
| [dto/SearchSuggestionDto.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java>) | [[SearchSuggestionDto]] | 4 |
| [exceptions/ImageNotFoundException.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/exceptions/ImageNotFoundException.java>) | [[ImageNotFoundException]] | 7 |
| [form/AddressForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/AddressForm.java>) | [[AddressForm]] | 8 |
| [form/AvatarForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/AvatarForm.java>) | [[AvatarForm]] | 10 |
| [form/CatalogFilterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java>) | [[CatalogFilterForm]] | 4 |
| [form/ChangePasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ChangePasswordForm.java>) | [[ChangePasswordForm]] | 10 |
| [form/ContactForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ContactForm.java>) | [[ContactForm]] | 8 |
| [form/ForgotPasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ForgotPasswordForm.java>) | [[ForgotPasswordForm]] | 5 |
| [form/ImageFiles.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java>) | [[ImageFiles]] | 7 |
| [form/LineBreakNormalizingEditor.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/LineBreakNormalizingEditor.java>) | [[LineBreakNormalizingEditor]] | 8 |
| [form/LoginForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/LoginForm.java>) | [[LoginForm]] | 5 |
| [form/MessageForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/MessageForm.java>) | [[MessageForm]] | 9 |
| [form/PaymentForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PaymentForm.java>) | [[PaymentForm]] | 8 |
| [form/ProfileForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ProfileForm.java>) | [[ProfileForm]] | 10 |
| [form/PublishForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java>) | [[PublishForm]] | 7 |
| [form/ReceiptForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReceiptForm.java>) | [[ReceiptForm]] | 9 |
| [form/RegisterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java>) | [[RegisterForm]] | 5 |
| [form/ResetPasswordForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ResetPasswordForm.java>) | [[ResetPasswordForm]] | 5 |
| [form/ReviewForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ReviewForm.java>) | [[ReviewForm]] | 10 |
| [form/ShippingAddressForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ShippingAddressForm.java>) | [[ShippingAddressForm]] | 8 |
| [security/AddressAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java>) | [[AddressAccessHandler]] | 8 |
| [security/AuthenticatedUser.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>) | [[AuthenticatedUser]] | 5 |
| [security/AuthenticatedUserDetailsService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java>) | [[AuthenticatedUserDetailsService]] | 5 |
| [security/AuthenticationSessions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java>) | [[AuthenticationSessions]] | 5 |
| [security/InquiryAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java>) | [[InquiryAccessHandler]] | 9 |
| [security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>) | [[MultipartExceptionHandlerFilter]] | 7 |
| [security/PostAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java>) | [[PostAccessHandler]] | 7 |
| [security/SameSiteRedirects.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java>) | [[SameSiteRedirects]] | 5 |
| [security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>) | [[VerificationAccessDeniedHandler]] | 5 |
| [validation/AvatarFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/AvatarFormValidator.java>) | [[AvatarFormValidator]] | 10 |
| [validation/CatalogFilterValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java>) | [[CatalogFilterValidator]] | 4 |
| [validation/MatchingPasswords.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswords.java>) | [[MatchingPasswords]] | 5 |
| [validation/MatchingPasswordsValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/MatchingPasswordsValidator.java>) | [[MatchingPasswordsValidator]] | 5 |
| [validation/PasswordsMatching.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PasswordsMatching.java>) | [[PasswordsMatching]] | 5 |
| [validation/PaymentFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PaymentFormValidator.java>) | [[PaymentFormValidator]] | 8 |
| [validation/PublishFormValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java>) | [[PublishFormValidator]] | 7 |
| [validation/ReceiptValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java>) | [[ReceiptValidator]] | 9 |
| [validation/ShippingAddressValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ShippingAddressValidator.java>) | [[ShippingAddressValidator]] | 8 |
| [validation/ValidAvatarForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidAvatarForm.java>) | [[ValidAvatarForm]] | 10 |
| [validation/ValidCatalogFilters.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidCatalogFilters.java>) | [[ValidCatalogFilters]] | 4 |
| [validation/ValidPassword.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPassword.java>) | [[ValidPassword]] | 5 |
| [validation/ValidPaymentForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPaymentForm.java>) | [[ValidPaymentForm]] | 8 |
| [validation/ValidPublishForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidPublishForm.java>) | [[ValidPublishForm]] | 7 |
| [validation/ValidReceipt.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidReceipt.java>) | [[ValidReceipt]] | 9 |
| [validation/ValidShippingAddress.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ValidShippingAddress.java>) | [[ValidShippingAddress]] | 8 |
