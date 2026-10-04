---
title: "Landing flow"
categories: ["Flows", "Web", "Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/Pagination.java", "models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java", "models/src/main/java/ar/edu/itba/paw/models/PostSort.java", "models/src/main/java/ar/edu/itba/paw/models/SearchText.java", "models/src/main/java/ar/edu/itba/paw/models/SearchResult.java", "models/src/main/java/ar/edu/itba/paw/models/PostPage.java", "models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java", "webapp/src/main/webapp/WEB-INF/views/landing/index.jsp", "webapp/src/main/webapp/js/catalog.js"]
---

# Landing flow

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

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>), líneas 138–195.

```java
    @Override
    public List<PostSummary> search(final PostSearchCriteria criteria, final int limit, final int offset) {
        final List<Object> parameters = new ArrayList<>();
        final String where = searchWhere(criteria, parameters);
        parameters.add(limit);
        parameters.add(offset);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + where + "ORDER BY "
                + orderBy(criteria.getSort()) + " LIMIT ? OFFSET ?", ROW_MAPPER, parameters.toArray()));
    }

    @Override
    public int countSearch(final PostSearchCriteria criteria) {
        final List<Object> parameters = new ArrayList<>();
        final String where = searchWhere(criteria, parameters);
        return jdbcTemplate.queryForObject(COUNT_SELECT + where, Integer.class, parameters.toArray());
    }

    // Un solo WHERE para listar y contar: si divergen, la paginacion promete paginas que no existen.
    private static String searchWhere(final PostSearchCriteria criteria, final List<Object> parameters) {
        final List<String> clauses = new ArrayList<>();
        // Los vendidos no se ofrecen: la landing solo lista lo que todavia se puede comprar.
        clauses.add("p.status = ?");
        parameters.add(PostStatus.AVAILABLE.name());
        // La query llega normalizada con SearchText.compact, igual que en las sugerencias:
        // compara contra la misma columna para que las dos encuentren los mismos discos.
        if (criteria.getQuery() != null) {
            final String pattern = "%" + escapeLike(criteria.getQuery()) + "%";
            clauses.add("(REPLACE(a.search_phrase, ' ', '') LIKE ? " + LIKE_ESCAPE_CLAUSE
                    + " OR REPLACE(ar.search_phrase, ' ', '') LIKE ? " + LIKE_ESCAPE_CLAUSE + ")");
            parameters.add(pattern);
            parameters.add(pattern);
        }
        if (criteria.getGenre() != null) {
            clauses.add("a.genre = ?");
            parameters.add(criteria.getGenre().name());
        }
        if (criteria.getCondition() != null) {
            clauses.add("p.item_condition = ?");
            parameters.add(criteria.getCondition().name());
        }
        if (criteria.getArtistId() != null) {
            clauses.add("a.artist_id = ?");
            parameters.add(criteria.getArtistId());
        }
        if (criteria.getReleaseYear() != null) {
            clauses.add("a.release_year = ?");
            parameters.add(criteria.getReleaseYear());
        }
        if (criteria.getMinPrice() != null) {
            clauses.add("p.price >= ?");
            parameters.add(criteria.getMinPrice());
        }
        if (criteria.getMaxPrice() != null) {
            clauses.add("p.price <= ?");
            parameters.add(criteria.getMaxPrice());
        }
        return "WHERE " + String.join(" AND ", clauses) + " ";
    }
```

El orden nunca viene del usuario como texto: el enum [[PostSort]] elige entre diez `ORDER BY` fijos, todos desempatados por "más nuevo primero".

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>), líneas 231–263.

```java
    // Cada criterio mapea a un ORDER BY fijo: al SQL nunca entra texto del usuario.
    private static String orderBy(final PostSort sort) {
        switch (sort) {
            case OLDEST:
                return "p.created_at ASC, p.id ASC";
            case PRICE_ASC:
                return "p.price ASC, " + NEWEST_FIRST;
            case PRICE_DESC:
                return "p.price DESC, " + NEWEST_FIRST;
            case TITLE_ASC:
                return "LOWER(a.title) ASC, " + NEWEST_FIRST;
            case TITLE_DESC:
                return "LOWER(a.title) DESC, " + NEWEST_FIRST;
            case ARTIST_ASC:
                return "LOWER(ar.name) ASC, " + NEWEST_FIRST;
            case ARTIST_DESC:
                return "LOWER(ar.name) DESC, " + NEWEST_FIRST;
            case RELEASE_YEAR_ASC:
                return "a.release_year ASC, " + NEWEST_FIRST;
            case RELEASE_YEAR_DESC:
                return "a.release_year DESC, " + NEWEST_FIRST;
            case NEWEST:
            default:
                return NEWEST_FIRST;
        }
    }

    // Los comodines de LIKE que escriba el usuario se buscan literalmente: "%" no puede traer todo el catalogo.
    private static String escapeLike(final String value) {
        return value.replace(LIKE_ESCAPE, LIKE_ESCAPE + LIKE_ESCAPE)
                .replace("%", LIKE_ESCAPE + "%")
                .replace("_", LIKE_ESCAPE + "_");
    }
```

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

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>), líneas 44–120.

