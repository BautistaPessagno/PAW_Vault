---
title: "Cover image flow"
categories: ["Flows", "Web", "Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java", "models/src/main/java/ar/edu/itba/paw/models/ImageRules.java", "models/src/main/java/ar/edu/itba/paw/models/Image.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java", "services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java", "persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java", "webapp/src/main/webapp/WEB-INF/web.xml"]
---

# Cover image flow

> [!summary] En una frase
> Las imágenes se guardan como bytes en la tabla `images`, se validan por firma al subir y se sirven siempre a través del recurso al que pertenecen, con caché de un año.

## Qué resuelve

El transversal de "manejo de imágenes": subida, validación, almacenamiento y entrega de fotos de publicaciones, portadas heredadas y fotos de perfil.

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| Commons FileUpload (`CommonsMultipartResolver`) | Parsear `multipart/form-data` |
| `MultipartFilter` | Parsear antes de Spring Security para leer el token CSRF |
| [[MultipartExceptionHandlerFilter]] | Convertir "archivo demasiado grande" en una redirección con aviso |
| [[ImageRules]] | Tipos, tamaño y firma |
| PostgreSQL `BYTEA` | Almacenamiento |
| `ResponseEntity<byte[]>` + `Cache-Control` | Entrega |

## Subida

1. El formulario declara `enctype="multipart/form-data"`.
2. `MultipartFilter` usa el bean `multipartResolver`: tope del request `MAX_MULTIPART_BYTES` (26 MiB), UTF-8 y resolución perezosa.
3. Si el request excede el tope, la excepción salta al leer las partes y [[MultipartExceptionHandlerFilter]] la atrapa (mirando también la causa, porque puede venir envuelta) y redirige: al formulario de publicar o editar con `?coverTooLarge`, a la venta con `?receiptTooLarge`, o al perfil con `?avatarTooLarge`.
4. El validador del formulario llama a `ImageFiles.isValid`: mira el tamaño antes de leer los bytes y después aplica [[ImageRules]].
5. El controller convierte a [[ImageUpload]] y el service llama a `ImageService.create`, que normaliza el tipo, valida **de nuevo** y guarda. Un rechazo se loguea como `WARN` con tipo y tamaño.

Reglas: PNG, JPEG o WEBP; el tipo que declara el navegador tiene que coincidir con los primeros bytes del archivo; entre 1 byte y 5 MiB.

## Entrega

| URL | Qué exige el SQL |
|---|---|
| `/post/{postId}/images/{imageId}` | Que la imagen sea la principal del post, la portada de su álbum o una de su galería |
| `/users/{userId}/avatar/{imageId}` | Que sea el avatar vigente de esa Cuenta y que esté verificada |
| `/albums/{albumId}/cover/{imageId}` | Que sea la portada de ese álbum |

Respuesta: el `Content-Type` guardado y `Cache-Control: max-age` de 365 días, público. Si no hay coincidencia, 404 sin cuerpo.

Las tres rutas son públicas. Lo que protege no es la sesión sino la pertenencia: no existe una URL `/images/{id}` que permita recorrer ids.

## Borrado

`ImageDao.delete` es un `DELETE` con cuatro `NOT EXISTS`: solo borra si ningún álbum, post, galería ni Cuenta referencia la imagen. Por eso el orden importa: primero se quita la referencia, después se pide el borrado.

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| Imágenes en la base | Sistema de archivos del servidor | El servidor de la cátedra solo recibe un WAR; la base es el único almacenamiento persistente | Inferencia; ADR 0002 habla de mantener catálogo y arte dentro del proyecto |
| Validar la firma y no solo el tipo declarado | Confiar en `Content-Type` | "El tipo declarado tiene que coincidir con la firma del contenido: no alcanza la extensión" | Comentario en [[ImageRules]]; commit `2d2603a7` |
| Servir desde el recurso asociado | `/images/{id}` | Que no se puedan enumerar imágenes ajenas ni huérfanas | Commit `b30c8745` |
| Caché de un año | Sin caché | "Una imagen nunca cambia una vez guardada": cambiar la foto crea otro id | Comentario en [[ImageController]] |
| Resolución multipart perezosa | Parseo inmediato | Que el exceso de tamaño se pueda traducir en un filtro externo | Comentario en [[WebConfig]] |
| Commons FileUpload y no el multipart de Servlet 3 | `StandardServletMultipartResolver` | "Se conserva como resolver multipart de esta entrega" | Comentario en [[WebConfig]] |
| Validar en formulario y en service | Un solo lugar | Error junto al campo, y garantía aunque se saltee el formulario | Comentario en [[ImageFiles]] |
| Borrado condicional | Borrado directo | La tabla es compartida por posts, álbumes y avatares | SQL de [[ImageJdbcDao]] |
| Portada del álbum heredada, sin escritura nueva | Seguir escribiéndola | Las fotos son del ejemplar; `cover_image_id` queda como dato viejo que el `COALESCE` todavía lee | Comentario en [[AlbumJdbcDao]] |

