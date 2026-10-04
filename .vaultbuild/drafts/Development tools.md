@title: Development tools
@categories: Operations
@files: tools/paw_checks.py, tools/git-hooks/pre-commit, tools/setup_local_postgres.sh, tools/seed_local_data.sh, tools/sql/demo-users.sql, database/seed_dev_posts.sql, database/demo_posts.tsv

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

{{file:tools/paw_checks.py}}

### Hook

{{file:tools/git-hooks/pre-commit}}
