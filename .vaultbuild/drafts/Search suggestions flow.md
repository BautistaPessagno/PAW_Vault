@title: Search suggestions flow
@categories: Flows, Web, Services, Persistence
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/dto/SearchSuggestionDto.java, webapp/src/main/java/ar/edu/itba/paw/webapp/dto/ArtistSuggestionDto.java, services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java, models/src/main/java/ar/edu/itba/paw/models/SearchSuggestion.java, models/src/main/java/ar/edu/itba/paw/models/SearchSuggestionType.java, persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java, webapp/src/main/webapp/js/autocomplete.js, webapp/src/main/webapp/WEB-INF/tags/input-control.tag, pom.xml

> [!summary] En una frase
> Dos endpoints devuelven JSON con hasta cinco sugerencias ordenadas por relevancia, y el navegador arma la lista con `textContent`, sin interpretar HTML.

## Qué resuelve

El autocompletado del buscador (álbumes y artistas) y el del campo "artista" al publicar. Es la observación 3 del sprint 2: antes el servidor devolvía HTML armado y el cliente lo inyectaba con `innerHTML`.

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| `@ResponseBody` + `produces = application/json` | El método devuelve datos, no una vista |
| Jackson (`jackson-databind` 2.15.2) | Con Jackson en el classpath, Spring MVC registra solo el conversor a JSON |
| DTOs en `webapp` | Los modelos de dominio no se serializan directo |
| `MessageSource` | La etiqueta "Álbum" o "Artista" traducida en el servidor |
| SQL con `UNION` y `CASE` | Ranking en la base |
| `fetch` + `createElement` + `textContent` | Cliente sin `innerHTML` |
| Atributos ARIA (`listbox`, `aria-activedescendant`) | Navegación con teclado y lector de pantalla |

## Contrato

```
GET /search/suggestions?q=...
[ { "value": "Kind of Blue", "type": "ALBUM",  "typeLabel": "Álbum",   "detail": "Miles Davis" },
  { "value": "Miles Davis",  "type": "ARTIST", "typeLabel": "Artista", "detail": null } ]

GET /artists/suggestions?q=...
[ { "value": "Miles Davis" } ]
```

Siempre `200 application/json`. Sin `q`, con `q` vacío o de más de 255 caracteres: `[]`. El ejemplo sale del issue del sprint 2; los campos coinciden con [[SearchSuggestionDto]] y [[ArtistSuggestionDto]].

## Recorrido paso a paso

1. La persona escribe. `autocomplete.js` espera un instante (`SEARCH_DELAY_MS`) antes de pedir y numera cada pedido: si llega la respuesta de uno viejo, la descarta.
2. `fetch(sourceUrl + '?q=' + encodeURIComponent(texto))`.
3. Controller → `PostService.findSearchSuggestions` o `ArtistService.findSuggestions`: normalizan con `SearchText.compact` y devuelven vacío si no queda nada.
4. DAO, una sola sentencia:
   - Buscador: `UNION` de artistas y álbumes que tengan al menos una publicación `AVAILABLE`.
   - Campo artista: todos los artistas del catálogo.
   - Filtro: `REPLACE(search_phrase, ' ', '') LIKE '%texto%'`.
   - Orden: 0 coincidencia exacta, 1 prefijo del texto completo, 2 prefijo de alguna palabra, 3 aparición en cualquier parte; después alfabético. `LIMIT 5`.
5. El controller convierte a DTO. `typeLabel` se resuelve con el `Locale` del request; `detail` es el artista cuando la sugerencia es un álbum.
6. El cliente lee `response.json()` y crea cada `<li>` con `createElement`, `textContent` y `setAttribute`. Un título con `<` o `&` se ve tal cual.
7. En el buscador, elegir una sugerencia envía el formulario (`submitOnSelect`).

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| JSON y no fragmentos HTML | JSP parcial + `innerHTML` (versión anterior) | Observación de la cátedra: el servidor devuelve datos y la interfaz los presenta | Issue del sprint 2 |
| DTO separado del modelo | Serializar `SearchSuggestion` | El contrato JSON no queda atado al dominio | Issue del sprint 2 |
| `typeLabel` en el servidor | Traducir en JavaScript | La traducción sigue en los bundles | Issue del sprint 2 |
| Ranking en SQL | Traer todo y ordenar en memoria (versión anterior) | No cargar la tabla entera por cada tecla | Comentario en [[PostJdbcDao]] |
| El `WHERE` es el caso más amplio del ranking | Un filtro por nivel | No descarta ninguna fila que el ranking pudiera puntuar | Comentario en [[PostJdbcDao]] |
| Buscador solo sugiere lo que tiene publicaciones disponibles | Todo el catálogo | Que la sugerencia lleve a resultados | SQL de [[PostJdbcDao]] |
| Límite de 255 en la query | Sin límite | Nada más largo puede coincidir | Comentario en [[PostServiceImpl]] |
| Jackson agregado solo en `webapp` | En todos los módulos | Es un detalle de presentación | `webapp/pom.xml` |

## Límites conocidos

- Las rutas son públicas y sin límite de frecuencia.
- El `LIKE` con comodín inicial no usa índice.
- `autocomplete.js` no tiene tests automáticos.

## Preguntas de defensa

**¿Qué devuelve el endpoint y por qué JSON?**
Una lista de objetos. Se cambió desde HTML porque así el servidor entrega datos reutilizables y el cliente no interpreta markup ajeno.

**¿Cómo se convierte la lista de Java a JSON?**
Con `@ResponseBody`, Spring busca un conversor para `application/json`; al estar Jackson en el classpath, lo registra automáticamente.

**¿Cómo evitan XSS en el desplegable?**
El cliente nunca usa `innerHTML`: todo texto entra por `textContent`.

**¿Cómo ordenan las sugerencias?**
Con un `CASE` en SQL: exacta, prefijo, prefijo de palabra, contiene.

## Evidencia de código

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/SearchSuggestionController.java:20-49}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ArtistSuggestionController.java:16-34}}

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:58-82}}

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java:197-203}}

{{code:services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:177-188}}
