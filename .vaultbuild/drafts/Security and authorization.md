@title: Security and authorization
@categories: Web, Services, Architecture
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java, webapp/src/main/webapp/WEB-INF/web.xml, webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java, webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java, models/src/main/java/ar/edu/itba/paw/models/ImageRules.java, models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java, persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java, pom.xml

> [!summary] En una frase
> Una regla por capa: `SecurityConfig` decide quién entra a cada URL, `@PreAuthorize` decide si el recurso es tuyo, el service vuelve a chequear antes de escribir y la base cierra las carreras con `UPDATE` condicionales.

La observación 4 del sprint 2 fue que la autorización "no seguía un criterio único". Esta nota describe el criterio que quedó después de los PR #43 y #46, y todo lo demás que protege a la aplicación.

## Herramientas

| Herramienta | Para qué |
|---|---|
| `DelegatingFilterProxy` + `SecurityFilterChain` | Enganchar la cadena de Spring Security al contenedor y definir sus reglas |
| `authorizeHttpRequests` con `RequestMatcher` | Reglas por URL |
| `@EnableMethodSecurity` + `@PreAuthorize` (SpEL) | Reglas por recurso en los métodos de los controllers |
| Beans `postAccess`, `inquiryAccess`, `addressAccess` | Las funciones que consulta el SpEL |
| `AccessDeniedHandler` propio | Decidir entre "verificá tu correo" y 403 |
| `@ControllerAdvice` | Traducir excepciones de negocio a 400, 403 y 404 en un solo lugar |
| `CsrfFilter` (activo por defecto) | Token en todo POST |
| `BCryptPasswordEncoder` | Hash de contraseñas |
| `SessionRegistry` | Expirar sesiones |
| Taglib `sec:` | Mostrar u ocultar partes de la vista y emitir el token CSRF |
| JSTL `c:out` | Escapar todo dato en las JSP |

## Orden de los filtros

Definido en `web.xml`. El orden importa:

| # | Filtro | Rutas | Por qué está ahí |
|---|---|---|---|
| 1 | `CharacterEncodingFilter` (UTF-8 forzado) | `/*` | Que los parámetros se lean en UTF-8 antes que nadie los toque |
| 2 | `MultipartExceptionHandlerFilter` | `/publish`, `/post/*`, `/inquiries/*`, `/profile/avatar` | Envuelve a los siguientes: si el archivo excede el límite, redirige al formulario con un aviso |
| 3 | `MultipartFilter` | Las mismas | Parsea el cuerpo multipart **antes** de la seguridad, para que el token CSRF del formulario ya sea legible |
| 4 | `springSecurityFilterChain` | `/*` | Sesión, CSRF, login, logout y autorización por URL |
| 5 | `DispatcherServlet` | `/` | Controllers; acá corre `@PreAuthorize` |

{{code:webapp/src/main/webapp/WEB-INF/web.xml:20-85}}

## Las cuatro capas de una decisión

Ejemplo: aceptar una consulta, `POST /inquiries/42/accept`.

1. **URL.** `/inquiries/{id}/**` está en `VERIFIED_PATHS`: hace falta la authority `VERIFIED`. Un anónimo va al login; una Cuenta sin verificar, a `/verify/required`.
2. **Recurso.** `@PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")` pregunta si quien tiene la sesión es el publicante de esa consulta. Si no, 403.
3. **Service.** `InquiryServiceImpl.accept` llama a `requireSeller` de nuevo y lanza `ForbiddenOperationException` si no coincide. El service no confía en que todo llamador pase por el controller.
4. **Base.** `UPDATE inquiries SET status = ? WHERE id = ? AND status = ?` y `UPDATE posts ... AND status = ?`: si otra transacción ya movió el estado, no afecta filas y se corta con `InvalidInquiryStateException` (409).

## Autorización por URL

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java:85-110}}

| Quién | Rutas |
|---|---|
| Cuenta verificada (`hasAuthority("VERIFIED")`) | `/publish/**`, `/post/*/edit`, `/post/*/delete`, `/post/*/contact`, `/cart`, `/cart/**`, `/profile/**`, `/inquiries`, `/inquiries/sent`, `/inquiries/{id}/**` |
| Con sesión (`authenticated()`) | `/verify/resend`, `/verify/required` |
| Cualquiera (`permitAll()`) | Todo lo demás: catálogo, ficha, perfiles públicos, imágenes, sugerencias, login, registro, verificación y recuperación |

