---
title: Verification record
categories: [Testing]
type: guide
module: vault
project: quieroVinilos
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: verified-static
---

# Verification record

## Refresh through f12af08, 2026-09-22

The target is `f12af080cf6a27101160f005102a20f436574cf7`, the head of local main and of the local origin/main ref; no fetch was performed. The source working tree was clean. The range from `40328f0` has 101 commits and 168 changed, added or deleted paths, including 29 new Java files and no deleted ones. Two non-Java files were deleted: database/albums.sql and views/inquiry/index.jsp.

The 123 Java notes were regenerated from the Git objects at the target by a script whose output format was first calibrated against `40328f0`: it reproduced all 94 existing code notes byte for byte, including their Connections lines, which count project type names used outside comments. Summaries were then rewritten for every new or changed class and for unchanged classes whose behavior changed around them. Flow, mechanism and resource notes were rewritten from the current source with the same structure, and five flows plus the [[Paginated listings]] guide were added.

| Check | Result |
|---|---|
| Canonical root Markdown | 170 notes, excluding the CLAUDE symlink |
| Current source coverage | All 326 tracked paths mapped exactly once in [[Source inventory]]; all 123 Java source/test files have dedicated notes |
| Current exact excerpts | 241 excerpts match their cited line ranges in the target Git objects |
| Source links and metadata | All 326 distinct local source-link targets exist; every `sources` entry of the 159 notes pinned to `f12af08` is a tracked path |
| Frontmatter | YAML parses on all 170 notes; every note has a valid category list |
| Category counts | All notes Base scope 169 (template excluded); Inbox scope 0; Flows 12 (eleven flows and the audit) |
| Internal links | A static resolver over note names and vault files finds zero unresolved wikilinks and embeds |
| Diagrams | The twelve Mermaid diagrams written in this refresh parse and render with mermaid-cli 11.17 in headless Chromium |
| Repository static checker | python3 tools/paw_checks.py all reports i18n OK and jsp OK |
| Agent entry point | CLAUDE.md remains a relative symlink to AGENTS.md |

Obsidian itself was not available from the environment used for this refresh, so Bases were not queried through the Obsidian CLI, the reading view was not inspected and Obsidian's bundled Mermaid version was not exercised. The category counts above come from the same filters evaluated over parsed frontmatter.

Documentation conflicts found while reading the source, such as stale CONTEXT.md and TODO.md statements, implemented specifications still marked ready, the per-page catalog counter, the accent-sensitive submitted search and a likely failure of the demo seed against the new NOT NULL search_phrase columns, are recorded in [[Known gaps and document drift]]. The seed failure is a static inference.

A `git status` run during inspection left an empty .git/index.lock in the source checkout. It was deleted immediately; no tracked source file changed. The pre-existing uncommitted vault changes to .obsidian/app.json, Categories/Architecture.base and the 2026-09-17 audit sections were preserved, and this refresh was not committed to the vault repository.

No Maven test or build, JSP compilation, application server, PostgreSQL mutation or concurrency run, SMTP delivery or deployment was performed. Source assertions and static checks do not establish application runtime behavior. Earlier records below retain their original counts and limits.

[[Home]] · [[Source inventory]] · [[Testing and evidence]] · [[Known gaps and document drift]]

## Flow snippets and sequence diagrams, 2026-09-16

Updated the six current flow notes with twelve focused Java snippets and six Mermaid sequence diagrams. The diagram style follows the previous Landing/Publish/Contact flow notes at vault commit 3920982: class participants, method-call arrows, return arrows and alt/opt branches. The calls reflect source revision 40328f0 rather than restoring outdated behavior.

