@title: Recent changes 2026-10-05
@categories: History, Navigation
@footer: yes

> [!summary] En una frase
> Entre el mapa anterior del vault (`8929aea`, 4 de octubre) y `c3e2a4c` (5 de octubre) entraron 14 pull requests y 60 commits: correcciones de seguridad y de bloqueos, precio fijado al aceptar, vuelta a la venta, conversación y reseñas por rol, quitar fotos con una X, filtros por estado y logs de publicación.

Los datos salen de `git log 8929aea..c3e2a4c` sobre el clon local. La copia de trabajo estaba en `1368153` (PR #57) y `origin/main` en `c3e2a4c`; el vault se generó desde los objetos de `c3e2a4c` y no se hizo `fetch` desde el vault.

## Resumen

| | |
|---|---|
| Commit anterior | `8929aeaa59b250e6c7119212f96437e153e815ac` (4 de octubre, merge del PR #48) |
| Commit actual | `c3e2a4cd23337bd35175d14ef551ba12a758a59d` (5 de octubre, merge del PR #62) |
| Commits | 60 en total, 39 sin contar merges |
| Archivos | 74 cambiados, 12 nuevos, ninguno borrado. Versionados: 472, de los cuales 238 son Java |
| Migraciones | Sin cambios: siguen V1–V11 |
| Tests | 550 casos (`@Test`): 257 en persistence, 293 en services (eran 504) |
| ADR | Nuevo: 0004, precio fijado al aceptar |

## Pull requests, en orden de merge

Todos se integraron el 5 de octubre: del #49 al #57 entre las 01:36 y las 01:41, y del #59 al #62 entre las 13:36 y las 13:37 (hora de Git, UTC).

| PR | Rama | Qué trajo | Nota |
|---|---|---|---|
| #49 | edutormakh1/fix-cart-covers | Las tapas del carrito vuelven a cargar desde `/post/{postId}/images/{id}` (`2eed2f76`) | [[Cart flow]] |
| #50 | edutormakh1/fix-profile-back-navigation | `origin` y `originPage` tolerantes en la ficha: un valor inválido ya no da 400 (`ca06676c`) | [[Post detail flow]] |
| #51 | edutormakh1/fix-post-service-authorization | Editar y eliminar exigen en el service ser el publicante o ADMIN (`563f7020`) | [[Edit and delete flow]], [[Security and authorization]] |
| #52 | edutormakh1/fix-cart-contact-lock-order | Agregar al carrito bloquea el post antes que la Cuenta (`e12c0e39`) | [[Cart flow]], [[Transactions and concurrency]] |
| #53 | edutormakh1/fix-receipt-immutability | [[Receipt]] copia sus bytes (`612391ea`) | [[Inquiry and sale flow]] |
| #55 | edutormakh1/sale-payment-return | Después de cargar los datos de cobro, el vendedor vuelve a la venta que quería aceptar (`25f95bc9`, `97f489b3`) | [[Addresses and payment flow]] |
| #56 | edutormakh1/sale-price-at-acceptance | El precio de la venta se fija al aceptar; ADR 0004 (`7e073053`) | [[Inquiry and sale flow]] |
| #58 | user-byline-tag | `user-byline.tag`: foto y nombre con enlace al perfil, también en las reseñas (`d6111f2d`) | [[UI components]] |
| #54 | edutormakh1/sale-conversation-ui | Página de la venta más compacta, `sale-detail.js`, foco del chat, cancelar la reseña sin JavaScript (`a88e7e20`, `bda29dcf`, `c1a3dacf`, `1d7b49e5`) | [[Conversation flow]], [[Reviews flow]] |
| #57 | edutormakh1/profile-role-reviews | Reseñas del perfil público separadas por rol y paginadas (`5d439ef4`, `f0e92d0b`) | [[Public profile flow]], [[Paginated listings]] |
| #59 | gallery-remove-x | Quitar fotos al editar con una X que atenúa la foto y se puede deshacer (`1cc8230e`, `b017d3dd`) | [[Gallery flow]] |
| #60 | tgorganchian/filtro-estado-consultas | Bandejas filtradas por estado con chips y conteos (`61c71cff`, `91d98f88`) | [[Status filters flow]] |
| #61 | tgorganchian/filtro-estado-publicaciones | "Mis publicaciones" filtrada por estado; el filtro se conserva al volver de la ficha (`ca9edde0`, `7d178376`) | [[Status filters flow]], [[Profile flow]] |
| #62 | tgorganchian/log-post-y-excepciones | Logs de publicar y editar; 400 para datos de post o de cobro inválidos; 38 tests renombrados a la convención (`c60be91e`, `1900a542`) | [[Logging]], [[Validation and errors]], [[Testing and evidence]] |

## Qué cambió, por tema

### Seguridad y consistencia

- La pertenencia de un post se vuelve a chequear en el service, con el id de quien actúa, además del `@PreAuthorize` (`563f7020`).
- Todas las operaciones que tocan post y Cuenta bloquean en el mismo orden: primero el post (`e12c0e39`).
- `Receipt` es inmutable de verdad (`612391ea`).
- `InvalidPostDataException` e `InvalidPaymentInfoException` tienen handler: 400 en lugar de 500 (`c60be91e`).

### Venta

- Mientras una consulta está `PENDING`, la bandeja y la página muestran el precio actual del post. Al aceptar, `startSale` copia ese precio y cambia el estado en un solo `UPDATE` (`7e073053`, ADR 0004).
- Aceptar sin datos de cobro lleva al perfil con `returnInquiryId`; guardar los datos vuelve a `/inquiries/{id}#sale-actions` (`25f95bc9`, `97f489b3`).
- La página de la venta junta resumen, conversación y reseña en una sola columna (`a88e7e20` y siguientes).

### Perfiles y reseñas

- El perfil público separa reseñas como vendedor y como comprador, con 10 por página y su propio parámetro `reviewPage` (`5d439ef4`).
- `rating.tag`, `review-content.tag` y `user-byline.tag` reemplazan el marcado repetido (`f0e92d0b`, `d6111f2d`).

### Listados

- Bandejas y "Mis publicaciones" se filtran por estado; los chips muestran cuántos elementos hay en cada uno y el filtro viaja en la paginación y en el regreso desde la ficha (`61c71cff`, `ca9edde0`, `7d178376`).

### Publicaciones

- La galería al editar usa una X por foto en lugar de una casilla con texto (`1cc8230e`, `b017d3dd`).
- Publicar y editar dejan un log INFO con ids (`c60be91e`).

### Tests

- 46 casos nuevos desde `8929aea`, entre ellos [[ReceiptTest]] e [[InquiryStatusFilterTest]].
- Todos los nombres siguen `test<Método>When<Condición>Returns<Resultado>` (`1900a542`).

## Archivos nuevos

| Archivo | Para qué |
|---|---|
| `docs/adr/0004-freeze-sale-price-at-acceptance.md` | Decisión de fijar el precio al aceptar |
| [[ReviewPage]], [[ReviewSubjectRole]] | Página de reseñas por rol |
| [[FilterCounts]], [[InquiryStatusFilter]] | Conteos y grupos de estados de los filtros |
| [[ReceiptTest]], [[InquiryStatusFilterTest]] | Tests nuevos |
| `rating.tag`, `review-content.tag`, `user-byline.tag`, `filter-chips.tag` | Componentes de la interfaz ([[UI components]]) |
| `js/sale-detail.js` | Comportamiento de la página de la venta ([[Views and assets]]) |

## Qué cambió en el vault

- Nota nueva: [[Status filters flow]], con dos diagramas.
- Diagramas Mermaid actualizados en [[Inquiry and sale flow]], [[Addresses and payment flow]], [[Public profile flow]], [[Edit and delete flow]], [[Cart flow]], [[Post detail flow]], [[Conversation flow]], [[Gallery flow]] y [[Publish flow]]; diagrama nuevo en [[Paginated listings]].
- El diagrama Mermaid pasó a ser obligatorio en toda nota de flujo ([[Vault guide]], [[Note template]], [[AGENTS]]).
- [[Known gaps and document drift]]: tres puntos resueltos (tapas del carrito, pertenencia en el service, 500 por datos inválidos) y un límite nuevo sobre logs antes del commit.

## Quién hizo qué

Commits sin contar merges, según el autor registrado en Git:

| Autor | Commits | Temas |
|---|---|---|
| Eduardo Tormakh | 27 | Correcciones de seguridad y bloqueos, vuelta a la venta, precio al aceptar, conversación, reseñas por rol |
| Tadeo Gorganchian | 10 | Filtros por estado, logs y 400, convención de nombres de tests, ajustes de la galería, la venta a la que vuelve el vendedor y tests de `startSale` |
| Bautista Pessagno | 2 | Byline de usuario, quitar fotos con una X |

## Qué queda abierto

Ver [[Known gaps and document drift]] y [[Sprint 2 defense review]]: siguen pendientes el tipo de dato del dinero y el plazo para el comprobante.
