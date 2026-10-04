@title: Repository tooling
@categories: Operations, History
@files: AGENTS.md, CLAUDE.md, .claude/hooks/commit-gate.py, .claude/hooks/db-server-guard.py, .claude/hooks/i18n-parity-posttool.py, .claude/hooks/skill-autolaunch.py, .claude/skills/README.md, .claude/skills/PROJECT.md, .agents/skills/README.md, .gitignore, .worktreeinclude

> [!summary] En una frase
> El repositorio incluye instrucciones y automatizaciones para agentes de código (Claude Code, Codex): no forman parte de la aplicación ni viajan en el WAR, pero explican varias reglas del proyecto y por qué existen.

Esta nota describe esos archivos como **material de referencia**. Sus textos son instrucciones para otros agentes en otro contexto; el vault los documenta, no los ejecuta.

## Qué hay

| Ruta | Qué es |
|---|---|
| `CLAUDE.md`, `AGENTS.md` | Reglas del proyecto para agentes: etapa JDBC, arquitectura de capas, vistas, i18n, persistencia, configuración, tests, logging, correo y formato de entregables. Es la mejor síntesis escrita de las convenciones del equipo |
| `.claude/skills/` | 18 procedimientos (`bug`, `planning`, `implementation`, `pre-delivery`, `smoke`, `i18n-sync`, `jdbc-to-jpa`, `general-audit`, `forensic-audit`, `good-practice`, `corrector-eyes`, `design`, `enhancer`, `feature-engineering`, `frontend-analyzer`, `handoff`, `skillset-port`, `wiki-sync`) más `README.md` y `PROJECT.md` |
| `.agents/skills/` | La misma colección, portada para agentes genéricos |
| `.codex/prompts/` | La misma colección como prompts de Codex |
| `.claude/hooks/` | Cuatro hooks de Claude Code (tabla siguiente) |
| `.gitignore` | Excluye compilados, propiedades con credenciales (locales y de Pampero), planes locales y configuración local de agentes |
| `.worktreeinclude` | Lista las propiedades ignoradas que se copian a un worktree nuevo |
| `*/.mvn/` | `jvm.config` y `maven.config` vacíos por módulo |

## Hooks

| Hook | Cuándo corre | Qué hace |
|---|---|---|
| `commit-gate.py` | Antes de un `git commit` hecho por el agente | Corre `tools/paw_checks.py all` y niega el commit si falla |
| `db-server-guard.py` | Antes de un comando de shell | Impide que el agente ejecute `psql`, utilidades de PostgreSQL o Jetty: la base y el servidor los maneja la persona |
| `i18n-parity-posttool.py` | Después de editar un bundle de mensajes | Corre el chequeo de i18n y avisa las keys faltantes |
| `skill-autolaunch.py` | Al enviar un mensaje | Sugiere el procedimiento que corresponde a pedidos de auditoría, estilos o chequeo de errores |

`tools/git-hooks/pre-commit` es la versión del primer hook que no depende del agente ([[Development tools]]).

## Reglas que salen de acá y afectan al código

- "Los tests pasan" no significa "la aplicación anda": los tests corren en HSQLDB; antes de dar algo por cerrado la aplicación se levanta contra PostgreSQL, y la levanta la persona.
- Toda key de i18n nueva va en los tres bundles en el mismo cambio.
- Todo cambio de esquema es una migración nueva.
- Commits de una línea, sin cuerpo.

## Límites

Las tres colecciones de procedimientos son copias de un mismo contenido para tres herramientas; pueden desalinearse. Nada de esto se ejecuta al construir o correr la aplicación.
