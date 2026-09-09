---
title: "Development tools"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "operations"]
sources: ["tools/paw_checks.py", "tools/git-hooks/pre-commit", "tools/setup_local_postgres.sh"]
---

# Development tools

These scripts support development and do not execute as part of an ordinary HTTP request.

## Deterministic checks

`python3 tools/paw_checks.py all` runs three checks. i18n compares property-key sets with the intentional Spanish fallback rule. flyway checks duplicate V-number filenames and warns when migrations have newer mtimes than the test schema. jsp compares opening/closing counts for selected JSTL/form tags after removing comments.

The Flyway check name does not imply an installed migration runner. Its timestamp comparison does not prove schema equivalence. The JSP check does not compile JSPs, verify nesting or detect every escaping issue. The parser is a project heuristic, not a full properties/XML parser.

## Commit hooks

`tools/git-hooks/pre-commit` can be activated by the repository's core.hooksPath configuration. It finds the check script and runs `all` using Python 3 or Python. It blocks when that check fails, but it does not run Maven tests. If no script exists it exits successfully. The source AGENTS claim that the pre-commit forces both checks and Maven is therefore stronger than the hook implementation.

`.claude/hooks/commit-gate.py` is a separate agent-tool hook that checks git commit commands and invokes `.claude/scripts/paw_checks.py`. Its own parse/runtime failures and timeout fail open. Presence on disk does not prove a hook is registered or active; local hook registration is ignored by Git.

## Local database wizard

`tools/setup_local_postgres.sh` is an interactive five-stage Bash helper targeting Homebrew postgresql@18. It checks commands, starts PostgreSQL if needed, previews and may create/reset the local role/database, loads schema or the artist migration, seeds the initial album when needed, then verifies selected tables.

It contains a hardcoded local-development password and outdated text saying WebConfig uses fixed credentials. Current WebConfig reads property files. The helper can change roles and database ownership. It was inspected as source and not executed for this map. Its existing-table branch does not migrate historical posts.publisher_email to current posts.user_id, and the last table-count check only covers users/artists/albums. It is not proof that a current Post schema is ready.

## Source entry points

- [tools/paw_checks.py](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/paw_checks.py>)
- [tools/git-hooks/pre-commit](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/git-hooks/pre-commit>)
- [tools/setup_local_postgres.sh](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/setup_local_postgres.sh>)

[[Build and dependencies]] · [[Schema history and seeds]] · [[Repository tooling]]
