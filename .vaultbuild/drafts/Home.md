@title: Home
@categories: Navigation
@tags: codemap, navigation
@footer: no

Este vault documenta quieroVinilos en el commit `c3e2a4cd23337bd35175d14ef551ba12a758a59d`, inspeccionado el 5 de octubre de 2026. Todas las notas viven en la raíz; la carpeta `Categories` solo tiene vistas filtradas, así que una nota puede aparecer en varias categorías sin moverse.

## Empezá por acá

| Si querés... | Abrí |
|---|---|
| Saber qué es el proyecto y qué versión está documentada | [[Project snapshot]] |
| Ver qué cambió desde el mapa anterior | [[Recent changes 2026-10-05]] (antes: [[Recent changes 2026-10-04]]) |
| Ubicar una funcionalidad, sus rutas y sus clases | [[Feature map]] |
| Leer todo el código en un orden que tenga sentido | [[Roadmap de lectura]] |
| Preparar una defensa | [[Defense guide]] |
| Ver qué se observó en la defensa del sprint 2 y cómo está hoy | [[Sprint 2 defense review]] |
| Saber qué falta o qué puede fallar | [[Known gaps and document drift]] |

## Fundamentos

1. [[Domain and identity]]: Cuenta, Álbum, Post, Consulta y sus estados.
2. [[Architecture]]: los seis módulos y por qué una capa no puede saltearse otra.
3. [[Startup and dependency injection]]: cómo el WAR se convierte en una aplicación andando.
4. [[Database schema]] y [[Schema history and seeds]]: tablas, restricciones y migraciones.

## Flujos por funcionalidad

Cada nota de flujo tiene la misma estructura: qué resuelve, herramientas, recorrido paso a paso con un diagrama Mermaid del flujo, datos, decisiones con su fuente, concurrencia, límites, preguntas de defensa y código.

| Área | Notas |
|---|---|
| Cuenta | [[Authentication flow]] · [[Tokens and email links]] · [[Password recovery flow]] · [[Profile flow]] · [[Public profile flow]] |
| Catálogo | [[Landing flow]] · [[Search suggestions flow]] · [[Post detail flow]] |
| Vender | [[Publish flow]] · [[Edit and delete flow]] · [[Cover image flow]] · [[Gallery flow]] |
| Comprar | [[Contact flow]] · [[Cart flow]] · [[Addresses and payment flow]] |
| Venta | [[Inquiry and sale flow]] · [[Conversation flow]] · [[Reviews flow]] |

## Mecanismos transversales

| Tema | Nota |
|---|---|
| Quién puede hacer qué | [[Security and authorization]] |
| Correo | [[Mail delivery]] |
| Transacciones y bloqueos | [[Transactions and concurrency]] |
| Validación y respuestas de error | [[Validation and errors]] |
| Paginación y filtros por estado | [[Paginated listings]] · [[Status filters flow]] |
| Idiomas | [[Localization]] |
| Interfaz | [[UI components]] · [[UI styles and tokens]] · [[Views and assets]] |

## Operación y evidencia

[[Build and dependencies]] · [[Configuration and running]] · [[Logging]] · [[Development tools]] · [[Repository tooling]] · [[Testing and evidence]] · [[History and specifications]]

## Notas de código

Hay una nota por cada una de las 238 clases Java, con su resumen, sus métodos, quién la usa, sus tests y el código completo. Se llega por el buscador rápido con el nombre de la clase, o por [[Source inventory]], que lista los 472 archivos versionados y dónde está documentado cada uno. Las referencias entre notas de código son estáticas; el orden de ejecución lo dan las notas de flujo.

## Categorías

![[Categories/Navigation.base]]

[[Categories/Architecture.base|Architecture]] · [[Categories/Domain.base|Domain]] · [[Categories/Web.base|Web]] · [[Categories/Services.base|Services]] · [[Categories/Persistence.base|Persistence]] · [[Categories/Flows.base|Flows]] · [[Categories/Operations.base|Operations]] · [[Categories/Testing.base|Testing]] · [[Categories/History.base|History]]

## Mantenimiento

[[Vault guide]] define las categorías, el estándar de profundidad de las notas y el procedimiento de actualización. [[AGENTS]] es la entrada para agentes; `CLAUDE.md` es un enlace simbólico a ese archivo. [[Verification record]] guarda qué se verificó en cada actualización. [[Note template]] es el punto de partida para una nota nueva.

## Material anterior

[[Audit local 2026-09-17]] registra una auditoría manual sobre una rama anterior. [[Legacy user flow]] describe el esqueleto inicial. [[TODO cambios]] son apuntes personales tomados después de la defensa del sprint 2.

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación.
