@title: Publish flow
@categories: Flows, Web, Services, Persistence
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/form/PublishForm.java, webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java, webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java, models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java, models/src/main/java/ar/edu/itba/paw/models/ImageRules.java, services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java, services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java, persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java, persistence/src/main/java/ar/edu/itba/paw/persistence/AlbumJdbcDao.java, persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java, webapp/src/main/webapp/WEB-INF/views/publish/index.jsp, webapp/src/main/webapp/js/publish-preview.js

> [!summary] En una frase
> Publicar es elegir o crear el artista y el álbum del catálogo compartido, guardar hasta cinco fotos y crear un Post propio con precio y estado; todo en una transacción y con un Post por álbum y por publicante.

## Qué resuelve

`GET` y `POST /publish`. Editar y eliminar están en [[Edit and delete flow]]; las fotos, en [[Gallery flow]] y [[Cover image flow]].

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| Spring MVC multipart (Commons FileUpload) | Formulario con archivos |
| Bean Validation + [[PublishFormValidator]] | Reglas de campo y reglas cruzadas (año de prensado no anterior al de lanzamiento) |
| [[VinylInputRules]] e [[ImageRules]] (en `models`) | Límites compartidos por formulario, vista, catálogo y service |
| Autocompletado de artista | `/artists/suggestions` en JSON ([[Search suggestions flow]]) |
| `publish-preview.js` | Vista previa de la tarjeta mientras se escribe |
| `@Transactional` | Artista, álbum, imágenes, post y galería juntos |
| Restricciones `UNIQUE` | Identidad de artista, de álbum y un Post por publicante y álbum |
| `Savepoint` JDBC | Recuperarse de una carrera al crear un artista sin perder la transacción |
| [[SearchText]] | Columna `search_phrase` para búsqueda sin tildes |

## Recorrido paso a paso

1. `GET /publish` exige `VERIFIED`. La vista recibe géneros, condiciones y los límites de año, precio y tipos de imagen.
2. `POST /publish` llega como multipart. `MultipartFilter` lo parsea antes de la seguridad para que el token CSRF sea legible. Si el request supera 26 MiB, [[MultipartExceptionHandlerFilter]] redirige a `/publish?coverTooLarge`.
3. Validación de [[PublishForm]]:
   - Título y artista obligatorios, hasta 255. Año de lanzamiento, género, precio y condición obligatorios. Zona hasta 100, descripción hasta 1000.
   - [[PublishFormValidator]]: años entre 1000 y 9999 y no futuros; precio entre 1 y 99.999.999; prensado no anterior al lanzamiento; hasta 5 fotos, cada una válida según [[ImageRules]].
4. `PostServiceImpl.publish`, en una transacción:
   - Repite las reglas numéricas (`requireValidPostData`) y el tope de fotos: un POST que saltee el formulario no entra.
   - `artistService.findOrCreate`: identidad = el nombre en minúsculas solo con letras y dígitos. "Soda Stereo" y "soda-stereo" son el mismo artista.
   - `albumService.findOrCreate`: identidad = artista, título en minúsculas y año.
   - Si el publicante ya tiene un Post de ese álbum, `DuplicatePostException`.
   - Crea las imágenes (cada una se valida de nuevo en `ImageService.create`).
   - Crea el Post con la primera foto como principal (`posts.image_id`) y estado `AVAILABLE`.
   - Si hay más fotos, `replaceGallery` las guarda en `post_images` con orden 1 a 4.
5. Errores traducidos:
   - `DuplicatePostKeyException` (la restricción `UNIQUE (user_id, album_id)` detectó una carrera) → `DuplicatePostException` → error global `publish.duplicate`.
   - Otra `DataIntegrityViolationException` (dos publicaciones simultáneas crearon el mismo álbum) → `ConcurrentPublishException` → `publish.concurrent`, que invita a reintentar.
6. Éxito: aviso flash `postCreated` y redirección a la ficha `/post/{id}`.

## Datos

