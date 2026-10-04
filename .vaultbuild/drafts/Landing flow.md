@title: Landing flow
@categories: Flows, Web, Services, Persistence
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java, webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java, services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/Pagination.java, models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java, models/src/main/java/ar/edu/itba/paw/models/PostSort.java, models/src/main/java/ar/edu/itba/paw/models/SearchText.java, models/src/main/java/ar/edu/itba/paw/models/SearchResult.java, models/src/main/java/ar/edu/itba/paw/models/PostPage.java, models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java, persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, webapp/src/main/webapp/WEB-INF/views/landing/index.jsp, webapp/src/main/webapp/js/catalog.js

> [!summary] En una frase
> `GET /` es el catálogo: búsqueda por texto sin tildes ni mayúsculas, seis filtros, diez órdenes y páginas de 15, todo resuelto en dos consultas SQL con parámetros.

## Qué resuelve

El transversal de "queries no triviales": buscar, filtrar, ordenar y paginar las publicaciones disponibles. Incluye la observación 2 del sprint 2 (un solo estado vacío).

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| Formulario `GET` ligado a [[CatalogFilterForm]] | Los filtros viajan en la URL: se pueden compartir y volver atrás |
| `PropertyEditor` propio (`IgnoreInvalidEditor`) | Un valor de enum desconocido en la URL se ignora en vez de romper |
| Bean Validation + [[CatalogFilterValidator]] | Año y precios fuera de rango, rango invertido |
| [[SearchText]] | Normalizar lo que se teclea igual que lo que se guardó |
| Columnas `search_phrase` | Texto ya normalizado en la base, comparado con `LIKE` |
| `ESCAPE` en `LIKE` | Que `%` y `_` del usuario se busquen literalmente |
| `LIMIT ? OFFSET ?` + `COUNT(*)` | Paginación con total |
| [[Pagination]] | Aritmética de páginas y "página fuera de rango" |
| `catalog.js` | Enviar el orden al cambiar el `select` y plegar filtros en pantallas angostas |

## Recorrido paso a paso

1. `GET /?q=...&genre=...&condition=...&year=...&minPrice=...&maxPrice=...&sort=...&page=N`. Ruta pública.
2. **Binding.** `PostSort`, `Genre`, `Condition` y `Long` pasan por `IgnoreInvalidEditor`: si el texto no es un valor válido, el filtro queda sin pedir. Los `Integer` no usan ese editor: Spring conserva el valor rechazado para mostrar el error junto al campo.
3. **Validación.** Año entre 1000 y 9999 y no futuro; precios entre 1 y 99.999.999; mínimo no mayor que máximo.
4. El controller no decide nada: pasa los criterios y la página tal como llegaron. `PostService.search(criteria, page)`, transacción de solo lectura:
   - Texto de más de 255 caracteres → `InvalidSearchQueryException` (400): ningún título ni artista es más largo que su columna.
   - `SearchText.compact(query)`: minúsculas, sin diacríticos, sin separadores. "Soda Stéreo", "sodastereo" y "SODA-STEREO" buscan lo mismo.
   - `normalize(criteria)`: un filtro fuera de rango se ignora; un rango de precios invertido descarta los dos extremos.
   - `countSearch` y, si hay resultados, `search` con `LIMIT 15 OFFSET (page-1)*15`. Los dos usan **el mismo** `WHERE`.
   - `Pagination.offsetFor` lanza 404 si la página es menor que 1 o supera el total.
   - Devuelve [[SearchResult]] con los criterios **tal como se aplicaron**.
5. El controller arma el modelo con `result.getCriteria()`: el orden y los filtros que la vista marca como activos son los que el service aplicó, no los que llegaron en la URL. `returnQuery` es la query string codificada, para que la ficha pueda volver al mismo listado.
6. **Estado vacío.** Con texto o filtros y sin resultados: la página del disco, con un mensaje según el caso (solo texto, solo filtros, ambos) y las acciones "Quitar filtros" (conserva el texto) y "Nueva búsqueda". Sin texto ni filtros: "todavía no hay vinilos". Con errores de filtro: solo los errores.

## La consulta

El `WHERE` se arma agregando una cláusula por filtro presente y un parámetro por cláusula. Siempre incluye `p.status = 'AVAILABLE'`.

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:138-195}}