La lista `VERIFIED_PATHS` se define una sola vez y la usan dos cosas: la regla de acceso y el `AccessDeniedHandler`. Ya no hay regla para `/admin/**`: el panel se eliminó en el PR #46 y el rol `ADMIN` solo aparece en la expresión de moderación de publicaciones.

## Autorización por recurso

| Endpoint | Expresión | Bean |
|---|---|---|
| Editar y eliminar publicación | `hasRole('ADMIN') or @postAccess.isPublisher(authentication, #postId)` | [[PostAccessHandler]] |
| Aceptar, rechazar, confirmar pago, pedir otro comprobante | `@inquiryAccess.isSeller(authentication, #inquiryId)` | [[InquiryAccessHandler]] |
| Subir comprobante | `@inquiryAccess.isBuyer(...)` | [[InquiryAccessHandler]] |
| Ver la consulta, escribir, calificar, ver el comprobante, cancelar | `@inquiryAccess.isParty(...)` | [[InquiryAccessHandler]] |
| Editar y eliminar dirección | `@addressAccess.isOwner(authentication, #addressId)` | [[AddressAccessHandler]] |

Tres detalles que suelen preguntarse:

- **`#postId` funciona por el nombre del parámetro.** Spring necesita los nombres de parámetros en el bytecode; el POM raíz lo pide con `maven.compiler.parameters=true`.
- **Un recurso inexistente "pasa" el handler.** Los tres devuelven `true` si no encuentran el recurso, para que el service responda 404. Si devolvieran `false`, un id inexistente daría un 403 engañoso.
- **Sin sesión devuelven `false`.** `AuthenticatedUser.idOf` devuelve vacío si el principal no es una Cuenta.

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java:9-40}}

### Qué vuelve a chequear cada service

| Recurso | Chequeo en el service | Dónde |
|---|---|---|
| Consulta y venta | Sí: `requireSeller`, `requireBuyer`, `requireParty`, y `lockConfirmedSale` para reseñas | [[InquiryServiceImpl]] |
| Dirección | Sí: `archiveOwned` compara el dueño | [[AddressServiceImpl]] |
| Publicación (editar, eliminar) | **No.** `PostService.update` y `delete` no reciben quién opera; solo exigen que el post siga disponible | [[PostServiceImpl]] |
| Consultar un post propio | Sí: `validateContactable` lanza `ForbiddenOperationException` | [[InquiryServiceImpl]] |

Para las publicaciones la pertenencia vive únicamente en `@PreAuthorize`. Es coherente con el comentario de [[SecurityConfig]] ("los services vuelven a chequear la pertenencia de la Venta y de la libreta"), pero significa que un llamador nuevo de `PostService.update` que no pase por [[PublishController]] no tendría ese control.

## Cómo se convierte una denegación en respuesta

| Situación | Quién la detecta | Respuesta |
|---|---|---|
| Anónimo en ruta protegida | Spring Security | Redirección a `/login`; tras el login vuelve a la URL pedida |
| Con sesión, sin `VERIFIED`, en ruta de `VERIFIED_PATHS` | [[VerificationAccessDeniedHandler]] | Redirección a `/verify/required` |
| Cualquier otra denegación (`@PreAuthorize` falso) | [[VerificationAccessDeniedHandler]] delega en el handler estándar | Forward a `/error/403` |
| `ForbiddenOperationException` desde un service | [[ErrorResponseAdvice]] | Vista `error/403` con estado 403 |
| `*NotFoundException`, `PageNotFoundException` | [[ErrorResponseAdvice]] | Vista `error/404` con estado 404 |
| Ruta que no existe | `<error-page>` de `web.xml` → [[ErrorController]] | 404 con el mismo view resolver y locale |
| `InvalidImageException`, `InvalidReviewException`, parámetro de tipo incorrecto | [[ErrorResponseAdvice]] | 400 |
| `InvalidInquiryStateException`, `PostUnavailableException` | Handler del controller correspondiente | 409 |
| Sesión expirada por cambio de clave | Filtro de sesiones concurrentes | Redirección a `/login?sessionExpired` |
| Casos esperables del carrito (post propio, no disponible, repetido, lleno, dirección archivada, nada para enviar) | [[CartExceptionAdvice]], solo para [[CartController]] y con prioridad sobre [[ErrorResponseAdvice]] | Redirección a la pantalla de origen con un aviso, no una página de error |
| Token CSRF ausente o inválido | `CsrfFilter` | Denegación que pasa por el mismo handler; en general termina en 403 |

