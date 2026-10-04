@title: Recent changes 2026-10-04
@categories: History, Navigation
@footer: yes

> [!summary] En una frase
> Entre el mapa anterior del vault (`f12af08`, 22 de septiembre) y `8929aea` (4 de octubre) entraron 13 pull requests y 112 commits: venta con comprobante, direcciones, Flyway, cuenta verificada, conversación, galería, avatares, perfiles públicos, reseñas, carrito y una limpieza que sacó la lógica de los controllers.

Los datos salen de `git log f12af08..8929aea` sobre el clon local. No se hizo `fetch` desde el vault: es el estado que tenía el repositorio en la máquina el 4 de octubre.

## Resumen

| | |
|---|---|
| Commit anterior | `f12af080cf6a27101160f005102a20f436574cf7` (22 de septiembre) |
| Commit actual | `8929aeaa59b250e6c7119212f96437e153e815ac` (4 de octubre, merge del PR #48) |
| Commits | 112 en total, 90 sin contar merges |
| Archivos versionados | 460, de los cuales 232 son Java |
| Migraciones | De un `schema.sql` a Flyway V1–V11 |
| Tests | 504 casos (`@Test`): 235 en persistence, 269 en services |

## Pull requests, en orden de merge

| PR | Fecha | Rama | Qué trajo | Nota |
|---|---|---|---|---|
| #35 | 23/09 | busqueda-y-filtros-catalogo | Filtros de precio y año validados, páginas numeradas con total, búsqueda con la misma normalización que las sugerencias, volver al listado de origen | [[Landing flow]] |
| #40 | 30/09 | venta-1-perfil | Datos de cobro (CBU y alias) y libreta de direcciones en el perfil | [[Addresses and payment flow]] |
| #44 | 30/09 | venta-2-direccion | Elegir dirección de envío al consultar; el vendedor ve solo ciudad y provincia hasta aceptar | [[Contact flow]] |
| #42 | 30/09 | payment-verification-flow | Venta con comprobante: reserva, comprobante, confirmación, cancelación, un correo por cambio de estado, precio congelado | [[Inquiry and sale flow]] |
| #38 | 30/09 | migracion-flyway | `schema.sql` reemplazado por migraciones Flyway | [[Database schema]] |
| #39 | 30/09 | porteo-skills | Procedimientos y hooks para agentes, chequeos unificados | [[Repository tooling]] |
| #43 | 02/10 | cuenta-verificada-observaciones-sprint-2 | Cuenta creada al registrarse y verificada después; sugerencias en JSON; un solo estado vacío; 403 y 404 centralizados; cierre de sesiones al cambiar la clave; freno al reenvío | [[Authentication flow]], [[Security and authorization]] |
| #45 | 02/10 | conversacion-consulta | Conversación dentro de cada consulta | [[Conversation flow]] |
| #46 | 04/10 | all-features-preview | Galería de hasta cinco fotos, avatares, perfiles públicos, reseñas, moderación de publicaciones por ADMIN, imágenes servidas desde su recurso | [[Gallery flow]], [[Public profile flow]], [[Reviews flow]] |
| #47 | 04/10 | carrito-consultas | Carrito para enviar varias consultas juntas | [[Cart flow]] |
| #48 | 04/10 | controller-logic-eradication | Tope de direcciones, orden por defecto y validación de página movidos a los services | [[Architecture]] |

Los PR #36 (`validaciones-centralizadas`, reglas de publicación compartidas) y #37 (`catalog-ui-polish`, paginación y errores de precio) se integraron el 23/09 dentro de la rama del #35 y no figuran como merge directo sobre `main`.

## Qué cambió, por tema

### Cuenta y seguridad

- El registro crea la cuenta con contraseña y deja la sesión iniciada; el correo se verifica después. Una cuenta sin verificar navega pero no opera (`0870c81d`).
- `users.enabled` pasó a llamarse `verified` (V6, `801f9aa1`).
- La verificación se exige por URL en [[SecurityConfig]]; la pertenencia de un recurso, con `@PreAuthorize` y los beans `postAccess`, `inquiryAccess` y `addressAccess` (`86b1f75d`).
- Cambiar o recuperar la contraseña cierra todas las sesiones de la cuenta, con `SessionRegistry` (`1350d001`).
- El reenvío del enlace de verificación tiene un freno de un minuto (`1350d001`).
- Se eliminó el panel `/admin`; ADMIN modera publicaciones disponibles (`60480b55`, `e462c468`).

### Catálogo y búsqueda

- Filtros combinables con validación, páginas numeradas, total de resultados (`3f3ea4e9`, `6aa48619`).
- Búsqueda enviada con la misma normalización de tildes que las sugerencias (`a4c39048`).
- Sugerencias de búsqueda y de artista en JSON (`bc8fd210`).
- Un único estado vacío para toda búsqueda sin resultados (`c16f1131`).
- Solo se muestran como activos los filtros que se aplicaron (`10ac1757`).

### Venta

- Estados nuevos: la consulta pasa por espera de pago y pago informado; la publicación puede estar reservada (`ae16dd63`, `e317537c`).
- Comprobante de pago: se sube, se descarga con nombre, se valida por tipo, tamaño y firma (`94aaa078`).
- Precio congelado en la consulta (`2aeee636`).
- Dirección de envío elegida al consultar; guardar dirección nueva y consulta en la misma transacción (`c747d4d4`, `af58cf4a`).
- Datos de cobro obligatorios para aceptar; hasta tres direcciones (`1f378fc2`).
- Un correo por cada cambio de estado (`7bae67b1`).
- Aceptar y rechazar autorizados con `@PreAuthorize`; la regla de cancelación pasó al modelo (`86b1f75d`).

### Conversación, reseñas y perfiles

- Mensajes dentro de la consulta, con aviso por correo; 409 al escribir en una conversación cerrada (`77f0d1e3`, `e0d1127d`).
- Reseñas entre comprador y vendedor tras una venta confirmada; borrado idempotente (`33508cd4`, `896130f9`).
- Perfil público con avatar, publicaciones y reseñas (`2ad3d8d4`).
- Foto de perfil desde un diálogo (`08627f5f`).

### Publicaciones e imágenes

- Galería de hasta cinco fotos al publicar y editar (`abf4cdbe`, `5fc0ec8f`).
- Validación de la firma de las imágenes subidas (`2d2603a7`).
- Las imágenes se sirven desde la ruta de su recurso: `/post/{id}/images/{id}`, `/users/{id}/avatar/{id}`, `/albums/{id}/cover/{id}` (`b30c8745`).
- Reglas de publicación centralizadas en [[VinylInputRules]] (`435733bc`).

### Carrito

- Agregar y quitar vinilos, tope de veinte, envío agrupado por publicante con un correo por cada uno (`93fce19d`, `0ce52cf8`).
- Lógica en [[CartServiceImpl]], regla de contacto unificada en [[ContactRules]], consultas creadas en lote (`0f9218f1`, `93058b58`).

### Infraestructura

- Flyway con V1–V11 y `baselineOnMigrate` (`a89e6d28`, `e4ac4915`).
- `tools/paw_checks.py` como chequeo único, con hook de pre-commit (`c85705aa`).

## Qué desapareció

| Archivo | Reemplazo |
|---|---|
| `persistence/.../schema.sql` | Migraciones Flyway |
| `AdminController`, `admin/index.jsp` | Sin reemplazo: el panel estaba vacío ([[AdminController]]) |
| `VerifyEmailForm` | La verificación ya no pide datos ([[VerifyEmailForm]]) |
| `InquiryAcceptedNotification`, `inquiry-accepted.html` | [[InquiryUpdateNotification]], `inquiry-update.html` |
| `artist/suggestions.jsp`, `search/suggestions.jsp` | Respuestas JSON |
| `ContactFormValidator`, `ValidContactForm` | [[ShippingAddressValidator]], [[ValidShippingAddress]] |
| `inquiries.message` (columna) | Tabla `inquiry_messages` |

## Quién hizo qué

Commits sin contar merges, según el autor registrado en Git:

| Autor | Commits | Temas |
|---|---|---|
| Lorenzo Méndez | 40 | Venta con comprobante, direcciones, datos de cobro, limpieza de controllers |
| Tadeo Gorganchian | 23 | Búsqueda y filtros, Flyway, herramientas, carrito |
| Eduardo Tormakh | 16 | Validaciones centralizadas, galería, avatares, perfiles públicos, reseñas, moderación |
| Bautista Pessagno | 11 | Cuenta verificada, observaciones del sprint 2, conversación, revisión del PR #46 |

## Qué queda abierto

Ver [[Known gaps and document drift]]. Lo más visible: las tapas del carrito apuntan a una ruta que ya no existe.