- All twelve added snippets match the cited source paths and line ranges. The vault now has 150 current excerpts and five historical excerpts matching their pinned Git objects.
- Obsidian's loaded Mermaid renderer generated SVG successfully for all six diagrams. Authentication and cover sequence diagrams and their snippets were also observed in the reading-view DOM. This is documentation-rendering evidence, not application execution.
- The Flows Base lists all six current flows; Obsidian reports zero unresolved links. Source coverage remains 257 tracked paths and 94 Java notes; all 436 local source-link targets exist.
- Source main remains at 40328f0. A concurrent local edit to persistence/src/main/resources/schema.sql adds a legacy verification-token migration. This task preserved that edit and kept the snippets pinned to the committed revision. The earlier clean-checkout assertion belongs to the previous refresh, not this follow-up.
- No application source edits or runtime tests were performed. Existing Obsidian configuration/Base formatting changes remain outside the documentation commit.

[[Authentication flow]] · [[Landing flow]] · [[Publish flow]] · [[Contact flow]] · [[Inquiry and sale flow]] · [[Cover image flow]]

## Refresh through 40328f0, 2026-09-16

The target is origin/main at `40328f0a23ce3814ab62a9f0124a6ba1e6ae71be`, fetched during this task. The initial local branch was the sale branch at aea81a9, whose tree already matched the target. The user then switched to local main at the target revision. Final source checks use that clean local main checkout. The diff from ff96f27 has 125 changed or added paths.

| Check | Result |
|---|---|
| Canonical root Markdown | 134 notes, excluding the CLAUDE symlink |
| Current source coverage | All 257 tracked paths mapped exactly once; all 94 Java source/test files have dedicated notes |
| Current exact excerpts | 138 match their cited source-line ranges |
| Historical exact excerpts | Five match pinned pre-removal Git objects |
| Source links/metadata | All 424 local source-link targets exist; all current source metadata refers to tracked paths |
| Checkout identity | Every tracked source file byte-matches the target Git object |
| Categories | Obsidian metadata has valid category lists on all 134 canonical notes |
| Bases | All 12 query successfully through Obsidian CLI with vault=PAW_Vault |
| All notes / Inbox | 133 categorized non-template notes / zero uncategorized notes |
| Internal links | Obsidian unresolved total is zero; static wikilink resolution also passes |
| Reading view | Inquiry and sale flow is in preview mode; rendered DOM contains the current owner/state/transaction explanation and one Mermaid SVG |
| Repository static checker | python3 tools/paw_checks.py all reports i18n OK and jsp OK |
| Whitespace | git diff --check passes |
| Agent entry point | CLAUDE.md remains a relative symlink to AGENTS.md |
| Source application preservation | No application edits by this task; source working tree is clean |

The old web UserNotFoundException note is preserved as [[Legacy UserNotFoundException]]; the current [[UserNotFoundException]] is the new services-contracts class. Authentication, inquiries/sales, filters, per-post images, configuration, views, schema and related test explanations were updated together. Notes for unaffected tooling and historical code retain their earlier evidence dates.

The pre-existing .obsidian/app.json and Categories/Architecture.base formatting changes are preserved outside this documentation commit. Bases were checked in their current working-tree form.

No Maven test/build, JSP compilation, application server, PostgreSQL mutation/concurrency run, real SMTP delivery or deployment was performed. Source assertions, a rendered vault note and static checks do not establish application runtime behavior. Earlier records below retain their original counts and limits.

[[Home]] · [[Source inventory]] · [[Testing and evidence]] · [[Known gaps and document drift]]

## Refresh through ff96f27, 2026-09-09

Target and local source HEAD are `ff96f275ae009bad4534751b7a4857cf45aea7ac`. The source working tree is clean. The comparison with 041ce34 contains 71 changed/added/deleted paths across image upload, async mail, schema, tests, packaging/logging and scaffold cleanup. The initial read used a temporary Git archive while the checkout still pointed to 041ce34; the final checks use the user's updated checkout at ff96f27.