El orden nunca viene del usuario como texto: el enum [[PostSort]] elige entre diez `ORDER BY` fijos, todos desempatados por "más nuevo primero".

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:231-263}}

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| Columna `search_phrase` normalizada | `LOWER(...)`/`unaccent` en cada consulta | La normalización se hace una vez, en Java, con la misma función que normaliza la búsqueda | Comentario en [[SearchText]] |
| Comparar contra la forma sin espacios | Comparar palabras | Que "sodastereo" encuentre "Soda Stereo" | Comentario en [[SearchText]] |
| Misma normalización que las sugerencias | Dos reglas | "Lo que el autocompletado ofrece, la búsqueda lo encuentra" | Comentario en [[PostServiceImpl]] |
| Un solo `WHERE` para contar y listar | Dos métodos separados | Si divergen, la paginación promete páginas que no existen | Comentario en [[PostJdbcDao]] |
| `ORDER BY` desde un enum | Concatenar el parámetro | Al SQL nunca entra texto del usuario | Comentario en [[PostJdbcDao]] |
| Escapar `%` y `_` | Dejarlos pasar | Un `%` no puede traer todo el catálogo | Comentario en [[PostJdbcDao]] |
| Filtros inválidos se ignoran en el service | Error | Vienen de la URL: no cortan la búsqueda. El formulario sí muestra el error | Comentario en [[PostServiceImpl]] |
| El orden por defecto y la validación de página viven en el service | Resolverlos en el controller (versión anterior) | El controller quedó sin lógica: el PR #48 la movió y la vista muestra como activo solo lo que el service aplicó | Comentario en [[LandingController]]; commits `f918e28b`, `10ac1757` |
| Un solo estado vacío | Mensajes distintos por texto y por filtros | Observación 2 del sprint 2: "es el mismo resultado presentado de dos formas" | Issue del sprint 2 |
| Página 1 siempre existe | 404 si no hay resultados | Una búsqueda vacía no es un error | Comentario en [[Pagination]] |
| Solo se listan los `AVAILABLE` | Mostrar todo | "La landing solo lista lo que todavía se puede comprar" | Comentario en [[PostJdbcDao]] |
| Sin N+1 | Cargar álbum y artista por tarjeta | El resumen sale de un `JOIN` de cuatro tablas | SQL de [[PostJdbcDao]] |

## Cambios respecto de septiembre

- La búsqueda enviada ahora ignora tildes (antes solo las sugerencias).
- El contador muestra el total real: el service cuenta antes de listar, en lugar de pedir una fila de más.
- El estado vacío es uno solo.
- El controller ya no valida la página ni elige el orden por defecto (PR #48).
- El aviso de "agregaste el vinilo a tu carrito" aparece acá: agregar desde la ficha vuelve al listado de origen ([[Cart flow]]).

## Límites conocidos

- `LIKE '%texto%'` sobre `REPLACE(search_phrase, ' ', '')` no puede usar el índice de `search_phrase`: recorre la tabla. Con el volumen actual no es un problema medido.
- `artistId` se acepta como filtro pero ningún control lo ofrece.
- `OFFSET` grande recorre las filas anteriores.
- La paginación muestra anterior y siguiente, no el total de páginas.

## Preguntas de defensa

**¿Cómo buscan sin distinguir tildes ni mayúsculas?**
Al guardar un artista o un álbum se calcula `search_phrase` con `SearchText.phrase` (NFD, sin marcas diacríticas, minúsculas, separadores a un espacio). Al buscar se normaliza igual y se compara con `LIKE`.

**¿Cómo evitan inyección SQL si el `WHERE` es dinámico?**
Lo dinámico es qué cláusulas fijas se incluyen. Los valores siempre van como parámetros `?`, y el orden sale de un `switch` sobre un enum.

**¿Qué pasa si pido la página 9999, o la 0?**
404 en los dos casos: `Pagination.offsetFor`, en el service, rechaza una página menor que 1 o mayor que el total.

**¿Por qué los filtros van por `GET`?**
No cambian estado, y así la búsqueda queda en la URL: se puede compartir, guardar y volver con el botón atrás.

**¿Por qué cuentan antes de listar?**
Para mostrar el total y saber si la página pedida existe. Si el total es 0 no se ejecuta la segunda consulta.

## Evidencia de código

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java:44-120}}

{{code:services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:155-175}}

{{code:services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:208-225}}

{{code:models/src/main/java/ar/edu/itba/paw/models/SearchText.java:7-36}}

{{code:services/src/main/java/ar/edu/itba/paw/services/Pagination.java:3-35}}