```java
    // Los valores cerrados o legacy que no se entienden se ignoran. Los Integer no usan
    // este editor: Spring conserva el valor rechazado para mostrar un error junto al campo.
    @InitBinder
    public void initBinder(final WebDataBinder binder) {
        binder.registerCustomEditor(PostSort.class, new IgnoreInvalidEditor(text -> PostSort.valueOf(upperCase(text))));
        binder.registerCustomEditor(Genre.class, new IgnoreInvalidEditor(text -> Genre.valueOf(upperCase(text))));
        binder.registerCustomEditor(Condition.class, new IgnoreInvalidEditor(text -> Condition.valueOf(upperCase(text))));
        binder.registerCustomEditor(Long.class, new IgnoreInvalidEditor(Long::valueOf));
    }

    private static String upperCase(final String text) {
        return text.toUpperCase(Locale.ROOT);
    }

    private static final class IgnoreInvalidEditor extends PropertyEditorSupport {

        private final Function<String, Object> parser;

        private IgnoreInvalidEditor(final Function<String, Object> parser) {
            this.parser = parser;
        }

        // valueOf tira IllegalArgumentException cuando el texto no es un valor valido,
        // y NumberFormatException la extiende: en los dos casos el filtro queda sin pedir.
        @Override
        public void setAsText(final String text) {
            try {
                setValue(parser.apply(text.trim()));
            } catch (final IllegalArgumentException e) {
                setValue(null);
            }
        }
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public ModelAndView landing(@Valid @ModelAttribute("catalogFilterForm") final CatalogFilterForm form,
                                final BindingResult bindingResult,
                                @RequestParam(value = "page", defaultValue = "1") final int pageNumber,
                                final HttpServletRequest request) {
        // Un filtro invalido no corta la busqueda: el service lo ignora y aplica el resto, incluida
        // la pagina. Lo que se muestra como activo es lo que el service aplico, no lo que llego.
        final SearchResult result = postService.search(form.toCriteria(), pageNumber);
        final PostSearchCriteria applied = result.getCriteria();
        final ModelAndView mav = new ModelAndView("landing/index");
        mav.addObject("query", result.getQuery());
        mav.addObject("total", result.getTotal());
        mav.addObject("sort", applied.getSort());
        mav.addObject("sorts", PostSort.values());
        mav.addObject("genres", Genre.values());
        mav.addObject("conditions", Condition.values());
        mav.addObject("selectedGenre", applied.getGenre());
        mav.addObject("selectedCondition", applied.getCondition());
        mav.addObject("selectedArtistId", applied.getArtistId());
        mav.addObject("selectedYear", applied.getReleaseYear());
        mav.addObject("minPrice", applied.getMinPrice());
        mav.addObject("maxPrice", applied.getMaxPrice());
        mav.addObject("catalogFilterErrors", bindingResult.hasErrors());
        mav.addObject("minimumYear", VinylInputRules.MIN_YEAR);
        mav.addObject("currentYear", VinylInputRules.currentYear());
        mav.addObject("minimumPrice", VinylInputRules.MIN_PRICE);
        mav.addObject("maximumPrice", VinylInputRules.MAX_PRICE);
        mav.addObject("posts", result.getPage().getPosts());
        mav.addObject("postPage", result.getPage());
        // Cada tarjeta lleva el listado de origen para que la ficha pueda volver a el
        // con la misma busqueda, filtros y pagina.
        final String listingQuery = request.getQueryString();
        mav.addObject("returnQuery", listingQuery == null ? null
                : URLEncoder.encode(listingQuery, StandardCharsets.UTF_8));
        return mav;
    }

    @ExceptionHandler(InvalidSearchQueryException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView invalidSearchQuery() {
        return new ModelAndView("error/400");
    }
}
```

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 155–175.

```java
    // Una busqueda vacia no filtra nada: se muestra lo mismo que la landing sin buscar,
    // pero respetando el orden pedido.
    @Override
    @Transactional(readOnly = true)
    public SearchResult search(final PostSearchCriteria criteria, final int pageNumber) {
        final String query = blankToNull(criteria.getQuery());
        if (query != null && query.length() > MAX_QUERY_LENGTH) {
            throw new InvalidSearchQueryException();
        }
        // Misma normalizacion que las sugerencias: lo que el autocompletado ofrece, la
        // busqueda lo encuentra. Una query sin letras ni digitos no coincide con nada.
        final String searchQuery = query == null ? null : SearchText.compact(query);
        final PostSearchCriteria normalized = normalize(criteria, searchQuery);
        final int total = searchQuery != null && searchQuery.isEmpty() ? 0 : postDao.countSearch(normalized);
        final int totalPages = Pagination.pagesFor(total, CATALOG_PAGE_SIZE);
        final int offset = Pagination.offsetFor(pageNumber, CATALOG_PAGE_SIZE, totalPages);
        final List<PostSummary> posts = total == 0
                ? List.of()
                : postDao.search(normalized, CATALOG_PAGE_SIZE, offset);
        return new SearchResult(query, normalized, new PostPage(posts, pageNumber, totalPages), total);
    }
```

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 208–225.