| Check | Result |
|---|---|
| Canonical root Markdown | 92 notes; eleven new notes for image code/tests and the cover flow |
| Current source coverage | All 196 tracked paths mapped; all 54 current Java files have a dedicated note |
| Current exact excerpts | 86 match source-line ranges in the target checkout |
| Historical exact excerpts | Five removed Java excerpts match pinned Git objects at 041ce34 |
| Source metadata/links | Referenced current sources exist; all 310 local source-link targets exist |
| Java checkout identity | All 54 current Java files byte-match their target Git objects |
| Categories | Every note has a valid category list in Obsidian metadata |
| Bases | All 12 query successfully through Obsidian CLI using vault=PAW_Vault |
| All notes / Inbox | 91 non-template categorized notes / zero uncategorized notes |
| Internal links | No unresolved links reported by Obsidian |
| Reading view | Cover image flow renders in preview mode with current metadata, storage decisions, limits and retrieval text |
| Repository checker | python3 tools/paw_checks.py all returns i18n OK and jsp OK; main checker no longer has Flyway |
| Agent entry point | CLAUDE.md remains a relative symlink to AGENTS.md |
| Source application preservation | No source edits by this task; source git status is clean |

Code references and reverse references were rechecked against current Java sources. Removed code and routes are categorized as History; their older excerpts do not claim to be current implementation. Documentation conflicts are recorded in [[Known gaps and document drift]], including old SMTP recovery requirements and README startup/configuration claims.

No Maven tests/build, JSP compilation, application server, PostgreSQL mutation or actual SMTP delivery was run. The checks above verify documentation and static source consistency. They do not establish deployed behavior, async saturation, image decoding or schema-upgrade safety.

[[Home]] · [[Source inventory]] · [[Testing and evidence]] · [[Cover image flow]]

## Earlier verification records

The sections below are historical records. Their earlier counts, source states and checker names do not describe this refresh.

## Current refresh, 2026-09-09

Updated the vault from baseline 16f3aa7 and its provisional UI snapshot to committed HEAD `041ce34404963b689d05443ca00abb7e75aa7f15`. Git reports a clean working tree. The diff contains 17 changed or added paths, all in JSP views/tags, CSS and locale bundles. No backend Java, test, SQL or Maven file changed. Notes outside this refresh retain their original commit metadata.

| Check | Result |
|---|---|
| Root notes | 81 canonical Markdown files |
| Source inventory | All 196 tracked paths covered; obsolete provisional tag entries removed |
| Exact excerpts | All 83 excerpts match the cited source-line ranges, including updated JSP, tag, CSS and default bundle blocks |
| External source links | All 306 local source link targets exist |
| Obsidian categories | CLI metadata exposes a valid category list on every canonical note |
| Category Bases | All 12 queried successfully through CLI using vault=PAW_Vault |
| All notes / Inbox | 80 categorized non-template notes / zero uncategorized notes |
| Internal links | Obsidian unresolved total returns zero |
| Source preservation | No application edits; git status --porcelain is empty after verification |
| Static repository checks | python3 .claude/scripts/paw_checks.py all: i18n OK, flyway OK, jsp OK |
| Reading view | UI components opened in preview mode; CLI DOM confirms current commit, seven-tag introduction, form explanation and button excerpt |
| Agent entry point | CLAUDE.md remains the relative symlink AGENTS.md |

Obsidian CLI exited with code 134 inside the sandbox, then worked through the approved external CLI invocation. These checks establish documentation consistency and static source checks. They do not establish JSP compilation, browser layout, binding behavior at runtime, database migrations or email delivery. No Maven tests, server startup, database writes or SMTP delivery were run.

The previous record below is historical evidence from the initial map. Its counts, provisional UI state and rendering limitation do not describe the current refresh.

[[Home]] · [[Source inventory]] · [[Testing and evidence]] · [[Known gaps and document drift]]

## Previous verification at 16f3aa7

### Checks completed

