---
title: "Development tools"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
tags: ["codemap", "operations"]
sources: ["tools/paw_checks.py", "tools/git-hooks/pre-commit", "tools/setup_local_postgres.sh", "tools/seed_local_data.sh"]
---

# Development tools

The scripts support development and do not run during ordinary HTTP handling. Their text is reference material; no setup, seed or deployment command was executed for this documentation refresh.

## Deterministic checks

`python3 tools/paw_checks.py all` runs i18n and JSP checks only. i18n compares default, English/French and Spanish override keys. JSP checks selected opening/closing tag counts in views and tag files; it does not compile JSPs, verify binding or prove browser behavior. The file did not change in this range.

The agent-local .claude/scripts/paw_checks.py remains a separate older implementation with a Flyway check. It must not be described as identical to tools/paw_checks.py. The distinction is relevant to agent hooks that still invoke the old copy.

## Hooks

The versioned tools/git-hooks/pre-commit runs the main script's all command, not Maven tests. It is now committed with the executable bit, so `git config core.hooksPath tools/git-hooks` can use it directly. Presence of a hook file still does not prove the path is configured. The .claude/hooks/commit-gate.py agent hook invokes its own check copy and may fail open on its own errors or timeouts.

## Local database setup

The interactive tools/setup_local_postgres.sh targets Homebrew postgresql@18. It can start the service and create or alter the local role and database. It no longer loads database/users.sql and database/albums.sql or seeds an initial album: after confirmation it applies the canonical idempotent persistence/src/main/resources/schema.sql, verifies the connection and points to the separate seed script. Its literal development configuration is not evidence of the user's actual secrets or installed database state. It does not start Jetty.

## Local demo catalog

tools/seed_local_data.sh reads database/demo_posts.tsv, downloads the 24 declared covers from the Cover Art Archive with retries and a one-second pause, and validates MIME type, 5 MiB limit and SHA-256 before touching the database. It then builds a single psql transaction that loads tools/sql/demo-users.sql, database/seed_dev_posts.sql and one seed_demo_post call per row with base64-encoded text and image data, and ends with a DO block that verifies 24 unique posts, at least 200 artists and valid prices, statuses and images. It runs against the `paw-pg` container by default or a `DATABASE_URL`, and is idempotent by design. See [[Schema history and seeds]] for a likely conflict with the NOT NULL search_phrase columns.

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
