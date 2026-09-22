---
title: "Home"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
tags: ["codemap", "navigation"]
---

# Home

This vault maps quieroVinilos at commit `f12af080cf6a27101160f005102a20f436574cf7`, inspected on 2026-09-22 after the post detail page, editing and deletion, pagination, the profile page, password change and recovery, search suggestions and the split inbox. All documentation notes live in the root. The `Categories` folder contains property-filtered Bases, so one note can appear in several categories without being moved.

## Read the project in order

1. [[Project snapshot]] explains what exists and what does not.
2. [[Domain and identity]] explains accounts, catalog works, physical exemplars and inquiries.
3. [[Architecture]] explains the six modules and their boundaries.
4. [[Startup and dependency injection]] explains how the WAR becomes a running application.
5. The flow notes trace the current routes through the layers with Mermaid diagrams and focused, source-linked code snippets:
    - Browsing: [[Landing flow]], [[Search suggestions flow]], [[Post detail flow]]
    - Selling: [[Publish flow]], [[Edit and delete flow]], [[Cover image flow]]
    - Buying: [[Contact flow]], [[Inquiry and sale flow]]
    - Accounts: [[Authentication flow]], [[Profile flow]], [[Password recovery flow]]
    - [[Legacy user flow]] records the removed scaffold.
6. [[UI components]] and [[UI styles and tokens]] cover the shared JSP components and styles; [[Views and assets]] covers pages and scripts.
7. [[Database schema]], [[Transactions and concurrency]], [[Paginated listings]], [[Validation and errors]] and [[Mail delivery]] explain the shared mechanisms.
8. [[Testing and evidence]] and [[Known gaps and document drift]] show what the available evidence does and does not establish.

## Browse by category

![[Categories/Navigation.base]]

[[Categories/Architecture.base|Architecture]] · [[Categories/Domain.base|Domain]] · [[Categories/Web.base|Web]] · [[Categories/Services.base|Services]] · [[Categories/Persistence.base|Persistence]] · [[Categories/Flows.base|Flows]] · [[Categories/Operations.base|Operations]] · [[Categories/Testing.base|Testing]] · [[Categories/History.base|History]]

Use [[Source inventory]] to locate a file and its documentation. Code notes contain exact source, explanation, project-type references, reverse references and linked tests. Reference links describe static code references, not a complete dynamic call graph; flow notes explain execution order.

## Maintain the vault

[[Vault guide]] defines the category convention, search examples and update procedure. [[AGENTS]] is the agent entry point; `CLAUDE.md` is a symlink to it. [[Note template]] is a root-level starter for future notes.

## Auditoría local anterior

[[Audit local 2026-09-17]] registra la carga de 27 publicaciones, sus imágenes, seis consultas y hallazgos de usabilidad sobre la rama ejecutada `e5e926d`, anterior a este mapa. [[Known gaps and document drift]] indica cuáles de esos hallazgos resuelve `f12af08`.
