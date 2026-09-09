---
title: "Vault guide"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "navigation"]
---

# Vault guide

All content notes and future attachments go in the vault root. Only category views live in `Categories/`. Existing hidden Obsidian and skill folders remain infrastructure. Nothing needs to be physically moved when its subject changes.

## Categories

Use a YAML list property called categories. Each item is a plain category name matching a `.base` view. A note can contain several names and will appear in every matching Base. The base is a saved query, not a container that owns the note.

```yaml
categories:
  - Web
  - Flows
type: guide
module: webapp
project: quieroVinilos
snapshot: "2026-09-09"
status: documented
```

[[Categories/All notes.base]] lists categorized notes. [[Categories/Inbox.base]] catches newly dropped Markdown files without a categories property. [[Note template]] is a root-level starter, deliberately excluded from category views until copied and changed from type template.

| Category | Contents |
|---|---|
| Navigation | Home, inventory and vault maintenance |
| Architecture | Module boundaries and startup |
| Domain | Business identities and model values |
| Web | Controllers, forms, views and validation |
| Services | Business APIs, implementations, transactions and mail |
| Persistence | DAO contracts, implementations, schema and seeds |
| Flows | End-to-end HTTP traces |
| Operations | Build, runtime configuration, logging and tools |
| Testing | Test suites and evidence limits |
| History | Specs, decisions and known drift |

## Search and navigation

Use Quick Switcher for a class name such as PostServiceImpl. Follow its Connections section to contracts, callers and tests. Follow flow notes when you need runtime order rather than static references. The local graph and backlinks show incoming connections automatically.

Useful searches in Obsidian:

```text
[categories:Services]
[module:webapp]
[type:test]
"EmailDeliveryException"
"publisher_email"
```

Metadata lists are quoted in YAML when needed. Source code remains in fenced blocks so Java brackets do not become accidental note links. Root-level attachments can be embedded with wikilinks using their real filename.

## Updating a code map

1. Read the current repository source and compare its Git revision/state to [[Project snapshot]].
2. Update the affected code notes, exact source excerpts, flow explanations and resource notes together.
3. Distinguish implemented source, historical requirements and runtime observations. Record discrepancies in [[Known gaps and document drift]].
4. Update the commit/snapshot properties only for notes rechecked against that revision. Preserve evidence dates for older notes.
5. Reconcile [[Source inventory]] with tracked files. Check links, YAML and Base results, then record verification in [[Verification record]].

[[AGENTS]] is the maintenance instruction entry point. Edit that file once; CLAUDE.md is its symlink. This setup uses standard uppercase filenames for agent discovery.


## Diagrams in a new vault

Obsidian may show a one-time Allow prompt before rendering Mermaid. The flow and domain notes also explain each diagram in prose and tables. See [[Verification record]] for the rendering status.

The original starter note is retained at [[Welcome]].