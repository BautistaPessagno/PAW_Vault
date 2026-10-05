---
title: "Security and authorization"
categories: ["Web", "Services", "Architecture"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java", "webapp/src/main/webapp/WEB-INF/web.xml", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java", "models/src/main/java/ar/edu/itba/paw/models/ImageRules.java", "models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java", "pom.xml"]
---

# Security and authorization

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

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>), líneas 20–85.

```xml
  <filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
    <init-param>
      <param-name>forceEncoding</param-name>
      <param-value>true</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <filter>
    <filter-name>multipartExceptionHandlerFilter</filter-name>
    <filter-class>ar.edu.itba.paw.webapp.security.MultipartExceptionHandlerFilter</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>multipartExceptionHandlerFilter</filter-name>
    <url-pattern>/publish</url-pattern>
    <url-pattern>/post/*</url-pattern>
    <url-pattern>/inquiries/*</url-pattern>
    <url-pattern>/profile/avatar</url-pattern>
  </filter-mapping>
  <!--
    Corre antes de la cadena de Spring Security para que el token CSRF del form multipart
    de publicacion, edicion, comprobante o foto de perfil ya este parseado cuando se valida.
  -->
  <filter>
    <filter-name>multipartFilter</filter-name>
    <filter-class>org.springframework.web.multipart.support.MultipartFilter</filter-class>
    <init-param>
      <param-name>multipartResolverBeanName</param-name>
      <param-value>multipartResolver</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>multipartFilter</filter-name>
    <url-pattern>/publish</url-pattern>
    <url-pattern>/post/*</url-pattern>
    <url-pattern>/inquiries/*</url-pattern>
    <url-pattern>/profile/avatar</url-pattern>
  </filter-mapping>
  <filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>
  <listener>
    <listener-class>
      org.springframework.web.context.ContextLoaderListener
</listener-class>
  </listener>
  <!--
    Publica la creacion, el cambio de id y la destruccion de cada sesion para que el
    SessionRegistry de SecurityConfig sepa que sesiones siguen vivas.
  -->
  <listener>
    <listener-class>org.springframework.security.web.session.HttpSessionEventPublisher</listener-class>
  </listener>
```

## Las cuatro capas de una decisión

Ejemplo: aceptar una consulta, `POST /inquiries/42/accept`.

1. **URL.** `/inquiries/{id}/**` está en `VERIFIED_PATHS`: hace falta la authority `VERIFIED`. Un anónimo va al login; una Cuenta sin verificar, a `/verify/required`.
2. **Recurso.** `@PreAuthorize("@inquiryAccess.isSeller(authentication, #inquiryId)")` pregunta si quien tiene la sesión es el publicante de esa consulta. Si no, 403.
3. **Service.** `InquiryServiceImpl.accept` llama a `requireSeller` de nuevo y lanza `ForbiddenOperationException` si no coincide. El service no confía en que todo llamador pase por el controller.
4. **Base.** `UPDATE inquiries SET status = ? WHERE id = ? AND status = ?` y `UPDATE posts ... AND status = ?`: si otra transacción ya movió el estado, no afecta filas y se corta con `InvalidInquiryStateException` (409).

## Autorización por URL

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>), líneas 85–110.

```java
    /*
     * Regla por capa: aca se decide quien puede entrar a cada URL (anonimo, cuenta con sesion o
     * cuenta verificada). Quien puede operar sobre un recurso ajeno lo decide un @PreAuthorize en
     * el controller: @postAccess (Publicante o administrador) para editar y eliminar un Post, y
     * @inquiryAccess y @addressAccess para la Venta y la libreta. Los services vuelven a chequear la
     * pertenencia de Posts, Venta y libreta antes de escribir, y responden 403 o 404.
     *
     * Las rutas de cuenta verificada se definen una sola vez: las usan la regla de acceso y el
     * AccessDeniedHandler que manda a la pagina de "verifica tu correo".
     *
     * El perfil y las bandejas de consultas tambien piden la cuenta verificada: cualquiera puede
     * registrar un correo ajeno, y esa sesion no tiene que ver los datos de cobro, las
     * direcciones ni las consultas que el dueno real del correo cargue despues.
     */
    private static final RequestMatcher VERIFIED_PATHS = new OrRequestMatcher(
            new AntPathRequestMatcher("/publish/**"),
            new AntPathRequestMatcher("/post/*/edit"),
            new AntPathRequestMatcher("/post/*/delete"),
            new AntPathRequestMatcher("/post/*/contact"),
            new AntPathRequestMatcher("/cart"),
            new AntPathRequestMatcher("/cart/**"),
            new AntPathRequestMatcher("/profile/**"),
            new AntPathRequestMatcher("/inquiries"),
            new AntPathRequestMatcher("/inquiries/sent"),
            // Toda accion sobre una consulta: aceptar, rechazar y las que se sumen despues.
            new AntPathRequestMatcher("/inquiries/{inquiryId:[0-9]+}/**"));
```

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

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java>), líneas 9–40.

