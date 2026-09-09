---
title: Verification record
categories: [Testing]
type: guide
module: vault
project: quieroVinilos
snapshot: "2026-09-09"
commit: "041ce34404963b689d05443ca00abb7e75aa7f15"
status: verified-static
---

# Verification record

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
