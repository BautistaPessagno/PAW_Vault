---
title: "Development tools"
categories: ["Operations"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["tools/paw_checks.py", "tools/git-hooks/pre-commit", "tools/setup_local_postgres.sh", "tools/seed_local_data.sh", "tools/sql/demo-users.sql", "database/seed_dev_posts.sql", "database/demo_posts.tsv"]
---

# Development tools

> [!summary] En una frase
> Tres chequeos automáticos atrapan antes del commit los errores que más veces rompieron la aplicación en ejecución (una key de i18n faltante, dos migraciones con el mismo número, un tag JSTL sin cerrar), y dos scripts preparan la base local.

## `tools/paw_checks.py`

```bash
python3 tools/paw_checks.py all      # los tres
python3 tools/paw_checks.py i18n     # uno solo: i18n | flyway | jsp
```

| Chequeo | Qué verifica | Qué error evita |
|---|---|---|
| `i18n` | Que toda key de `messages.properties` exista en `_en` y `_fr`, y que ningún bundle tenga keys que el por defecto no tiene | Un texto en español en una página en otro idioma, o una `JasperException` cuando la key no está en el bundle por defecto ([[Localization]]) |
| `flyway` | Que no haya dos migraciones con la misma versión | Flyway se niega a arrancar |
| `jsp` | Que `c:if`, `c:forEach`, `c:choose`, `c:when`, `c:otherwise` y `form:form` abran y cierren la misma cantidad de veces por archivo | Un `</c:if>` sobrante tras un merge es un error 500 |

El chequeo de JSP es una heurística por expresiones regulares sobre el fuente sin comentarios: cuenta aperturas y cierres, no valida el anidamiento.

## Hook de pre-commit

```bash
git config core.hooksPath tools/git-hooks   # una vez por clon
```

A partir de ahí, cada `git commit` corre `paw_checks.py all` y se cancela si algo falla. `git commit --no-verify` lo saltea. Si no encuentra Python, el hook también bloquea; solo deja pasar cuando el script de chequeos no existe.

## Scripts de base local

| Script | Qué hace | Qué no hace |
|---|---|---|
| `tools/setup_local_postgres.sh` | Guía interactiva para macOS con Homebrew: inicia el servicio, crea el rol y la base si faltan, verifica la conexión JDBC. Muestra el estado antes de cada cambio y conserva lo existente | No crea tablas (lo hace Flyway al arrancar), no carga datos, no levanta la aplicación |
| `tools/seed_local_data.sh` | Descarga las tapas de las publicaciones de demostración, valida su hash y carga artistas, álbumes y publicaciones en una única transacción | No toca el esquema |

Los datos que usa el segundo están en `database/seed_dev_posts.sql` y `database/demo_posts.tsv`; las cuentas de demostración, en `tools/sql/demo-users.sql` ([[Schema history and seeds]]).

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Un único script de chequeos para personas y agentes | El mismo control sin importar quién commitea | Comentario en `tools/git-hooks/pre-commit`, commit `c85705aa` |
| Chequear paridad de i18n | Las keys faltantes llegaban commiteadas y fallaban en ejecución | Docstring de `check_i18n` |
| Chequear versiones Flyway | Dos PR pueden tomar el mismo número | `CLAUDE.md` del repo |
| Datos de demostración fuera del classpath | Que ningún arranque los ejecute ni viajen en el WAR | Comentario en `tools/sql/demo-users.sql` |

## Qué no cubren

Los tres chequeos son estáticos. No compilan, no corren tests y no levantan la aplicación: para eso están `mvn clean test` y el arranque contra PostgreSQL, que hace quien desarrolla ([[Testing and evidence]]).

## Evidencia de código

### Chequeos

Fuente exacta en `8929aea`: [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>), líneas 1–154.

```python
#!/usr/bin/env python3
"""
paw_checks.py — chequeos determinísticos del proyecto (sin dependencias fuera de stdlib).

Uso: python3 tools/paw_checks.py [i18n|flyway|jsp|all]

Exit 0 = todo OK. Exit 1 = hay errores (detalle por stdout). Los WARNING no afectan el exit code.

(keys i18n incompletas → JasperException en runtime) y C7 (JSPs desbalanceados que
los tests HSQLDB no atrapan).
"""
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
I18N_DIR = PROJECT_ROOT / "webapp/src/main/resources/i18n"
VIEWS_DIR = PROJECT_ROOT / "webapp/src/main/webapp/WEB-INF/views"
TAGS_DIR = PROJECT_ROOT / "webapp/src/main/webapp/WEB-INF/tags"
MIGRATIONS_DIR = PROJECT_ROOT / "persistence/src/main/resources/db/migration"

MAX_LISTED_KEYS = 20


def parse_properties_keys(path):
    """Keys de un .properties, manejando comentarios y líneas de continuación (\\ final)."""
    keys = set()
    if not path.exists():
        return keys
    continuation = False
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if continuation:
            # esta línea es la cola de un valor multilínea, no una key
            continuation = _ends_with_odd_backslashes(raw)
            continue
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        m = re.match(r"([^=:\s]+)\s*[=:]", line)
        if m:
            keys.add(m.group(1))
        continuation = _ends_with_odd_backslashes(raw)
    return keys


def _ends_with_odd_backslashes(line):
    n = 0
    for ch in reversed(line.rstrip("\n")):
        if ch == "\\":
            n += 1
        else:
            break
    return n % 2 == 1


def check_i18n():
    """Paridad de bundles. Regla del equipo (CLAUDE.md): messages.properties es el
    default (es); _en y _fr deben tener TODAS sus keys; _es puede estar vacío (hereda).
    Una key presente solo en un bundle hijo tampoco sirve: los demás locales caen al default
    y no la encuentran → JasperException."""
    errors = []
    default = parse_properties_keys(I18N_DIR / "messages.properties")
    if not default:
        return ["i18n: no pude leer keys de messages.properties (¿path correcto? %s)" % I18N_DIR]
    for loc in ("en", "fr"):
        missing = default - parse_properties_keys(I18N_DIR / f"messages_{loc}.properties")
        if missing:
            listed = ", ".join(sorted(missing)[:MAX_LISTED_KEYS])
            extra = "" if len(missing) <= MAX_LISTED_KEYS else f" (+{len(missing) - MAX_LISTED_KEYS} más)"
            errors.append(f"i18n: messages_{loc}.properties — faltan {len(missing)} keys: {listed}{extra}")
    for loc in ("es", "en", "fr"):
        orphans = parse_properties_keys(I18N_DIR / f"messages_{loc}.properties") - default
        if orphans:
            listed = ", ".join(sorted(orphans)[:MAX_LISTED_KEYS])
            errors.append(
                f"i18n: messages_{loc}.properties — {len(orphans)} keys huérfanas (no están en el "
                f"default, los otros locales las resuelven a missing): {listed}"
            )
    return errors


def check_flyway():
    """Detecta versiones Flyway duplicadas en db/migration."""
    if not MIGRATIONS_DIR.exists():
        return [f"flyway: no existe {MIGRATIONS_DIR}"]
    versions = {}
    for path in MIGRATIONS_DIR.iterdir():
        match = re.match(r"V(\d+)__", path.name)
        if match:
            versions.setdefault(int(match.group(1)), []).append(path.name)
    errors = []
    for version, files in sorted(versions.items()):
        if len(files) > 1:
            errors.append(
                f"flyway: versión V{version} duplicada: {', '.join(sorted(files))} — la app no bootea"
            )
    return errors


# Tags de bloque cuyo balance de apertura/cierre chequeamos. Los self-closing (<c:if .../>)
# son válidos (p.ej. c:if con var) y se excluyen del conteo de aperturas.
BALANCED_TAGS = ("c:if", "c:forEach", "c:choose", "c:when", "c:otherwise", "form:form")


def check_jsp():
    """Balance de tags JSTL por archivo (el 500 real: </c:if> desbalanceado post-merge).
    Heurística por regex sobre el fuente sin comentarios JSP/HTML."""
    errors = []
    files = []
    for base in (VIEWS_DIR, TAGS_DIR):
        if base.exists():
            files.extend(base.rglob("*.jsp"))
            files.extend(base.rglob("*.tag"))
    for f in sorted(files):
        text = f.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<%--.*?--%>", "", text, flags=re.DOTALL)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        for tag in BALANCED_TAGS:
            all_open = re.findall(rf"<{re.escape(tag)}(?=[\s>/])[^>]*>", text)
            self_closing = sum(1 for t in all_open if t.rstrip().endswith("/>"))
            opens = len(all_open) - self_closing
            closes = len(re.findall(rf"</{re.escape(tag)}\s*>", text))
            if opens != closes:
                rel = f.relative_to(PROJECT_ROOT)
                errors.append(f"jsp: {rel} — <{tag}> desbalanceado (aperturas={opens}, cierres={closes})")
    return errors


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    checks = {"i18n": check_i18n, "flyway": check_flyway, "jsp": check_jsp}
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

### Hook

Fuente exacta en `8929aea`: [tools/git-hooks/pre-commit](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/git-hooks/pre-commit>), líneas 1–36.

```text
#!/usr/bin/env bash
# pre-commit hook de git — traducción agente-agnóstica del hook "commit-gate" de Claude Code.
# Corre los checks determinísticos del proyecto antes de cada commit, sin importar qué
# agente (o humano) esté commiteando.
#
# Activación (una vez, en el repo):
#   git config core.hooksPath tools/git-hooks
# Bypass puntual (equivalente a PAW_SKIP_SMOKE=1):
#   git commit --no-verify
set -uo pipefail

run_checks() {
    local check_script="$1"

    if command -v python3 >/dev/null 2>&1 && python3 --version >/dev/null 2>&1; then
        python3 "$check_script" all
    elif command -v python >/dev/null 2>&1 && python --version >/dev/null 2>&1; then
        python "$check_script" all
    else
        return 1
    fi
}

# Checker único para todos los agentes.
if [ -f "tools/paw_checks.py" ]; then
    if run_checks "tools/paw_checks.py"; then
        exit 0
    else
        echo ""
        echo "Commit bloqueado por los checks del proyecto (arreglá lo de arriba)."
        echo "  Para commitear igual (con autorización del equipo): git commit --no-verify"
        exit 1
    fi
fi
# Sin script de checks → no bloquear.
exit 0
```

## Archivos para seguir el flujo

- [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>)
- [tools/git-hooks/pre-commit](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/git-hooks/pre-commit>)
- [tools/setup_local_postgres.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/setup_local_postgres.sh>)
- [tools/seed_local_data.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/seed_local_data.sh>)
- [tools/sql/demo-users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/sql/demo-users.sql>)
- [database/seed_dev_posts.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/seed_dev_posts.sql>)
- [database/demo_posts.tsv](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/demo_posts.tsv>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