```java
// Reglas de @PreAuthorize para la Consulta y su Venta: ver, conversar y cancelar es de las dos
// partes, subir el comprobante es del comprador y revisarlo es del Publicante. Una consulta inexistente pasa:
// el handler llega al service, que responde 404 en vez de un 403 enganioso.
public final class InquiryAccessHandler {

    private final InquiryService inquiryService;

    public InquiryAccessHandler(final InquiryService inquiryService) {
        this.inquiryService = inquiryService;
    }

    public boolean isBuyer(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isBuyer);
    }

    public boolean isSeller(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isSeller);
    }

    public boolean isParty(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isParty);
    }

    private boolean allows(final Authentication authentication, final long inquiryId,
                           final BiPredicate<InquiryParties, Long> rule) {
        return AuthenticatedUser.idOf(authentication)
                .map(userId -> inquiryService.findParties(inquiryId)
                        .map(parties -> rule.test(parties, userId))
                        .orElse(true))
                .orElse(false);
    }
}
```

### Qué vuelve a chequear cada service

| Recurso | Chequeo en el service | Dónde |
|---|---|---|
| Consulta y venta | Sí: `requireSeller`, `requireBuyer`, `requireParty`, y `lockConfirmedSale` para reseñas | [[InquiryServiceImpl]] |
| Dirección | Sí: `archiveOwned` compara el dueño | [[AddressServiceImpl]] |
| Publicación (editar, eliminar) | Sí, desde el PR #51: `findEditableById`, `update` y `delete` reciben el id de quien actúa y `requireEditable` exige publicante o rol `ADMIN` antes de exigir `AVAILABLE` | [[PostServiceImpl]] |
| Consultar un post propio | Sí: `validateContactable` lanza `ForbiddenOperationException` | [[InquiryServiceImpl]] |

Hasta `8929aea` las publicaciones eran la excepción: la pertenencia vivía solo en `@PreAuthorize`. El commit `563f7020` la llevó también al service y el comentario de [[SecurityConfig]] pasó a decir "los services vuelven a chequear la pertenencia de Posts, Venta y libreta". Ver [[Edit and delete flow]].

## Cómo se convierte una denegación en respuesta

| Situación | Quién la detecta | Respuesta |
|---|---|---|
| Anónimo en ruta protegida | Spring Security | Redirección a `/login`; tras el login vuelve a la URL pedida |
| Con sesión, sin `VERIFIED`, en ruta de `VERIFIED_PATHS` | [[VerificationAccessDeniedHandler]] | Redirección a `/verify/required` |
| Cualquier otra denegación (`@PreAuthorize` falso) | [[VerificationAccessDeniedHandler]] delega en el handler estándar | Forward a `/error/403` |
| `ForbiddenOperationException` desde un service | [[ErrorResponseAdvice]] | Vista `error/403` con estado 403 |
| `*NotFoundException`, `PageNotFoundException` | [[ErrorResponseAdvice]] | Vista `error/404` con estado 404 |
| Ruta que no existe | `<error-page>` de `web.xml` → [[ErrorController]] | 404 con el mismo view resolver y locale |
| `InvalidImageException`, `InvalidReviewException`, `InvalidPostDataException`, `InvalidPaymentInfoException`, parámetro de tipo incorrecto | [[ErrorResponseAdvice]] | 400 |
| `InvalidInquiryStateException`, `PostUnavailableException` | Handler del controller correspondiente | 409 |
| Sesión expirada por cambio de clave | Filtro de sesiones concurrentes | Redirección a `/login?sessionExpired` |
| Casos esperables del carrito (post propio, no disponible, repetido, lleno, dirección archivada, nada para enviar) | [[CartExceptionAdvice]], solo para [[CartController]] y con prioridad sobre [[ErrorResponseAdvice]] | Redirección a la pantalla de origen con un aviso, no una página de error |
| Token CSRF ausente o inválido | `CsrfFilter` | Denegación que pasa por el mismo handler; en general termina en 403 |

