---
title: "Development tools"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "operations"]
sources: ["tools/paw_checks.py", "tools/git-hooks/pre-commit", "tools/setup_local_postgres.sh"]
---

# Development tools

The scripts support development and do not run during ordinary HTTP handling. Their text is reference material; no setup or deployment command was executed for this documentation refresh.

## Deterministic checks

`python3 tools/paw_checks.py all` now runs i18n and JSP checks only. The Flyway check and CLI option were removed alongside the old migration directory. i18n compares default, English/French and Spanish override keys. JSP checks selected opening/closing tag counts in views and tag files; it does not compile JSPs, verify binding, or prove browser behavior.

The agent-local .claude/scripts/paw_checks.py remains a separate older implementation with a Flyway check. It must not be described as identical to tools/paw_checks.py. The distinction is relevant to agent hooks that still invoke the old copy.

## Hooks

The versioned tools/git-hooks/pre-commit runs the main script’s all command, not Maven tests. Presence of a hook file does not prove core.hooksPath is configured. The .claude/hooks/commit-gate.py agent hook invokes its own check copy and may fail open on its own errors/timeouts. No hook activation was changed in this vault task.

## Local database setup

The interactive tools/setup_local_postgres.sh targets Homebrew postgresql@18. It can start the service, create or alter local roles/database, load the manual SQL for a fresh database and seed the initial album. It now stops on the unsupported textual albums.artist schema instead of applying a migration. The seed omits cover_path and leaves cover_image_id null.

Existing-table checks accept artist_id and an artists table; this does not verify every newer image/Post column. The script does not start Jetty and was not executed. Its literal development configuration is not evidence of the user’s actual secrets or installed database state.

## Check entry point excerpt

[tools/paw_checks.py, lines 101–135](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/paw_checks.py>)

```python
            self_closing = sum(1 for t in all_open if t.rstrip().endswith("/>"))
            opens = len(all_open) - self_closing
            closes = len(re.findall(rf"</{re.escape(tag)}\s*>", text))
            if opens != closes:
                rel = f.relative_to(PROJECT_ROOT)
                errors.append(f"jsp: {rel} — <{tag}> desbalanceado (aperturas={opens}, cierres={closes})")
    return errors


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    checks = {"i18n": check_i18n, "jsp": check_jsp}
    if what == "all":
        selected = list(checks.items())
    elif what in checks:
        selected = [(what, checks[what])]
    else:
        print(f"uso: paw_checks.py [{'|'.join(checks)}|all]")
        return 2
    errors = []
    for name, fn in selected:
        errs = fn()
        errors.extend(errs)
        if not errs:
            print(f"{name}: OK")
    if errors:
        print("\nPROBLEMAS ENCONTRADOS:")
        for e in errors:
            print(f"  - {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

[[Build and dependencies]] · [[Schema history and seeds]] · [[Repository tooling]]
