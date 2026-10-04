@title: History and specifications
@categories: History
@files: CONTEXT.md, README.md, TODO.md, docs/setup.md, docs/adr/0001-establish-quiero-vinilos-domain.md, docs/adr/0002-own-the-album-catalog-locally.md, docs/adr/0003-conversation-inside-the-inquiry.md, docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md, docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md, docs/specs/feature_venta-con-comprobante_20260924.md, docs/plans/carrito-consultas.md

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
| 4 de octubre | Galería, avatares, perfiles públicos y reseñas (PR #46); carrito (PR #47); lógica fuera de los controllers (PR #48) |

El detalle por commit está en [[Recent changes 2026-10-04]].

## Notas históricas del vault

Las notas con `status: historical` conservan clases que ya no existen: [[HelloWorldController]], [[UserForm]], [[AlbumSummary]], [[EmailDeliveryException]], [[Legacy UserNotFoundException]], [[AdminController]], [[VerifyEmailForm]], [[InquiryAcceptedNotification]], [[ContactFormValidator]], [[ValidContactForm]]. [[Legacy user flow]] describe el esqueleto inicial y [[Audit local 2026-09-17]] registra una auditoría manual sobre una versión anterior.

## Evidencia de código

### ADR 0002

{{file:docs/adr/0002-own-the-album-catalog-locally.md}}

### ADR 0003

{{file:docs/adr/0003-conversation-inside-the-inquiry.md}}
