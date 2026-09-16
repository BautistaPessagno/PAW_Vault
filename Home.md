---
title: "Home"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
tags: ["codemap", "navigation"]
---

# Home

This vault maps quieroVinilos at commit `40328f0a23ce3814ab62a9f0124a6ba1e6ae71be`, inspected on 2026-09-16 after authentication, email verification, catalog filters and single-exemplar sales. Local main matches origin/main at this revision. All documentation notes live in the root. The `Categories` folder contains property-filtered Bases, so one note can appear in several categories without being moved.

## Read the project in order

1. [[Project snapshot]] explains what exists and what does not.
2. [[Domain and identity]] explains accounts, catalog works, physical exemplars and inquiries.
3. [[Architecture]] explains the six modules and their boundaries.
4. [[Startup and dependency injection]] explains how the WAR becomes a running application.
5. [[Authentication flow]], [[Landing flow]], [[Publish flow]], [[Contact flow]], [[Inquiry and sale flow]] and [[Cover image flow]] trace the current routes through the layers with Mermaid diagrams and focused, source-linked code snippets. [[Legacy user flow]] records the removed scaffold.
6. [[UI components]] and [[UI styles and tokens]] cover the latest shared JSP components and styles.
7. [[Database schema]], [[Transactions and concurrency]], [[Validation and errors]], [[Views and assets]] and [[Mail delivery]] explain the shared mechanisms.
8. [[Testing and evidence]] and [[Known gaps and document drift]] show what the available evidence does and does not establish.

## Browse by category

![[Categories/Navigation.base]]

[[Categories/Architecture.base|Architecture]] · [[Categories/Domain.base|Domain]] · [[Categories/Web.base|Web]] · [[Categories/Services.base|Services]] · [[Categories/Persistence.base|Persistence]] · [[Categories/Flows.base|Flows]] · [[Categories/Operations.base|Operations]] · [[Categories/Testing.base|Testing]] · [[Categories/History.base|History]]

Use [[Source inventory]] to locate a file and its documentation. Code notes contain exact source, explanation, project-type references, reverse references and linked tests. Reference links describe static code references, not a complete dynamic call graph; flow notes explain execution order.

## Maintain the vault

[[Vault guide]] defines the category convention, search examples and update procedure. [[AGENTS]] is the agent entry point; `CLAUDE.md` is a symlink to it. [[Note template]] is a root-level starter for future notes.
