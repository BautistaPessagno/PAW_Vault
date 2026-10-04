@title: Paginated listings
@categories: Web, Services, Persistence
@files: services/src/main/java/ar/edu/itba/paw/services/Pagination.java, models/src/main/java/ar/edu/itba/paw/models/PostPage.java, models/src/main/java/ar/edu/itba/paw/models/InquiryPage.java, models/src/main/java/ar/edu/itba/paw/models/SearchResult.java, services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java, persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java, webapp/src/main/webapp/WEB-INF/tags/pagination.tag

> [!summary] En una frase
> Todos los listados largos se paginan en la base con `LIMIT` y `OFFSET` después de un `COUNT`; el cálculo vive en una sola clase del módulo services y una página fuera de rango es un 404.

## Herramientas

| Herramienta | Para qué |
|---|---|
| `LIMIT ? OFFSET ?` | Traer solo las filas de la página |
| `SELECT COUNT(*)` con las mismas condiciones | Saber cuántas páginas hay |
| [[Pagination]] | Aritmética compartida: páginas necesarias y offset |
| [[PostPage]], [[InquiryPage]], [[SearchResult]] | Modelos que llevan los ítems junto con página actual y total |
| `pagination.tag` | Enlaces de página que conservan filtros y ancla |

## Qué se pagina y de a cuánto

| Listado | Tamaño | Dónde está la constante |
|---|---|---|
| Catálogo | 15 publicaciones | `PostServiceImpl.CATALOG_PAGE_SIZE` |
| Publicaciones del perfil privado y público | 15 | `PostServiceImpl.PROFILE_PAGE_SIZE` |
| Bandejas de consultas | 5 **publicaciones**, cada una con todas sus consultas | `InquiryServiceImpl.INBOX_PAGE_SIZE` |
| Reseñas del perfil público | Las 10 más recientes, sin páginas | `ReviewServiceImpl.RECENT_LIMIT` |
| Sugerencias | 5 | `SUGGESTION_LIMIT` |
| Mensajes de una conversación | Todos | |
| Carrito | Todos, con tope de 20 al agregar | `CartService.MAX_ITEMS` |

## Recorrido

1. El controller recibe `page` como `int` (por defecto 1) y lo pasa al service. No valida el rango: desde el PR #48 esa regla vive en el service.
2. El service hace el `COUNT`, calcula el total de páginas con `Pagination.pagesFor` y el offset con `Pagination.offsetFor`.
3. `offsetFor` lanza [[PageNotFoundException]] si la página es menor que 1, o mayor que el total cuando no es la primera. **La página 1 siempre existe**, aunque esté vacía.
4. El DAO ejecuta el `SELECT` con `LIMIT` y `OFFSET` ligados como parámetros.
5. El service devuelve un modelo de página; la JSP dibuja los ítems y `pagination.tag` arma los enlaces.
6. [[ErrorResponseAdvice]] convierte `PageNotFoundException` en un 404.

### La bandeja agrupa antes de paginar

Las bandejas no paginan consultas sino **grupos**: una publicación con todas sus consultas. [[InquiryJdbcDao]] cuenta con `COUNT(DISTINCT ...)` sobre la clave de grupo, trae las claves de la página con `GROUP BY ... ORDER BY ... LIMIT ? OFFSET ?` y después las consultas de esos grupos en otra sentencia con `IN (...)`. Así un grupo nunca queda partido entre dos páginas y no hay una consulta por grupo.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Paginar en la base | No traer a memoria filas que no se muestran | Requisito de la cátedra sobre consultas no triviales (`TODO.md`); inferencia |
| Una sola clase para la aritmética | Una única regla de "página fuera de rango" | Comentario en [[Pagination]] |
| La página 1 siempre es válida | Un listado vacío no es un error | Comentario en [[Pagination]] |
| Validar el rango en el service | La lógica de negocio no va en controllers | PR #48, commit `f918e28b` |
| Offset calculado en `long` | Un número de página enorme no desborda el `int` | Código de `offsetFor` |
| Agrupar la bandeja por publicación | El vendedor piensa en "las consultas de este vinilo" | `docs/specs/feature_perfil-consultas-ui_20260921.md` |
| Conservar filtros y orden en los enlaces | Cambiar de página no pierde la búsqueda | Commits `1312e5b7`, `3f3ea4e9` |

## Límites conocidos

- `OFFSET` recorre las filas salteadas: en páginas muy profundas es más lento que paginar por clave. Con el volumen del TP no se nota.
- Entre el `COUNT` y el `SELECT` puede entrar o salir una fila; la página puede mostrar un ítem de más o de menos respecto del total. Son lecturas, no afecta datos.
- Esto no es el patrón "1+1" de JPA: sigue siendo JDBC.

## Preguntas de defensa

**¿Cómo paginan?**
Con `COUNT` para el total y `LIMIT`/`OFFSET` para la página, los dos con las mismas condiciones. La aritmética está en una clase compartida.

**¿Qué pasa si pido la página 9999?**
El service lanza `PageNotFoundException` y la respuesta es un 404.

**¿Cómo paginan la bandeja si agrupa por publicación?**
Paginan los grupos: cuentan grupos distintos, traen las claves de la página y después las consultas de esos grupos en una sola sentencia.

**¿Dónde se valida el número de página?**
En el service. El controller solo lo recibe y lo pasa.

## Evidencia de código

### Aritmética

{{file:services/src/main/java/ar/edu/itba/paw/services/Pagination.java}}

### Página de grupos en la bandeja

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java:253-291}}