```java
    // Los filtros llegan de la URL, asi que pueden venir con cualquier valor. Uno fuera de
    // rango no corta la busqueda: se ignora y los demas se siguen aplicando. Sin orden
    // pedido, lo mas nuevo primero.
    private static PostSearchCriteria normalize(final PostSearchCriteria criteria, final String query) {
        final Long artistId = criteria.getArtistId() != null && criteria.getArtistId() > 0
                ? criteria.getArtistId() : null;
        final Integer releaseYear = validYearOrNull(criteria.getReleaseYear());
        final Integer minPrice = validPriceOrNull(criteria.getMinPrice());
        final Integer maxPrice = validPriceOrNull(criteria.getMaxPrice());
        // Un rango dado vuelta no deja pasar nada: se ignoran los dos extremos.
        final boolean invertedRange = !VinylInputRules.isPriceRangeOrdered(minPrice, maxPrice);
        return new PostSearchCriteria(query,
                criteria.getSort() == null ? PostSort.NEWEST : criteria.getSort(),
                criteria.getGenre(), criteria.getCondition(), artistId,
                releaseYear,
                invertedRange ? null : minPrice,
                invertedRange ? null : maxPrice);
    }
```

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/SearchText.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchText.java>), líneas 7–36.

```java
// Normalizacion compartida para busqueda: minusculas, sin diacriticos y con cada
// corrida de separadores reducida a un espacio. La usan los services para normalizar
// lo que teclea el usuario y el modulo persistence para llenar las columnas
// search_phrase. Si cambia la regla hay que reconstruir esas columnas, porque la
// comparacion se hace contra el valor ya guardado.
public final class SearchText {

    private static final Pattern DIACRITICS = Pattern.compile("\\p{M}+");
    private static final Pattern SEPARATORS = Pattern.compile("[^\\p{L}\\p{N}]+");

    private SearchText() {
    }

    // Forma con espacios: es la que se persiste y la que permite reconocer el
    // comienzo de cada palabra.
    public static String phrase(final String value) {
        if (value == null) {
            return "";
        }
        final String withoutDiacritics = DIACRITICS.matcher(
                Normalizer.normalize(value, Normalizer.Form.NFD)).replaceAll("");
        return SEPARATORS.matcher(withoutDiacritics.toLowerCase(Locale.ROOT)).replaceAll(" ").trim();
    }

    // Forma sin espacios: es contra la que se comparan las consultas, para que
    // "sodastereo" y "soda stereo" busquen lo mismo.
    public static String compact(final String value) {
        return phrase(value).replace(" ", "");
    }
}
```

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/Pagination.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>), líneas 3–35.

```java
// Aritmetica de paginado compartida por los services que listan de a paginas. Una sola
// regla para "pagina fuera de rango": la pagina 1 siempre existe, aunque este vacia; con el
// total conocido, cualquier otra tiene que caer dentro de el.
final class Pagination {

    private Pagination() {
    }

    // Paginas necesarias para un total; 0 cuando no hay filas.
    static int pagesFor(final int total, final int pageSize) {
        return (total + pageSize - 1) / pageSize;
    }

    // Offset de una pagina cuando el total es conocido.
    static int offsetFor(final int pageNumber, final int pageSize, final int totalPages) {
        if (pageNumber > 1 && pageNumber > totalPages) {
            throw new PageNotFoundException();
        }
        return offsetFor(pageNumber, pageSize);
    }

    // Offset de una pagina sin mirar el total: solo descarta numeros que no dan un offset valido.
    static int offsetFor(final int pageNumber, final int pageSize) {
        if (pageNumber < 1) {
            throw new PageNotFoundException();
        }
        final long offset = ((long) pageNumber - 1L) * pageSize;
        if (offset > Integer.MAX_VALUE) {
            throw new PageNotFoundException();
        }
        return (int) offset;
    }
}
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/LandingController.java>) · [[LandingController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/CatalogFilterForm.java>) · [[CatalogFilterForm]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/CatalogFilterValidator.java>) · [[CatalogFilterValidator]]
- [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>) · [[PostServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/Pagination.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/Pagination.java>) · [[Pagination]]
- [models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSearchCriteria.java>) · [[PostSearchCriteria]]
- [models/src/main/java/ar/edu/itba/paw/models/PostSort.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostSort.java>) · [[PostSort]]
- [models/src/main/java/ar/edu/itba/paw/models/SearchText.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchText.java>) · [[SearchText]]
- [models/src/main/java/ar/edu/itba/paw/models/SearchResult.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/SearchResult.java>) · [[SearchResult]]
- [models/src/main/java/ar/edu/itba/paw/models/PostPage.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostPage.java>) · [[PostPage]]
- [models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java>) · [[VinylInputRules]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>) · [[PostJdbcDao]]
- [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>)
- [webapp/src/main/webapp/js/catalog.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