Política: lo que no existe es 404, lo que existe y es ajeno es 403, lo que existe pero ya no admite la operación es 409.

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>), líneas 15–47.

```java
/*
 * Una cuenta sin verificar que entra a una ruta de cuenta verificada llega a la pagina que
 * le explica que le falta y le deja reenviar el enlace. Cualquier otra denegacion, como la
 * administracion, sigue siendo el 403 de siempre: verificar no le daria acceso.
 */
public final class VerificationAccessDeniedHandler implements AccessDeniedHandler {

    private static final String VERIFICATION_REQUIRED_PATH = "/verify/required";

    private final RequestMatcher verifiedPaths;
    private final AccessDeniedHandlerImpl forbiddenHandler = new AccessDeniedHandlerImpl();

    public VerificationAccessDeniedHandler(final RequestMatcher verifiedPaths, final String forbiddenPage) {
        this.verifiedPaths = verifiedPaths;
        this.forbiddenHandler.setErrorPage(forbiddenPage);
    }

    @Override
    public void handle(final HttpServletRequest request, final HttpServletResponse response,
                       final AccessDeniedException exception) throws IOException, ServletException {
        if (verifiedPaths.matches(request) && !isVerified()) {
            response.sendRedirect(request.getContextPath() + VERIFICATION_REQUIRED_PATH);
            return;
        }
        forbiddenHandler.handle(request, response, exception);
    }

    private static boolean isVerified() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return authentication != null && authentication.getAuthorities().stream()
                .anyMatch(authority -> AuthenticatedUser.VERIFIED.equals(authority.getAuthority()));
    }
}
```

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>), líneas 21–52.

```java
/*
 * Unico lugar donde las excepciones de pertenencia, de recurso inexistente y de datos que los
 * formularios ya validan se vuelven respuestas: un recurso que no existe es 404, uno que existe
 * pero es ajeno, 403, y un dato que no cumple las reglas del dominio, 400.
 */
@ControllerAdvice
public class ErrorResponseAdvice {

    @ExceptionHandler({PostNotFoundException.class, InquiryNotFoundException.class,
            UserNotFoundException.class, PageNotFoundException.class, AddressNotFoundException.class,
            ReceiptNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ModelAndView notFound() {
        return new ModelAndView("error/404");
    }

    @ExceptionHandler(ForbiddenOperationException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ModelAndView forbidden() {
        return new ModelAndView("error/403");
    }

    // Los formularios aplican las mismas ImageRules, ReviewRules, VinylInputRules y PaymentInfoRules:
    // solo llega aca un POST que se salteo la validacion. Un parametro de la URL que no es del tipo
    // esperado (una pagina que no es un numero, un origin desconocido) tambien es un pedido mal armado.
    @ExceptionHandler({InvalidImageException.class, InvalidReviewException.class, InvalidPostDataException.class,
            InvalidPaymentInfoException.class, MethodArgumentTypeMismatchException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ModelAndView badRequest() {
        return new ModelAndView("error/400");
    }
}
```

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

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>), líneas 103–117.

```xml
  <!--
    Sin <secure>, el contenedor marca la cookie de sesion como Secure cuando el request
    llega por HTTPS y la deja utilizable en el desarrollo local sobre HTTP.
  -->
  <session-config>
    <cookie-config>
      <http-only>true</http-only>
    </cookie-config>
    <!--
      Solo cookie: sin esto el contenedor reescribe cada URL con ;jsessionid hasta confirmar
      que hay cookie, y el StrictHttpFirewall de Spring Security rechaza el ";" con un 500.
      Las hojas de estilo son las primeras en caer y la pagina queda sin CSS.
    -->
    <tracking-mode>COOKIE</tracking-mode>
  </session-config>
```

## CSRF

Spring Security lo deja activo por defecto y el proyecto no lo desactiva. Todo POST necesita el token de la sesión.

- `form:form` lo agrega solo como campo oculto.
- Los `<form>` HTML comunes (aceptar, rechazar, eliminar, logout, reenviar enlace, avatar) usan `<sec:csrfInput/>`.
- En formularios multipart el token viaja en el cuerpo; por eso `MultipartFilter` va antes de la cadena de seguridad.
- El logout es un POST: un enlace malicioso no puede cerrar la sesión.
- Los `GET` no cambian estado, con una excepción deliberada: `GET /verify` (ver [[Tokens and email links]]).

## Contraseñas

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>), líneas 34–60.