Política: lo que no existe es 404, lo que existe y es ajeno es 403, lo que existe pero ya no admite la operación es 409.

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java:15-47}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java:19-50}}

## Sesiones

- La sesión vive en el servidor; el navegador guarda la cookie `JSESSIONID`.
- `<http-only>true</http-only>`: JavaScript no puede leerla.
- `<tracking-mode>COOKIE</tracking-mode>`: el contenedor no reescribe URLs con `;jsessionid`. Sin esto, el firewall de Spring Security rechazaba el `;` y las hojas de estilo devolvían 500.
- No se fija `<secure>`: el contenedor marca la cookie como `Secure` cuando el request llega por HTTPS y la deja usable en desarrollo sobre HTTP.
- Al autenticar cambia el id de sesión (fijación de sesión): Spring lo hace en el form login y `AuthenticationSessions.login` lo hace a mano en el registro.
- `maximumSessions(-1)`: sin tope de sesiones por Cuenta. El `SessionRegistry` está solo para poder expirarlas.
- `HttpSessionEventPublisher` le avisa al registro cuando una sesión nace, cambia de id o muere.
- [[AuthenticatedUser]] define `equals` y `hashCode` por id de Cuenta. El registro agrupa sesiones por principal: sin eso, el principal refrescado después de verificar sería "otro" y sus sesiones no se encontrarían.
- Cambiar o recuperar la clave llama a `logoutEverywhere`: expira las otras sesiones y cierra la actual.

{{code:webapp/src/main/webapp/WEB-INF/web.xml:103-117}}

## CSRF

Spring Security lo deja activo por defecto y el proyecto no lo desactiva. Todo POST necesita el token de la sesión.

- `form:form` lo agrega solo como campo oculto.
- Los `<form>` HTML comunes (aceptar, rechazar, eliminar, logout, reenviar enlace, avatar) usan `<sec:csrfInput/>`.
- En formularios multipart el token viaja en el cuerpo; por eso `MultipartFilter` va antes de la cadena de seguridad.
- El logout es un POST: un enlace malicioso no puede cerrar la sesión.
- Los `GET` no cambian estado, con una excepción deliberada: `GET /verify` (ver [[Tokens and email links]]).

## Contraseñas

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java:34-60}}

BCrypt con costo 12. [[ValidPassword]] exige de 12 a 72 caracteres, una letra y un número; el máximo es el tope de BCrypt. El formulario nunca vuelve a mostrar una clave. Cambiar la clave desde el perfil usa `UPDATE ... WHERE password_hash = <el leído>` para no pisar una clave elegida en paralelo.

## Entrada no confiable

