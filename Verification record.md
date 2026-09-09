---
title: Verification record
categories: [Testing]
type: guide
module: vault
project: quieroVinilos
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: verified-static
---

# Verification record

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