```java
    // Costo 12: es el que ya tienen los hashes guardados, subirlo los invalidaria.
    private static final int BCRYPT_STRENGTH = 12;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(BCRYPT_STRENGTH);
    }

    /*
     * Los services hashean la clave elegida al registrarse, pero no pueden
     * depender de spring-security: el modulo services no la tiene en su classpath. Este
     * bean adapta el encoder a la interfaz PasswordHasher de services-contracts.
     */
    @Bean
    public PasswordHasher passwordHasher(final PasswordEncoder passwordEncoder) {
        return new PasswordHasher() {
            @Override
            public String hash(final String rawPassword) {
                return passwordEncoder.encode(rawPassword);
            }

            @Override
            public boolean matches(final String rawPassword, final String passwordHash) {
                return passwordEncoder.matches(rawPassword, passwordHash);
            }
        };
    }
```

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

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>), líneas 15–64.

```java
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
```

Cómo se sirven:

- **Imágenes**: nunca por id suelto. Las rutas son `/post/{postId}/images/{imageId}`, `/users/{userId}/avatar/{imageId}` y `/albums/{albumId}/cover/{imageId}`, y el SQL exige que la imagen pertenezca a ese recurso. El avatar además exige que la Cuenta esté verificada. Así no se pueden recorrer imágenes ajenas incrementando el id.
- **Comprobante**: solo para las dos partes; `nosniff`, sin caché, `Content-Disposition: inline` con nombre y extensión. Las imágenes van con `Content-Security-Policy: sandbox`. El PDF no, porque el visor de Chrome no abre un documento con sandbox; por eso se exige la firma `%PDF-` al subirlo.

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>), líneas 47–68.

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
```

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>), líneas 237–261.

```java
    /*
     * El comprobante lo sube un usuario: nosniff y sin cache para que el navegador no lo
     * reinterprete ni lo guarde en disco. Las imagenes van ademas con sandbox. Los PDF no: el
     * visor integrado de Chrome se niega a abrir un documento con sandbox, y el PDF es el
     * comprobante mas comun. Por eso al subirlo se exige que empiece con la firma %PDF-, y sus
     * scripts corren en el sandbox propio del visor, sin acceso al origen. El nombre lleva la
     * extension del tipo para que al guardarlo quede un archivo que se pueda abrir.
     */
    @PreAuthorize("@inquiryAccess.isParty(authentication, #inquiryId)")
    @RequestMapping(value = "/{inquiryId:[0-9]+}/receipt", method = RequestMethod.GET)
    public ResponseEntity<byte[]> receipt(@PathVariable("inquiryId") final long inquiryId,
                                          @AuthenticationPrincipal final AuthenticatedUser currentUser) {
        final Receipt receipt = inquiryService.findReceipt(inquiryId, currentUser.getId());
        final MediaType mediaType = MediaType.parseMediaType(receipt.getContentType());
        final ResponseEntity.BodyBuilder response = ResponseEntity.ok()
                .contentType(mediaType)
                .cacheControl(CacheControl.noStore().cachePrivate())
                .header("X-Content-Type-Options", "nosniff")
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        ContentDisposition.inline().filename(receipt.getFilename()).build().toString());
        if (!MediaType.APPLICATION_PDF.equalsTypeAndSubtype(mediaType)) {
            response.header("Content-Security-Policy", "sandbox");
        }
        return response.body(receipt.getData());
    }
```

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

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>) · [[SecurityConfig]]
- [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>) · [[AuthenticatedUser]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java>) · [[AuthenticationSessions]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>) · [[VerificationAccessDeniedHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java>) · [[PostAccessHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java>) · [[InquiryAccessHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AddressAccessHandler.java>) · [[AddressAccessHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java>) · [[SameSiteRedirects]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>) · [[MultipartExceptionHandlerFilter]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorResponseAdvice.java>) · [[ErrorResponseAdvice]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ErrorController.java>) · [[ErrorController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/CartExceptionAdvice.java>) · [[CartExceptionAdvice]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ListingQueries.java>) · [[ListingQueries]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>) · [[PublishController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/InquiryController.java>) · [[InquiryController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ProfileController.java>) · [[ProfileController]]
- [models/src/main/java/ar/edu/itba/paw/models/ImageRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ImageRules.java>) · [[ImageRules]]
- [models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReceiptRules.java>) · [[ReceiptRules]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>) · [[ImageJdbcDao]]
- [pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/pom.xml>)

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