| Tabla | Qué se escribe | Unicidad |
|---|---|---|
| `artists` | `name`, `normalized_name`, `search_phrase` | `normalized_name` |
| `albums` | `title`, `normalized_title`, `artist_id`, `release_year`, `genre`, `search_phrase` | `(artist_id, normalized_title, release_year)` (V4) |
| `images` | `content_type`, `data` | — |
| `posts` | Publicante, álbum, precio, descripción, condición, prensado, zona, `image_id`, `status` | `(user_id, album_id)` |
| `post_images` | Fotos adicionales con `display_order` | `(post_id, display_order)`, `image_id` |

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| Catálogo propio de artistas y álbumes | Consumir un catálogo externo | La aplicación se despliega sola y PostgreSQL es la fuente de verdad | ADR 0002 |
| Artista como entidad con identidad normalizada | Texto libre en cada Post | Reutilizar entre publicaciones y poder filtrar y sugerir | Issue `publicacion-albumes/01` |
| Un Post por publicante y álbum | Varios | Regla del glosario: "un mismo publicante no puede duplicarlo" | `CONTEXT.md` |
| Las fotos son del Post, no del álbum | Portada compartida en el álbum | "El álbum conserva solo datos factuales compartidos; las fotos del ejemplar pertenecen a la publicación" | Comentario en [[AlbumServiceImpl]] |
| Savepoint al crear el artista | Dejar fallar | PostgreSQL deja la transacción inutilizable tras una violación de unicidad; el savepoint permite releer al ganador | Comentario en [[ArtistJdbcDao]] |
| Sin savepoint para el álbum: se traduce a "reintentá" | Repetir el patrón | La transacción del otro ya hizo commit, así que reintentar funciona | Comentario en [[PostServiceImpl]] |
| Reglas en `models`, usadas en formulario y service | Solo en el formulario | Un POST armado a mano no puede saltearlas | Comentario en [[VinylInputRules]] |
| `created_at` lo pone la base | Enviarlo desde Java | "El `DEFAULT` de la base es el único reloj de publicación" | Comentario en [[PostJdbcDao]] |
| Título normalizado como columna | Índice sobre `LOWER(title)` | HSQLDB, que usan los tests, no admite índices sobre expresiones | Migración V4 |
| Listas de los `<select>` en la vista y no como `@ModelAttribute` de clase | Declararlas una vez | El redirect posterior arrastraría el modelo como query string | Comentario en [[PublishController]] |

## Concurrencia y casos borde

- Dos publicaciones simultáneas del mismo artista nuevo: una inserta; la otra recibe la violación, vuelve al savepoint y relee.
- Dos publicaciones simultáneas del mismo álbum nuevo: una recibe "reintentá"; al reintentar encuentra el álbum.
- Doble clic en "Publicar": la segunda choca contra `UNIQUE (user_id, album_id)` y ve "ya publicaste este álbum".
- Sin fotos: el Post queda sin imagen propia y la ficha usa la portada heredada del álbum si existe, o el placeholder.

## Límites conocidos

- La unicidad por publicante y álbum incluye los Posts vendidos: no se puede publicar un segundo ejemplar del mismo álbum.
- `stock` existe en la tabla y siempre vale 1.
- Las imágenes se guardan en la base como `BYTEA`, sin redimensionar.
- [[PostServiceImplTest]] y [[PostJdbcDaoTest]] cubren reglas y SQL; la ruta del savepoint contra PostgreSQL no tiene test automático.

## Preguntas de defensa

**¿Qué pasa si dos personas publican a la vez el mismo artista nuevo?**
La segunda recibe la violación de unicidad dentro de un savepoint, vuelve atrás solo hasta ahí y relee el artista que creó la primera.

**¿Por qué la validación está en el formulario y también en el service?**
El formulario da el error junto al campo. El service es la garantía: no asume que quien lo llama validó.

**¿Cómo deciden si dos artistas son el mismo?**
Por el nombre normalizado: minúsculas y solo letras y dígitos. El nombre que se muestra conserva lo que escribió quien lo cargó.

**¿Dónde quedan las fotos?**
En la tabla `images`. La primera va referenciada desde el Post; las demás, desde `post_images` con su orden.

## Evidencia de código

Controller:

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java:76-100}}

Service:

{{code:services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:237-268}}

Reglas repetidas en el service:

{{code:services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java:350-380}}

Savepoint del artista:

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/ArtistJdbcDao.java:72-95}}

Identidad del artista:

{{code:services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java:26-31}}

{{code:services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java:57-63}}

Validador del formulario:

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/validation/PublishFormValidator.java:14-50}}
