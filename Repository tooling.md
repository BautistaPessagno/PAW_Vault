---
title: "Repository tooling"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "operations"]
sources: [".agents/skills/README.md", ".agents/skills/bug/SKILL.md", ".agents/skills/corrector-eyes/SKILL.md", ".agents/skills/design/SKILL.md", ".agents/skills/enhancer/SKILL.md", ".agents/skills/feature-engineering/SKILL.md", ".agents/skills/feature-engineering/context.md", ".agents/skills/forensic-audit/SKILL.md", ".agents/skills/frontend-analyzer/SKILL.md", ".agents/skills/frontend-analyzer/context.md", ".agents/skills/frontend-analyzer/scripts/research.py", ".agents/skills/general-audit/SKILL.md", ".agents/skills/good-practice/SKILL.md", ".agents/skills/handoff/SKILL.md", ".agents/skills/i18n-sync/SKILL.md", ".agents/skills/implementation/SKILL.md", ".agents/skills/jdbc-to-jpa/SKILL.md", ".agents/skills/planning/SKILL.md", ".agents/skills/pre-delivery/SKILL.md", ".agents/skills/skillset-port/SKILL.md", ".agents/skills/smoke/SKILL.md", ".agents/skills/wiki-sync/SKILL.md", ".claude/hooks/commit-gate.py", ".claude/hooks/db-server-guard.py", ".claude/hooks/i18n-parity-posttool.py", ".claude/hooks/skill-autolaunch.py", ".claude/scripts/paw_checks.py", ".claude/skills/README.md", ".claude/skills/bug/SKILL.md", ".claude/skills/corrector-eyes/SKILL.md", ".claude/skills/design/SKILL.md", ".claude/skills/enhancer/SKILL.md", ".claude/skills/feature-engineering/SKILL.md", ".claude/skills/feature-engineering/context.md", ".claude/skills/forensic-audit/SKILL.md", ".claude/skills/frontend-analyzer/SKILL.md", ".claude/skills/frontend-analyzer/context.md", ".claude/skills/frontend-analyzer/scripts/research.py", ".claude/skills/general-audit/SKILL.md", ".claude/skills/good-practice/SKILL.md", ".claude/skills/handoff/SKILL.md", ".claude/skills/i18n-sync/SKILL.md", ".claude/skills/implementation/SKILL.md", ".claude/skills/jdbc-to-jpa/SKILL.md", ".claude/skills/planning/SKILL.md", ".claude/skills/pre-delivery/SKILL.md", ".claude/skills/skillset-port/SKILL.md", ".claude/skills/smoke/SKILL.md", ".claude/skills/wiki-sync/SKILL.md", ".codex/prompts/bug.md", ".codex/prompts/corrector-eyes.md", ".codex/prompts/design.md", ".codex/prompts/enhancer.md", ".codex/prompts/feature-engineering.md", ".codex/prompts/forensic-audit.md", ".codex/prompts/frontend-analyzer.md", ".codex/prompts/general-audit.md", ".codex/prompts/good-practice.md", ".codex/prompts/handoff.md", ".codex/prompts/i18n-sync.md", ".codex/prompts/implementation.md", ".codex/prompts/jdbc-to-jpa.md", ".codex/prompts/planning.md", ".codex/prompts/pre-delivery.md", ".codex/prompts/skillset-port.md", ".codex/prompts/smoke.md", ".codex/prompts/wiki-sync.md", ".gitignore", "AGENTS.md", "CLAUDE.md"]
---

# Repository tooling

The source repository carries agent instructions and workflow helpers alongside application code. They are not Maven modules and do not participate in request handling.

| Path family | Role |
|---|---|
| AGENTS.md and CLAUDE.md | Source-project conventions for its JDBC stage |
| .agents/skills | Agent-neutral workflow descriptions and supporting references/scripts |
| .claude/skills | Claude-facing copies of workflow packages |
| .codex/prompts | Prompt entry points for corresponding workflows |
| .claude/hooks | Commit gating, database/server guard, i18n post-tool check and skill auto-launch implementations |
| .claude/scripts/paw_checks.py | Older agent-local checker; still includes Flyway while tools/paw_checks.py now has only i18n/JSP |
| .gitignore | Excludes outputs, local credentials, logs, local hook settings and local plans |

The packages include bug, audits, design, feature engineering, i18n sync, implementation, JDBC-to-JPA planning, smoke and wiki sync. Their presence is tooling inventory, not evidence that a JPA migration or other feature has happened. [[Source inventory]] links every individual tracked tooling file. This map does not execute embedded task prompts or adopt their feature requests.

Hook activation depends on local configuration. .claude/settings.local.json is ignored, and the Git hook requires core.hooksPath activation; source presence alone does not prove either is active. [[Development tools]] explains the concrete check and wizard behavior.

The vault has its own [[AGENTS]] tailored to documentation maintenance, with a single CLAUDE.md symlink. It is separate from the source repository's existing pair and does not alter them. Local secrets, .git internals, compiled targets and ignored scratch state are intentionally outside the documentation body.
