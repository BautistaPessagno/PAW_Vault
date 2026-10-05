@title: Known gaps and document drift
@categories: History, Testing
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java, models/src/main/java/ar/edu/itba/paw/models/ImageRules.java, models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java, services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java, README.md, TODO.md

> [!summary] En una frase
> Lista de lo que el código no hace, hace distinto de lo que dice su documentación, o podría fallar; todo sale de leer el código en `c3e2a4c`, sin ejecutar la aplicación.

Cada punto indica cómo se verificó. "Lectura" significa que se comprobó en el fuente; "inferencia" significa que la conclusión depende de cómo se comporta una biblioteca y no se observó en ejecución.

## Posibles defectos

| Hallazgo | Evidencia | Tipo |
|---|---|---|
| **`app.base-url` y `app.mail.from` no fallan al arrancar si faltan.** Se inyectan con `@Value("${...}")` y el proyecto no declara un `PropertySourcesPlaceholderConfigurer`. Sin ese bean, Spring resuelve los placeholders en modo no estricto y deja el texto `${app.base-url}` tal cual. Los enlaces de los correos saldrían rotos sin ningún error al iniciar | Lectura de [[EmailServiceImpl]] y [[WebConfig]] | Inferencia sobre Spring 5.3 |

## Comentarios que no coinciden con el código

| Dónde | Dice | El código |
|---|---|---|
| [[ReceiptValidator]] | El resolver multipart corta el request a los 6 MB | `ImageRules.MAX_MULTIPART_BYTES` es 5 MiB × 5 + 1 MiB = 26 MiB, desde que la galería admite cinco fotos |

## Documentos del repositorio desactualizados

| Documento | Qué dice | Qué hace el código en `c3e2a4c` |
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

| Punto | Estado en `c3e2a4c` |
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
- Las imágenes de comprobante se validan por tipo declarado y tamaño; solo el PDF se valida por contenido. Las fotos de publicaciones y avatares sí se validan por firma.

### Datos

- Unicidad `(user_id, album_id)` en `posts`: incluye publicaciones vendidas, así que no se puede volver a publicar un álbum ya vendido.
- Editar una publicación reescribe datos compartidos de artista y álbum, que otras publicaciones del mismo álbum también muestran ([[Edit and delete flow]]).
- Borrar una publicación rechaza sus consultas pendientes sin avisar por correo.
- `posts.stock` existe y vale siempre 1.
- `users.preferred_locale` se fija al registrarse y no se actualiza.

### Operación

- Casi todos los logs INFO, incluidos los de publicar y editar que sumó el PR #62, se escriben al final del método pero **antes** del commit; solo seis (crear consulta, verificar, enviar enlaces y cambiar o recuperar la clave) esperan al commit ([[Logging]]).
- No hay cola persistente de correo: si el proceso muere entre el commit y el envío, o el pool está saturado, el aviso se pierde ([[Mail delivery]]).
- `DriverManagerDataSource` sin pool de conexiones.
- Sin página propia para el error 500.
- Sin pasarela de pago: el comprobante se revisa a mano.

### Evidencia

- Ningún test cubre controllers, seguridad, vistas ni concurrencia; los de persistence corren en HSQLDB ([[Testing and evidence]]).
- Este vault es lectura estática. No registra ninguna ejecución de la aplicación en `c3e2a4c`.

## Resuelto desde el mapa anterior (`8929aea`)

| Antes | Ahora |
|---|---|
| Las tapas del carrito apuntaban a `/covers/{imageId}`, una ruta que ya no existía | `cart/index.jsp` usa `/post/{postId}/images/{imageId}` (`2eed2f76`, PR #49) |
| La pertenencia de una publicación para editarla o borrarla solo se controlaba con `@PreAuthorize` | El service la vuelve a chequear con el id de quien actúa (`563f7020`, PR #51; [[Edit and delete flow]]) |
| Agregar al carrito bloqueaba la Cuenta sin bloquear el post, en orden inverso al contacto y al envío | Bloquea primero el post y después la Cuenta (`e12c0e39`, PR #52; [[Transactions and concurrency]]) |
| `Receipt` exponía su arreglo de bytes: quien lo recibía podía modificar el comprobante | Copia el arreglo al construirse y al devolverlo (`612391ea`, PR #53) |
| Un `origin` desconocido o un `originPage` no numérico en la ficha daban 400 | Se ignoran y la ficha abre igual (`ca06676c`, PR #50; [[Post detail flow]]) |
| El precio de la venta quedaba fijo al consultar, aunque el vendedor cambiara el precio antes de aceptar | Se fija al aceptar (`7e073053`, PR #56, ADR 0004; [[Inquiry and sale flow]]) |
| Aceptar sin datos de cobro mandaba al perfil sin forma de volver a la venta | El perfil recuerda la venta y vuelve a ella al guardar (`25f95bc9`, PR #55; [[Addresses and payment flow]]) |
| El perfil público mostraba solo las 10 reseñas más recientes, mezclando roles | Reseñas separadas por rol y paginadas (`5d439ef4`, PR #57; [[Public profile flow]]) |
| `InvalidPostDataException` e `InvalidPaymentInfoException` no tenían handler web: un POST que salteara el formulario terminaba en 500 | [[ErrorResponseAdvice]] las responde con 400 (`c60be91e`, PR #62; [[Validation and errors]]) |
| Quitar una foto al editar era una casilla con texto debajo de cada imagen | Una X sobre la foto que la atenúa y se puede deshacer (`1cc8230e`, `b017d3dd`, PR #59; [[Gallery flow]]) |

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

### Rutas de imágenes que existen

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java:33-49}}

### Tope del multipart

{{code:models/src/main/java/ar/edu/itba/paw/models/ImageRules.java:11-13}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/validation/ReceiptValidator.java:10-14}}

### Validación del comprobante

{{code:models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java:29-38}}
