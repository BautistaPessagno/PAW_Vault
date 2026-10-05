---
title: "History and specifications"
categories: ["History"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["CONTEXT.md", "README.md", "TODO.md", "docs/setup.md", "docs/adr/0001-establish-quiero-vinilos-domain.md", "docs/adr/0002-own-the-album-catalog-locally.md", "docs/adr/0003-conversation-inside-the-inquiry.md", "docs/adr/0004-freeze-sale-price-at-acceptance.md", "docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md", "docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md", "docs/specs/feature_venta-con-comprobante_20260924.md", "docs/plans/carrito-consultas.md"]
---

# History and specifications

> [!summary] En una frase
> El repositorio guarda, junto al código, el glosario del dominio, tres decisiones de arquitectura, las especificaciones y planes de cada funcionalidad y los issues que las originaron; son la fuente del **por qué** de muchas decisiones que el código solo muestra como resultado.

Estos documentos son material de referencia. Describen intenciones de un momento; cuando difieren del código, manda el código ([[Known gaps and document drift]]).

## Dónde buscar cada cosa

| Pregunta | Documento |
|---|---|
| ¿Qué significa un término del dominio? | `CONTEXT.md` |
| ¿Por qué se tomó una decisión estructural? | `docs/adr/` |
| ¿Qué tenía que hacer una funcionalidad? | `docs/specs/` |
| ¿Cómo se planeó implementarla, paso a paso? | `docs/plans/` |
| ¿Qué problema o pedido la originó? | `docs/issues/` |
| ¿Cómo se instala y corre? | `README.md`, `docs/setup.md` |
| ¿Qué reglas sigue el equipo al programar? | `CLAUDE.md` ([[Repository tooling]]) |

## Glosario: `CONTEXT.md`

Define el lenguaje del proyecto y qué palabras evitar. Los términos que más importan para leer el código:

| Término | Significado | En el código |
|---|---|---|
| Álbum | La obra, identificada por título, artista y año | [[Album]] |
| Post | La publicación que vincula a un publicante con un álbum | [[Post]] |
| Cuenta | La identidad registrada: correo, contraseña y rol | [[User]] |
| Cuenta verificada | La Cuenta que demostró controlar su correo | `users.verified`, autoridad `VERIFIED` |
| Publicante | La Cuenta como autora de un Post | `posts.user_id` |
| Consulta | El pedido de un comprador sobre un Post; la venta es una etapa suya | [[Inquiry]] |
| Conversación | Los mensajes dentro de una Consulta | [[Message]] |

El glosario distingue **Cambio de contraseña** (con sesión, probando la actual) de **Recuperación de contraseña** (sin sesión, por enlace): son dos operaciones con reglas distintas ([[Profile flow]], [[Password recovery flow]]).

## Decisiones de arquitectura (ADR)

| ADR | Decisión | Consecuencia en el código |
|---|---|---|
| 0001 | El producto es quieroVinilos, un marketplace de vinilos usados entre particulares; el lenguaje sale de `CONTEXT.md` y las restricciones técnicas, de la cursada | Nombres de modelos, tablas y textos |
| 0002 | El catálogo de álbumes es propio, sin depender de un servicio externo | [[Artist]] y [[Album]] se crean al publicar, con `findOrCreate` ([[Publish flow]]) |
| 0003 | Comprador y publicante hablan dentro de la Consulta | Una conversación por consulta, sin tiempo real, sin `Reply-To` en los correos ([[Conversation flow]], [[Mail delivery]]) |
| 0004 | El precio de la venta se fija al aceptar la Consulta, no al crearla | Mientras está `PENDING` la bandeja muestra el precio actual del post; `startSale` lo copia al aceptar ([[Inquiry and sale flow]]) |

## Especificaciones y planes

| Funcionalidad | Especificación | Plan | Nota del vault |
|---|---|---|---|
| Portada | `docs/specs/landing-quiero-vinilos.md` | | [[Landing flow]] |
| Publicación de álbumes | `feature_publicacion-albumes_20260904.md` | | [[Publish flow]] |
| Contacto con el publicante | `feature_contacto-post_20260904.md` | | [[Contact flow]] |
| Cambio de contraseña | `feature_cambio-contrasena_20260920.md` | | [[Profile flow]] |
| Perfil, consultas y ficha | `feature_perfil-consultas-ui_20260921.md` | `docs/plans/perfil-consultas-ui.md` | [[Profile flow]], [[Post detail flow]] |
| Venta con comprobante | `feature_venta-con-comprobante_20260924.md` | `docs/plans/venta-con-comprobante.md` | [[Inquiry and sale flow]] |
| Carrito | | `docs/plans/carrito-consultas.md` | [[Cart flow]] |
| Entrega intermedia | | `docs/plans/entrega-intermedia/02` a `06` | Configuración, autenticación, venta, filtros |

## Issues

| Carpeta | Tema |
|---|---|
| `docs/issues/01` a `03` | Primera portada con catálogo fijo. Superados |
| `publicacion-albumes/` | Artista como entidad, publicar un álbum nuevo, reutilizar catálogo, rechazar duplicados |
| `publicacion-mailing/` | Contactar al publicante; recuperarse de un fallo de entrega |
| `selling-flow/` | Seguimiento de consultas, venta de ejemplar único, aviso al comprador |
| `conversacion-consulta/` | Conversación dentro de la consulta |
| `observaciones-sprint-2/` | Las cuatro observaciones de la cátedra |

### Las observaciones del sprint 2

El issue `observaciones-sprint-2/01` recoge cuatro de las observaciones de la defensa y cómo se resolvieron. La lista completa, con lo que quedó pendiente, está en [[Sprint 2 defense review]]. Es la referencia para entender por qué cambió el registro:

| Observación | Qué se cambió | Dónde leerlo |
|---|---|---|
| El registro estaba al revés: pedía verificar el correo antes de crear la cuenta | La cuenta se crea al registrarse, queda con sesión iniciada y se verifica después. Sin verificar puede navegar pero no operar | [[Authentication flow]] |
| Había más de una pantalla para "sin resultados" | Un único estado vacío para toda búsqueda | [[Landing flow]] |
| Las sugerencias devolvían HTML que se insertaba con `innerHTML` | Devuelven JSON y el cliente arma los nodos | [[Search suggestions flow]] |
| La autorización estaba repartida entre capas sin un criterio | Reglas por URL para la verificación; `@PreAuthorize` para la pertenencia; 403 y 404 centralizados | [[Security and authorization]] |

## Línea de tiempo

| Fecha | Hito |
|---|---|
| 21 de agosto | Primer commit del esqueleto |
| 9 de septiembre | Cierre de la primera iteración (`TODO.md`): portada, publicación, contacto por correo |
| Hasta el 22 de septiembre | Autenticación, perfil, cambio y recuperación de contraseña, sugerencias, bandejas. Es el estado que describía el mapa anterior del vault (`f12af08`) |
| 23 de septiembre | Búsqueda y filtros del catálogo (PR #35) |
| 24 al 30 de septiembre | Venta con comprobante, direcciones, datos de cobro (PR #40, #44, #42); Flyway (PR #38) |
| 2 de octubre | Cuenta verificada y observaciones del sprint 2 (PR #43); conversación (PR #45) |
| 4 de octubre | Galería, avatares, perfiles públicos y reseñas (PR #46); carrito (PR #47); lógica fuera de los controllers (PR #48). Es el estado del mapa anterior del vault (`8929aea`) |
| 5 de octubre | Correcciones: tapas del carrito, regreso al perfil, autorización en el service, orden de bloqueos y comprobante inmutable (PR #49 a #53); volver a la venta y precio fijado al aceptar (PR #55, #56, ADR 0004), conversación y reseñas por rol (PR #54, #57, #58); quitar fotos con una X, filtros por estado en bandejas y publicaciones, logs y 400 de datos inválidos (PR #59 a #62) |

El detalle por commit está en [[Recent changes 2026-10-05]] (desde `8929aea`) y [[Recent changes 2026-10-04]] (desde `f12af08`).

## Notas históricas del vault

Las notas con `status: historical` conservan clases que ya no existen: [[HelloWorldController]], [[UserForm]], [[AlbumSummary]], [[EmailDeliveryException]], [[Legacy UserNotFoundException]], [[AdminController]], [[VerifyEmailForm]], [[InquiryAcceptedNotification]], [[ContactFormValidator]], [[ValidContactForm]]. [[Legacy user flow]] describe el esqueleto inicial y [[Audit local 2026-09-17]] registra una auditoría manual sobre una versión anterior.

## Evidencia de código

### ADR 0002

Fuente exacta en `c3e2a4c`: [docs/adr/0002-own-the-album-catalog-locally.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>), líneas 1–3.

```markdown
# Own the album catalog locally

quieroVinilos stores its album catalog and cover assets inside this project instead of consuming VinylOS or another external catalog. This keeps the application independently deployable and makes PostgreSQL the source of truth, at the cost of maintaining its own seed data and artwork.
```

### ADR 0003

Fuente exacta en `c3e2a4c`: [docs/adr/0003-conversation-inside-the-inquiry.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0003-conversation-inside-the-inquiry.md>), líneas 1–3.

```markdown
# Keep buyer and publisher talking inside the Inquiry

Earlier specs (`feature_contacto-post`, `entrega-intermedia/06-selling-flow`) kept in-app replies out of scope and let the publisher answer by email through the inquiry mail's `Reply-To`. We now give every Inquiry exactly one Conversation of immutable Messages, refreshed by reload with one notification email per Message, and drop the `Reply-To` so neither party learns the other's email and the Conversation is the single record of what was agreed. We rejected a pre-purchase thread per Post (a second aggregate with its own access rules and inbox) and real-time delivery (WebSocket/polling infrastructure not justified for this stage).
```

### ADR 0004

Fuente exacta en `c3e2a4c`: [docs/adr/0004-freeze-sale-price-at-acceptance.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0004-freeze-sale-price-at-acceptance.md>), líneas 1–11.

```markdown
# Freeze the sale price when the seller accepts

A pending inquiry follows the current publication price, including inbox summaries.
Its initial snapshot remains a fallback if the publication disappears. Acceptance
locks the publication and writes that locked price together with the transition
from PENDING to AWAITING_PAYMENT in one conditional update. Reservation and this
transition share the service transaction: a failed transition rolls both back.

After acceptance, all sale states retain the agreed snapshot. Existing accepted
sales are not rewritten; legacy rows without a snapshot keep their previous
publication fallback. No schema change is required.
```

## Archivos para seguir el flujo

- [CONTEXT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/CONTEXT.md>)
- [README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/README.md>)
- [TODO.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/TODO.md>)
- [docs/setup.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/setup.md>)
- [docs/adr/0001-establish-quiero-vinilos-domain.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0001-establish-quiero-vinilos-domain.md>)
- [docs/adr/0002-own-the-album-catalog-locally.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>)
- [docs/adr/0003-conversation-inside-the-inquiry.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0003-conversation-inside-the-inquiry.md>)
- [docs/adr/0004-freeze-sale-price-at-acceptance.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0004-freeze-sale-price-at-acceptance.md>)
- [docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md>)
- [docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md>)
- [docs/specs/feature_venta-con-comprobante_20260924.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_venta-con-comprobante_20260924.md>)
- [docs/plans/carrito-consultas.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/carrito-consultas.md>)

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