## Límites conocidos

- Cada imagen se lee entera en memoria para servirla; no hay `ETag` ni respuestas parciales.
- No se redimensiona ni se quitan metadatos.
- La validación mira la firma, no decodifica la imagen: un archivo con cabecera válida y contenido corrupto se acepta.
- Con caché pública de un año, una imagen que deja de ser accesible puede seguir en cachés intermedios.

## Preguntas de defensa

**¿Dónde guardan las imágenes?**
En PostgreSQL, columna `BYTEA` de la tabla `images`, con su tipo.

**¿Cómo validan que sea una imagen?**
Comparando los primeros bytes con la firma del formato declarado: `89 50 4E 47...` para PNG, `FF D8 FF` para JPEG, `RIFF....WEBP` para WEBP.

**¿Qué pasa si subo algo de 100 MB?**
El resolver corta el request; un filtro propio atrapa la excepción y redirige al formulario con un aviso, en lugar de un error 500.

**¿Por qué el filtro multipart va antes que el de seguridad?**
Porque en un formulario multipart el token CSRF viaja dentro del cuerpo. Si no se parsea antes, el filtro CSRF no lo encuentra.

**¿Puedo ver cualquier imagen cambiando el id?**
No: la consulta exige que esa imagen pertenezca al post, usuario o álbum de la misma URL.

## Evidencia de código

Reglas:

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>), líneas 9–77.

```java
public final class ImageRules {

    public static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;
    public static final int MAX_GALLERY_IMAGES = 5;
    public static final long MAX_MULTIPART_BYTES = (long) MAX_IMAGE_BYTES * MAX_GALLERY_IMAGES + 1024 * 1024;

    // El tipo declarado tiene que coincidir con la firma del contenido: no alcanza la extension.
    private enum Format {
        PNG("image/png") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, (byte) 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A);
            }
        },
        JPEG("image/jpeg") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, (byte) 0xFF, (byte) 0xD8, (byte) 0xFF);
            }
        },
        WEBP("image/webp") {
            @Override
            boolean matches(final byte[] data) {
                return startsWith(data, 0, 'R', 'I', 'F', 'F') && startsWith(data, 8, 'W', 'E', 'B', 'P');
            }
        };

        private final String contentType;

        Format(final String contentType) {
            this.contentType = contentType;
        }

        abstract boolean matches(byte[] data);
    }

    // Lista para el atributo accept de los input file.
    public static final String ACCEPTED_CONTENT_TYPES = Arrays.stream(Format.values())
            .map(format -> format.contentType).collect(Collectors.joining(","));

    private ImageRules() {
    }

    // Unico lugar que normaliza: lo que se guarda es igual a lo que se valido.
    public static String normalizeContentType(final String contentType) {
        return contentType == null ? null : contentType.trim().toLowerCase(Locale.ROOT);
    }

    // Espera el tipo ya normalizado.
    public static boolean isValid(final String contentType, final byte[] data) {
        if (contentType == null || data == null || data.length == 0 || data.length > MAX_IMAGE_BYTES) {
            return false;
        }
        return Arrays.stream(Format.values())
                .anyMatch(format -> format.contentType.equals(contentType) && format.matches(data));
    }

    private static boolean startsWith(final byte[] data, final int offset, final int... signature) {
        if (data.length < offset + signature.length) {
            return false;
        }
        for (int index = 0; index < signature.length; index++) {
            if (data[offset + index] != (byte) signature[index]) {
                return false;
            }
        }
        return true;
    }
}
```

Guardado:

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>), líneas 48–65.