| Riesgo | Defensa en el código |
|---|---|
| XSS en vistas | Todo dato va por `<c:out>`; el texto visible sale de `<spring:message>` |
| XSS en autocompletado | Los endpoints devuelven JSON y `autocomplete.js` arma cada opción con `createElement` y `textContent`; se eliminó `innerHTML` (observación 3 del sprint 2) |
| XSS en correos | Thymeleaf escapa `th:text` |
| Inyección SQL | Solo parámetros `?`; el `ORDER BY` sale de un `switch` sobre el enum [[PostSort]]; los comodines de `LIKE` se escapan; las listas `IN` usan un placeholder por valor |
| Redirección abierta | [[SameSiteRedirects]] acepta el `Referer` solo si es del mismo host y cae dentro del context path, y descarta `//` y `\`. La ficha usa `returnQuery` únicamente detrás de `/?`, y el carrito pasa ese mismo parámetro por [[ListingQueries]], que solo deja caracteres de una query ya codificada |
| Enumeración de cuentas | Recuperación responde igual exista o no; el login da un error genérico. El registro sí informa el correo duplicado |
| Parámetros de filtro inválidos | Se ignoran o dan error de campo; un tipo incorrecto en la URL da 400 |

## Archivos subidos

| Tipo | Regla | Dónde |
|---|---|---|
| Fotos de publicación y avatar | PNG, JPEG o WEBP; el tipo declarado tiene que coincidir con la **firma** de los primeros bytes; hasta 5 MiB cada una; hasta 5 fotos por publicación | [[ImageRules]] |
| Comprobante | PDF, PNG, JPEG o WEBP; hasta 5 MiB; el PDF tiene que empezar con `%PDF-` | [[ReceiptRules]] |
| Request multipart completo | 26 MiB (`5 × 5 MiB + 1 MiB`) | `MAX_MULTIPART_BYTES`, aplicado por el resolver en [[WebConfig]] |

La misma regla se aplica dos veces: en el validador del formulario (para mostrar el error junto al campo) y en el service (por si alguien saltea el formulario). Las dos leen la misma clase de `models`.

{{code:models/src/main/java/ar/edu/itba/paw/models/ImageRules.java:15-64}}

Cómo se sirven:

- **Imágenes**: nunca por id suelto. Las rutas son `/post/{postId}/images/{imageId}`, `/users/{userId}/avatar/{imageId}` y `/albums/{albumId}/cover/{imageId}`, y el SQL exige que la imagen pertenezca a ese recurso. El avatar además exige que la Cuenta esté verificada. Así no se pueden recorrer imágenes ajenas incrementando el id.
- **Comprobante**: solo para las dos partes; `nosniff`, sin caché, `Content-Disposition: inline` con nombre y extensión. Las imágenes van con `Content-Security-Policy: sandbox`. El PDF no, porque el visor de Chrome no abre un documento con sandbox; por eso se exige la firma `%PDF-` al subirlo.

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java:47-68}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java:212-236}}

## Privacidad

- El publicante ve la dirección completa del comprador solo mientras hay una venta en curso o concretada. Pendiente, rechazada o cancelada, ve ciudad y provincia (`withAddressForSeller`).
- El comprador ve los datos de cobro solo mientras la venta está abierta (`isPaymentInfoVisible`).
- Ni CBU ni dirección viajan por correo.
- El perfil público solo existe para Cuentas verificadas.
- Los logs llevan ids, nunca correos ni el texto de un Mensaje.
- `database.properties` y `mail.properties` no se versionan.

## Límites conocidos

- La pertenencia de una publicación se chequea solo en la capa web.
- Sin límite de intentos de login, de pedidos de recuperación ni bloqueo de cuenta.
- Tokens de correo guardados en claro; el de verificación no vence.
- `SessionRegistry` en memoria: una sola instancia.
- El comprobante con tipo imagen no valida firma (solo el PDF); se compensa con `sandbox` y `nosniff` al servirlo.
- El comentario de [[ReceiptValidator]] dice que el resolver corta el request a los 6 MB; el valor actual es 26 MiB.
- Los headers de seguridad son los que Spring Security aplica por defecto; el repo no los ajusta.
- No hay tests de la capa web: la cadena de filtros, CSRF y `@PreAuthorize` se verificaron a mano según el issue.

Son observaciones sobre el código leído; no se ejecutó ninguna prueba de seguridad.

## Preguntas de defensa

**¿Dónde se decide quién puede hacer qué?**
En tres lugares con responsabilidades distintas: la URL en `SecurityConfig` (quién sos), `@PreAuthorize` en el controller (si el recurso es tuyo) y el service (lo vuelve a chequear para la venta y las direcciones).

**¿Por qué 404 y no 403 cuando el recurso no existe?**
Para no mentir. El handler deja pasar un id inexistente y el service responde 404.

**¿Cómo sabe `@PreAuthorize` cuál es `#inquiryId`?**
Por el nombre del parámetro del método, que se conserva en el bytecode con `-parameters`.

**¿Qué diferencia hay entre `hasRole('ADMIN')` y `hasAuthority('VERIFIED')`?**
`hasRole` agrega el prefijo `ROLE_`. `VERIFIED` es una authority sin prefijo: no es un rol, es un atributo de la Cuenta.

**¿Cómo se protegen de CSRF?**
Token por sesión en todo POST, agregado por `form:form` o por `sec:csrfInput`. El filtro multipart corre antes para que el token sea legible.

**¿Y de XSS?**
`c:out` en todas las vistas, `textContent` en el JavaScript y escape de Thymeleaf en los correos.

**¿Cómo evitan que suban un ejecutable con extensión de imagen?**
Se comparan los primeros bytes con la firma del formato declarado, en el formulario y en el service.

**¿Qué pasa si alguien cambia el id de una imagen en la URL?**
La consulta exige que esa imagen pertenezca al post, al usuario o al álbum de la misma URL. Si no, 404.

**¿Qué pasa con las sesiones si cambio la contraseña?**
Se expiran todas; cada navegador va a `/login?sessionExpired` en su próximo request.
