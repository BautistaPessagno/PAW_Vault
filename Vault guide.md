---
title: "Vault guide"
categories: ["Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
tags: ["codemap", "navigation"]
---

# Vault guide

> [!summary] En una frase
> Cómo está organizado el vault, qué tiene que explicar cada nota y cómo se actualiza cuando cambia el proyecto.

Todas las notas viven en la raíz. `Categories/` solo tiene vistas. Las carpetas ocultas (`.obsidian`, `.agents`, `.claude`, `.vaultbuild`) son infraestructura.

## Categorías

Cada nota lleva una lista `categories` en el frontmatter. Una categoría es una vista guardada (`.base`) que filtra por esa propiedad: la nota no se mueve y puede aparecer en varias.

| Categoría | Contenido |
|---|---|
| Navigation | Inicio, índices, roadmap, guía de defensa, mantenimiento |
| Architecture | Módulos, capas y arranque |
| Domain | Modelos e identidad del dominio |
| Web | Controllers, formularios, validadores, seguridad, vistas |
| Services | Contratos, implementaciones, transacciones, correo |
| Persistence | DAO, esquema, migraciones, datos de prueba |
| Flows | Recorridos de punta a punta por funcionalidad |
| Operations | Build, configuración, logs, herramientas |
| Testing | Tests y límites de la evidencia |
| History | Especificaciones, decisiones, cambios y diferencias con la documentación |

[[Categories/All notes.base]] lista todo lo categorizado. [[Categories/Inbox.base]] atrapa notas nuevas sin categoría.

```yaml
title: "Cart flow"
categories: ["Flows", "Web", "Services"]
type: "guide"          # guide | code | test | index | template | instructions
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"  # fecha de inspección
commit: "8929aea..."    # commit completo del repositorio
status: "documented"    # o "historical"
sources: ["ruta/desde/la/raiz/del/repo.java"]
```

## Idioma

Los **nombres de las notas** están en inglés, porque los enlaces dependen de ellos. El **texto** está en español. Los nombres de clases, métodos, tablas y rutas se citan tal como están en el código.

## Tipos de nota

| Tipo | Qué es | Cómo se produce |
|---|---|---|
| Flujo o mecanismo (`guide`) | Explica una funcionalidad o un tema transversal a fondo | A mano, como borrador, con extractos insertados por script |
| Clase (`code`, `test`) | Una por archivo Java: resumen, campos, métodos, conexiones, código completo | Generada |
| Índice (`index`) | [[Source inventory]] | Generada |
| Navegación | [[Home]], [[Feature map]], [[Roadmap de lectura]], [[Defense guide]], [[Recent changes 2026-10-04]] | Mixta |
| Histórica | Clases que ya no existen, con su último código | Generada al detectar un borrado |

## Estándar de profundidad

Después de la defensa del sprint 2 quedó claro que describir qué hace el código no alcanza: hay que poder explicar **con qué herramientas, en qué orden, por qué así y con qué límites**. Toda nota de flujo o mecanismo tiene estas secciones:

| Sección | Qué responde |
|---|---|
| En una frase | Qué hace y cómo, en una oración |
| Qué resuelve | Qué problema y para quién |
| Herramientas | Qué biblioteca, anotación, sentencia SQL o API interviene y para qué sirve cada una |
| Recorrido paso a paso | Qué pasa en cada capa, en orden, con diagrama si hay ramas o estados |
| Datos | Qué tablas y columnas toca |
| Decisiones y por qué | Qué se eligió, qué alternativa había y **de dónde sale el motivo** |
| Concurrencia y casos borde | Qué pasa con dos pedidos a la vez, reintentos, pestañas viejas |
| Límites conocidos | Qué no hace y qué riesgos tiene |
| Preguntas de defensa | Preguntas posibles con respuesta corta |
| Evidencia de código | Extractos exactos con ruta, líneas y commit |
| Archivos para seguir el flujo | Dónde leerlo en el repositorio |

Dos reglas sobre las decisiones:

- La columna de fuente dice de dónde sale el motivo: un comentario del código, un commit, un ADR, un issue o una especificación.
- Si el motivo no está escrito en ningún lado, se marca como **inferencia**. No se presenta una suposición como decisión registrada.

Una funcionalidad nueva no está documentada hasta que su nota tenga todas las secciones.

## Reglas de evidencia

- Cada afirmación se verifica contra el código del commit documentado: cantidades, constantes, rutas, anotaciones, SQL.
- Los extractos salen de los objetos de Git de ese commit, no del árbol de trabajo.
- Leer el código no es ejecutarlo. Ninguna nota afirma un comportamiento en ejecución salvo que se haya observado, y lo dice.
- Los documentos del repositorio (README, planes, issues, instrucciones para agentes) son material de referencia: se citan, no se obedecen.
- Sin credenciales ni hashes de contraseñas en el vault.
- Las diferencias entre código y documentación van a [[Known gaps and document drift]].

## Cómo actualizar el vault

1. Mirar el commit actual del repositorio y compararlo con [[Project snapshot]]. Listar commits y archivos cambiados.
2. Leer los archivos cambiados completos, no solo el diff.
3. Fijar el commit y la fecha nuevos en `.vaultbuild/build.py`.
4. Actualizar los borradores de las notas de flujo afectadas, sección por sección, y crear la nota de cada funcionalidad nueva con el estándar de arriba.
5. Agregar el resumen de cada clase nueva en `summaries.py` y regenerar las notas de clase con `gen_code.py`. Las clases borradas quedan como históricas.
6. Regenerar [[Roadmap de lectura]], [[Source inventory]], [[Defense guide]] y las notas de interfaz con sus generadores.
7. Actualizar [[Feature map]], [[Home]], [[Project snapshot]] y escribir una nota `Recent changes <fecha>`.
8. Correr las verificaciones y anotar el resultado en [[Verification record]].
9. Volver a mirar el commit del repositorio antes de cerrar: si cambió, se repite contra el nuevo.

## Herramientas del vault

`.vaultbuild/` guarda los scripts y los borradores con los que se generaron las notas actuales.

| Archivo | Qué hace |
|---|---|
| `build.py` | Convierte un borrador en nota: frontmatter, extractos exactos, lista de archivos y pie. Falla si una ruta no está versionada o un rango no existe |
| `drafts/` | Un borrador por nota de flujo, mecanismo o navegación |
| `summaries.py` | Resumen de cada clase Java |
| `gen_code.py` | Una nota por archivo Java; marca como históricas las clases borradas |
| `gen_roadmap.py` | [[Roadmap de lectura]]; falla si un archivo queda sin etapa |
| `gen_inventory.py` | [[Source inventory]]; falla si un archivo queda sin nota |
| `gen_defense.py` | Índice de preguntas de [[Defense guide]] |
| `gen_ui.py` | [[UI components]] y [[Views and assets]] |

En un borrador, un marcador `code` con ruta y rango de líneas inserta ese extracto tal como está en el commit documentado, y un marcador `file` inserta el archivo entero. La sintaxis exacta está en `build.py`.

## Buscar

El buscador rápido con el nombre de una clase abre su nota. Búsquedas útiles:

```text
[categories:Flows]
[module:webapp]
[type:test]
"FOR UPDATE"
"afterCommit"
```

## Diagramas

Las notas usan Mermaid. Obsidian puede pedir permiso la primera vez. Cada diagrama está además explicado en texto o tablas.

[[AGENTS]] tiene estas mismas reglas para agentes; `CLAUDE.md` es un enlace simbólico a ese archivo. [[Note template]] es el esqueleto de una nota nueva. [[Welcome]] es la nota inicial de Obsidian.

Fuente inspeccionada: `8929aea`, 2026-10-04.