```java
    @Override
    @Transactional
    public Image create(final String contentType, final byte[] data) {
        final String normalizedType = ImageRules.normalizeContentType(contentType);
        if (!ImageRules.isValid(normalizedType, data)) {
            LOGGER.warn("Rejected image contentType={} bytes={}", normalizedType, data == null ? 0 : data.length);
            throw new InvalidImageException();
        }
        final Image image = imageDao.create(normalizedType, data);
        LOGGER.info("Stored image {} ({}, {} bytes)", image.getId(), image.getContentType(), data.length);
        return image;
    }

    @Override
    @Transactional
    public boolean delete(final long id) {
        return imageDao.delete(id);
    }
```

Entrega:

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>), líneas 20–62.

```java
@Controller
public class ImageController {

    // Una imagen nunca cambia una vez guardada, asi que el navegador puede cachearla por id.
    private static final long CACHE_DAYS = 365;

    private final ImageService imageService;

    @Autowired
    public ImageController(final ImageService imageService) {
        this.imageService = imageService;
    }

    @RequestMapping(value = "/post/{postId:\\d+}/images/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> postImage(@PathVariable("postId") final long postId,
                                           @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findPostImage(postId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    @RequestMapping(value = "/users/{userId:\\d+}/avatar/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> userAvatar(@PathVariable("userId") final long userId,
                                            @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findUserAvatar(userId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    @RequestMapping(value = "/albums/{albumId:\\d+}/cover/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> albumCover(@PathVariable("albumId") final long albumId,
                                            @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findAlbumCover(albumId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    private static ResponseEntity<byte[]> imageResponse(final Image image) {
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(image.getContentType()))
                .cacheControl(CacheControl.maxAge(CACHE_DAYS, TimeUnit.DAYS).cachePublic())
                .body(image.getData());
    }

    @ExceptionHandler(ImageNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public void imageNotFound() {
    }
}
```

Pertenencia y borrado condicional:

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>), líneas 47–87.

```java
    @Override
    public Optional<Image> findPostImage(final long postId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM posts p JOIN albums a ON a.id = p.album_id WHERE p.id = ? "
                        + "AND (p.image_id = i.id OR a.cover_image_id = i.id OR EXISTS ("
                        + "SELECT 1 FROM post_images pi WHERE pi.post_id = p.id AND pi.image_id = i.id)))",
                ROW_MAPPER, imageId, postId).stream().findFirst();
    }

    @Override
    public Optional<Image> findUserAvatar(final long userId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM users u WHERE u.id = ? AND u.verified = TRUE AND u.avatar_image_id = i.id)",
                ROW_MAPPER, imageId, userId).stream().findFirst();
    }

    @Override
    public Optional<Image> findAlbumCover(final long albumId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM albums a WHERE a.id = ? AND a.cover_image_id = i.id)",
                ROW_MAPPER, imageId, albumId).stream().findFirst();
    }

    @Override
    public Image create(final String contentType, final byte[] data) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("content_type", contentType);
        parameters.put("data", data);
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new Image(id.longValue(), contentType, data);
    }

    @Override
    public boolean delete(final long id) {
        return jdbcTemplate.update("DELETE FROM images WHERE id = ? " +
                        "AND NOT EXISTS (SELECT 1 FROM albums WHERE cover_image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM posts WHERE image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM post_images WHERE image_id = images.id) " +
                        "AND NOT EXISTS (SELECT 1 FROM users WHERE avatar_image_id = images.id)", id) == 1;
    }
}
```

Resolver:

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>), líneas 115–127.

```java
  /*
   * Se conserva Commons FileUpload como resolver multipart de esta entrega. El nombre
   * del bean es obligatorio: DispatcherServlet lo busca como "multipartResolver".
   */
  @Bean
  public MultipartResolver multipartResolver() {
    final CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
    multipartResolver.setMaxUploadSize(ImageRules.MAX_MULTIPART_BYTES);
    multipartResolver.setDefaultEncoding(StandardCharsets.UTF_8.name());
    // El filtro multipart externo traduce el limite excedido antes de entrar al controller.
    multipartResolver.setResolveLazily(true);
    return multipartResolver;
  }
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>) · [[ImageController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/ImageFiles.java>) · [[ImageFiles]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>) · [[MultipartExceptionHandlerFilter]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/WebConfig.java>) · [[WebConfig]]
- [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>) · [[ImageRules]]
- [models/src/main/java/ar/edu/itba/paw/models/Image.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Image.java>) · [[Image]]
- [services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>) · [[ImageServiceImpl]]
- [services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/ImageService.java>) · [[ImageService]]
- [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/ImageDao.java>) · [[ImageDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>) · [[ImageJdbcDao]]
- [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
