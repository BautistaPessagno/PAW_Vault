---
title: "Known gaps and document drift"
categories: ["History", "Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/webapp/WEB-INF/views/cart/index.jsp", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java", "models/src/main/java/ar/edu/itba/paw/models/ImageRules.java", "models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java", "README.md", "TODO.md"]
---

# Known gaps and document drift

> [!summary] En una frase
> Lista de lo que el código no hace, hace distinto de lo que dice su documentación, o podría fallar; todo sale de leer el código en `8929aea`, sin ejecutar la aplicación.

Cada punto indica cómo se verificó. "Lectura" significa que se comprobó en el fuente; "inferencia" significa que la conclusión depende de cómo se comporta una biblioteca y no se observó en ejecución.

## Posibles defectos

| Hallazgo | Evidencia | Tipo |
|---|---|---|
| **Las tapas del carrito apuntan a una ruta que no existe.** `cart/index.jsp` arma la URL como `/covers/{imageId}`. [[ImageController]] solo atiende `/post/{postId}/images/{imageId}`, `/users/{userId}/avatar/{imageId}` y `/albums/{albumId}/cover/{imageId}`, y los recursos estáticos son `/css`, `/js` e `/images`. Las demás vistas ya usan la ruta nueva. Consecuencia esperable: las miniaturas del carrito dan 404 | Lectura de la JSP, del controller y de `WebConfig` | Lectura; el 404 es inferencia |
| **`app.base-url` y `app.mail.from` no fallan al arrancar si faltan.** Se inyectan con `@Value("${...}")` y el proyecto no declara un `PropertySourcesPlaceholderConfigurer`. Sin ese bean, Spring resuelve los placeholders en modo no estricto y deja el texto `${app.base-url}` tal cual. Los enlaces de los correos saldrían rotos sin ningún error al iniciar | Lectura de [[EmailServiceImpl]] y [[WebConfig]] | Inferencia sobre Spring 5.3 |
| `InvalidPostDataException` e `InvalidPaymentInfoException` no tienen handler web. Solo se alcanzan salteando el formulario; la respuesta sería un 500 | Búsqueda de usos en `webapp` | Lectura |

El primero se originó en la convivencia de dos PR: el #46 movió las imágenes a rutas asociadas a su recurso y el #47 (carrito) se escribió contra la ruta anterior.

## Comentarios que no coinciden con el código

| Dónde | Dice | El código |
|---|---|---|
| [[ReceiptValidator]] | El resolver multipart corta el request a los 6 MB | `ImageRules.MAX_MULTIPART_BYTES` es 5 MiB × 5 + 1 MiB = 26 MiB, desde que la galería admite cinco fotos |

## Documentos del repositorio desactualizados

| Documento | Qué dice | Qué hace el código en `8929aea` |
|---|---|---|
| `README.md`, sección "Credenciales de acceso" | El registro no pide contraseña hasta demostrar acceso al correo; un token abre un formulario donde se eligen usuario y contraseña | Desde el PR #43 la cuenta se crea con contraseña al registrarse, inicia sesión en el acto y verifica el correo después ([[Authentication flow]]) |
| `TODO.md` (fechado 09/09) | No hay Spring Security; no hay búsqueda, filtros ni paginación | Los tres existen |
| `TODO.md`, deuda técnica | Cambiar la clave no cierra las sesiones de otros navegadores | Resuelto en el PR #43 con `SessionRegistry` ([[Security and authorization]]) |
| `TODO.md`, deuda técnica | El esquema no tiene claves foráneas | V3 las agregó ([[Database schema]]) |
| `docs/setup.md` | Nombra el módulo `service-contracts` | Se llama `services-contracts` |
| `database/users.sql` | Tabla `users` de cuatro columnas | Resto del esqueleto inicial; no lo usa nadie |
| `docs/issues/02` y `03` | Catálogo editorial fijo de ocho álbumes | La portada lista publicaciones reales |

`CONTEXT.md` (glosario) y los ADR sí están al día: el glosario incorporó la Cuenta verificada y el carrito.

## Pendientes respecto de la defensa del sprint 2

El detalle de cada observación está en [[Sprint 2 defense review]].

| Punto | Estado en `8929aea` |
|---|---|
| Usar `BigDecimal` para el dinero | No aplicado: el precio es `int` en los modelos e `INTEGER` en la base. Ningún uso de `BigDecimal` en el repositorio |
| Liberar la reserva si el comprobante no llega a tiempo | No hay plazo ni tarea programada: el Post queda reservado hasta que alguien cancela |
| Validar el token antes de mostrar el formulario de nueva contraseña | `GET /reset-password` muestra el formulario sin validar; el token se valida al enviar |
| No exponer si una cuenta existe | La recuperación no lo expone; el registro sí informa que el correo ya tiene cuenta |
| No mezclar mecanismos de autorización | Conviven reglas por URL y `@PreAuthorize`, con un criterio por capa |
| Correos en inglés | El idioma sale del navegador o de la cuenta; falta confirmarlo en ejecución con un navegador en español |

## Límites de diseño

No son errores: son decisiones o simplificaciones que conviene poder explicar.

### Seguridad

- Los tokens de verificación y de recuperación se guardan **en claro** en la base. Se dejó de guardar su hash en el commit `a8468071`. Quien pueda leer la tabla puede usar un enlace vigente ([[Tokens and email links]]).
- El token de verificación **no vence**. El de recuperación dura una hora.
- No hay límite de intentos de login ni de pedidos de recuperación. Sí hay un freno de un minuto para el reenvío de la verificación.
- El `SessionRegistry` vive en memoria: con más de una instancia, cerrar las sesiones de una cuenta solo alcanzaría a las de esa instancia.
- La propiedad de una publicación para editarla o borrarla se controla solo con `@PreAuthorize` en el controller: `PostService.update` y `delete` no reciben quién actúa.
- Las imágenes de comprobante se validan por tipo declarado y tamaño; solo el PDF se valida por contenido. Las fotos de publicaciones y avatares sí se validan por firma.

### Datos

- Unicidad `(user_id, album_id)` en `posts`: incluye publicaciones vendidas, así que no se puede volver a publicar un álbum ya vendido.
- Editar una publicación reescribe datos compartidos de artista y álbum, que otras publicaciones del mismo álbum también muestran ([[Edit and delete flow]]).
- Borrar una publicación rechaza sus consultas pendientes sin avisar por correo.
- `posts.stock` existe y vale siempre 1.
- `users.preferred_locale` se fija al registrarse y no se actualiza.

### Operación

- No hay cola persistente de correo: si el proceso muere entre el commit y el envío, o el pool está saturado, el aviso se pierde ([[Mail delivery]]).
- `DriverManagerDataSource` sin pool de conexiones.
- Sin página propia para el error 500.
- Sin pasarela de pago: el comprobante se revisa a mano.

### Evidencia

- Ningún test cubre controllers, seguridad, vistas ni concurrencia; los de persistence corren en HSQLDB ([[Testing and evidence]]).
- Este vault es lectura estática. No registra ninguna ejecución de la aplicación en `8929aea`.

## Resuelto desde el mapa anterior (`f12af08`)

| Antes | Ahora |
|---|---|
| La búsqueda enviada no ignoraba tildes como las sugerencias | Misma normalización en las dos (`a4c39048`) |
| El catálogo no mostraba el total de resultados | Páginas numeradas y total (`3f3ea4e9`) |
| Dos pantallas distintas para "sin resultados" | Un solo estado vacío (`c16f1131`) |
| El registro pedía verificar antes de crear la cuenta | Se crea la cuenta y se verifica después (`0870c81d`) |
| Sugerencias devueltas como HTML | JSON (`bc8fd210`) |
| Reglas de acceso repartidas | Reglas por URL para la verificación y `@PreAuthorize` para la pertenencia (`0870c81d`, `86b1f75d`) |
| Cambiar la clave no cerraba otras sesiones | Las cierra (`1350d001`) |
| Esquema en un `schema.sql` sin claves foráneas | Flyway V1–V11 con claves foráneas (PR #38) |
| Panel `/admin` vacío | Eliminado; ADMIN modera desde las publicaciones (`60480b55`) |
| Lógica de negocio en controllers | Movida a services (PR #48) |

## Evidencia de código

### URL de la tapa en el carrito

Fuente exacta en `8929aea`: [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>), líneas 51–55.

```jsp
                                <c:forEach items="${group.items}" var="item">
                                    <c:choose>
                                        <c:when test="${item.coverImageId.present}"><c:url value="/covers/${item.coverImageId.get()}" var="coverUrl"/></c:when>
                                        <c:otherwise><c:url value="/images/covers/placeholder.svg" var="coverUrl"/></c:otherwise>
                                    </c:choose>
```

### Rutas de imágenes que existen

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>), líneas 33–49.

```java
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
```

### Tope del multipart

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>), líneas 11–13.

```java
    public static final int MAX_IMAGE_BYTES = 5 * 1024 * 1024;
    public static final int MAX_GALLERY_IMAGES = 5;
    public static final long MAX_MULTIPART_BYTES = (long) MAX_IMAGE_BYTES * MAX_GALLERY_IMAGES + 1024 * 1024;
```

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java>), líneas 10–14.

```java
/*
 * Segunda capa del limite: el resolver multipart corta el request entero a los 6 MB, y este
 * validador deja el comprobante en el tope de ReceiptRules con un error bajo el campo. La
 * regla es la misma que aplica InquiryService al guardarlo.
 */
```

### Validación del comprobante

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java>), líneas 29–38.

```java
    // Espera el tipo ya normalizado.
    public static boolean isValid(final String contentType, final byte[] data) {
        if (contentType == null || !EXTENSIONS.containsKey(contentType)) {
            return false;
        }
        if (data == null || data.length == 0 || data.length > MAX_BYTES) {
            return false;
        }
        return !PDF.equals(contentType) || startsWith(data, PDF_SIGNATURE);
    }
```

## Archivos para seguir el flujo

- [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>) · [[ImageController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java>) · [[ReceiptValidator]]
- [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>) · [[ImageRules]]
- [models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java>) · [[ReceiptRules]]
- [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) · [[EmailServiceImpl]]
- [README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/README.md>)
- [TODO.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/TODO.md>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