| Check | Result |
|---|---|
| Content notes | 81 canonical root Markdown files, including instructions and template |
| Agent entry point | CLAUDE.md is a relative symlink to AGENTS.md |
| Category Bases | All 12 queried successfully through Obsidian CLI |
| Categorized notes | All notes Base returns 80; the template is excluded intentionally |
| Uncategorized Markdown | Inbox Base returns zero |
| Internal links | Obsidian unresolved reports zero |
| Source coverage | All 187 tracked paths and 13 working-tree additions have inventory entries |
| Source excerpts | All 87 exact excerpts match the cited source-line ranges |
| External source links | All 314 file-link targets exist |
| Source preservation | This task made no application edits. A final 200-file SHA-256 snapshot was stable across the UI refresh verification |
| Repository checks | paw_checks.py all returns i18n OK, flyway OK, jsp OK |
| Home rendering | Reading-view DOM includes the guide and embedded Navigation Base with six results |
| Navigation | Home, All notes and Inbox bookmarked through CLI |
| Vault structure | Content in root; Bases in Categories; existing theme and graph workspace preserved |

### Concurrent source edits

The repository was initially clean. During final checks, another source of edits changed three product JSPs, three i18n bundles and style.css, and added eleven JSP tags plus two CSS files. The affected notes and excerpts were refreshed, and the new files were added to the inventory. Java service/controller/DAO behavior remained unchanged. These UI changes are marked as a working-tree snapshot rather than attributed to the baseline commit. No build or runtime assertion is made for this concurrent work.

### Rendering limit

Obsidian displays a one-time “Display Mermaid diagrams in this vault?” prompt with an Allow button. Diagram rendering remains gated by that vault trust choice. The diagram source and equivalent prose/tables are present, but the diagrams were not marked visually verified. When you choose Allow in a diagram note, Obsidian can render them. No permission setting was bypassed.

The sandboxed Obsidian CLI initially exited with code 134. Retrying the same CLI outside the sandbox succeeded, and subsequent vault/query/DOM checks used that approved CLI path. Desktop automation was not used for the completed verification.

### Not run

No Maven tests, PostgreSQL mutations, server startup, actual SMTP delivery or course deployment were performed. No external issue tracker was queried. Existing test code and historical done labels are described as source evidence, not fresh successful executions. Agent-tooling files are inventoried by role rather than treated as runtime application code.

[[Home]] · [[Testing and evidence]] · [[Source inventory]] · [[Vault guide]]

## Audit de ejecución local, 2026-09-17

[[Audit local 2026-09-17]] registra pruebas sobre el worktree `redesign-header-filtros`, commit `e5e926d4c1f2026494b3dc03768d984092b1052a`. No es una actualización del inventario de `40328f0`.

- PostgreSQL confirmó 27 publicaciones con imagen, dos usuarios activos (IDs 1 y 3) y seis consultas PENDING. Los endpoints de las 27 imágenes respondieron 200 con contenido JPEG. Se observaron seis avisos de interés en Apple Mail.
- Los once fragmentos del informe coinciden exactamente con sus archivos y líneas en la rama ejecutada. Los enlaces internos del informe resuelven. La cobertura completa del inventario histórico no se recalculó para esta rama.
- Obsidian CLI, con `vault=PAW_Vault`, confirmó cero enlaces sin resolver, categorías válidas del informe, doce Bases consultables y cero notas en Inbox. Testing incluye el informe nuevo. Una comprobación preliminar que asumía JSON para todos los archivos Base se descartó: algunas vistas usan YAML; la validación final fue mediante Obsidian.
- `CLAUDE.md` continúa como enlace relativo a `AGENTS.md`. Los checkouts de la aplicación se verificaron limpios; no hubo cambios de código. Se preservaron cambios preexistentes en `.obsidian/app.json` y `Categories/Architecture.base`.
- Las limitaciones de pruebas negativas, del navegador y de alcance están detalladas en el informe. La evidencia de SMTP corresponde a esos seis mensajes, no a una garantía general de entrega.
