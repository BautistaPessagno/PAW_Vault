---
title: "Authentication flow"
categories: ["Flows", "Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java", "services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java", "webapp/src/main/webapp/WEB-INF/web.xml", "webapp/src/main/webapp/WEB-INF/tags/site-header.tag"]
---

# Authentication flow

> [!summary] En una frase
> La Cuenta se crea y queda con sesión en el mismo `POST /register`; verificar el correo es un paso posterior que no bloquea el login y solo agrega la authority `VERIFIED`, que es la que exigen las URLs sensibles.

## Qué resuelve

Registro, inicio y cierre de sesión, verificación del correo y reenvío del enlace. Es el flujo que la cátedra observó en el sprint 2 ("primero la creación y luego la verificación", "que no haga falta volver a iniciar sesión") y que el PR #43 reescribió. La recuperación de contraseña está en [[Password recovery flow]]; el detalle de los enlaces, en [[Tokens and email links]]; las reglas de acceso completas, en [[Security and authorization]].

## Herramientas

| Herramienta | Para qué se usa acá | Dónde se configura |
|---|---|---|
| Spring Security 5.8 (`spring-security-web`, `-config`, `-taglibs`) | Cadena de filtros, form login, logout, CSRF, sesiones, `@PreAuthorize`, tags `sec:` en JSP | [[SecurityConfig]], `web.xml` (`DelegatingFilterProxy`) |
| BCrypt (`BCryptPasswordEncoder`, costo 12) | Hash de contraseñas con sal incluida en el propio hash | [[SecurityConfig]] `passwordEncoder()` |
| `PasswordHasher` (interfaz propia) | Que `services` pueda hashear sin depender de Spring Security | Contrato en `services-contracts`, adaptador en [[SecurityConfig]] |
| `UserDetailsService` + `UserDetails` | Cargar la Cuenta por correo y exponerla como principal | [[AuthenticatedUserDetailsService]], [[AuthenticatedUser]] |
| `HttpSession` + cookie `JSESSIONID` | Guardar el `SecurityContext` entre requests | `web.xml` `<session-config>` |
| `SessionRegistry` + `HttpSessionEventPublisher` | Saber qué sesiones tiene abiertas cada Cuenta para poder expirarlas | [[SecurityConfig]], `web.xml` |
| Bean Validation (Hibernate Validator) | Reglas de correo, nombre y contraseña del formulario | [[RegisterForm]], [[ValidPassword]], [[MatchingPasswords]] |
| `SecureRandom` + Base64 URL | Generar el token del enlace de verificación | [[UserServiceImpl]] `generateToken()` |
| Spring JDBC | `users` y `email_verification_tokens` | [[UserJdbcDao]], [[EmailVerificationTokenJdbcDao]] |
| `@Transactional` + `TransactionSynchronization` | Que la Cuenta y su token se guarden juntos y el correo salga solo si hubo commit | [[UserServiceImpl]], [[TransactionCallbacks]] |
| JavaMail + Thymeleaf + `@Async` | Armar y mandar el correo sin frenar el request | [[Mail delivery]] |

## Recorrido paso a paso

### 1. Registro: `POST /register`

1. El navegador envía correo, nombre de usuario, contraseña y confirmación. El formulario es un `form:form`, así que Spring agrega solo el campo oculto `_csrf`.
2. `CsrfFilter` valida el token antes de llegar al controller. `/register` no está en ninguna regla restrictiva: cae en `anyRequest().permitAll()`.
3. `@InitBinder("registerForm")` recorta espacios en `email` y `username`. La contraseña no se recorta: un espacio es parte de la clave.
4. `@Valid` aplica [[RegisterForm]]: correo obligatorio, con formato y hasta 100 caracteres; nombre obligatorio hasta 100; contraseña con [[ValidPassword]] (12 a 72 caracteres, al menos una letra y un número); y `@MatchingPasswords` a nivel de clase compara las dos contraseñas y cuelga el error del campo de confirmación. Con errores se vuelve a mostrar `auth/register`.
5. `UserService.register(email, username, password, locale)` abre una transacción:
   - Normaliza el correo con `EmailRules.normalize` (recorte y minúsculas).
   - Busca la Cuenta por correo. Si existe **y ya tiene contraseña**, verificada o no, lanza `DuplicateUserException`.
   - Hashea la contraseña con `PasswordHasher.hash` (BCrypt costo 12).
   - Si existe una Cuenta *pendiente* del flujo anterior (sin contraseña), la completa con `completePending`, un `UPDATE ... WHERE password_hash IS NULL`. Si devuelve `false`, otro registro llegó antes y lanza `DuplicateUserException`.
   - Si no existe, la inserta con `verified = false`, rol `USER` y el idioma del request normalizado por `SupportedLocales`. Una carrera en el insert choca contra el índice único de `users.email` (`DuplicateKeyException`) y se traduce a `DuplicateUserException`.
   - `issueVerificationToken`: borra los enlaces anteriores de la Cuenta, genera un token nuevo, lo guarda con su fecha y **registra** el envío del correo para después del commit.
6. Al volver del service la transacción ya hizo commit. Recién ahí corre el callback: `EmailService.sendVerificationEmail`, que es `@Async` y entra al pool `mail-`. El request no espera al SMTP.
7. Si hubo `DuplicateUserException`, el controller marca el campo `email` y agrega `duplicateEmail`, con lo que la vista ofrece el enlace a recuperar la contraseña.
8. Si salió bien, `AuthenticationSessions.login` inicia la sesión a mano (ver abajo) y redirige a `/`. La cabecera muestra el banner de "verificá tu correo" porque el principal todavía no tiene `VERIFIED`.

### 2. Login programático después del registro

El form login de Spring no interviene acá, porque la persona no pasó por `/login`. `AuthenticationSessions.login` reproduce lo que haría el filtro:

1. Si ya había sesión HTTP, `request.changeSessionId()` le cambia el id (protección contra fijación de sesión).
2. Crea un `SecurityContext` vacío y le pone un `UsernamePasswordAuthenticationToken` con el principal [[AuthenticatedUser]], sin credenciales y con sus authorities.
3. Lo deja en `SecurityContextHolder` (para el resto de este request) y lo guarda en la sesión con `HttpSessionSecurityContextRepository.saveContext` (para los siguientes).
4. Registra la sesión en el `SessionRegistry`. El form login lo hace solo; esta ruta no pasa por él y sin este paso un cambio de clave no podría expirarla.

### 3. Login normal: `POST /login`

1. `formLogin` define `/login` como página, `email` y `password` como nombres de los parámetros, `/login?error` como destino del fallo y `defaultSuccessUrl("/", false)`: si la persona venía de una URL protegida, vuelve a esa; si no, al inicio.
2. Spring Security llama a `AuthenticatedUserDetailsService.loadUserByUsername(email)`, que usa `UserService.findByEmail` (normaliza el correo). Si no hay Cuenta, o es una pendiente sin contraseña, lanza `UsernameNotFoundException` con el mismo mensaje genérico.
3. El proveedor compara la contraseña enviada con el hash usando el `PasswordEncoder` (BCrypt).
4. `AuthenticatedUser.isEnabled()` devuelve siempre `true`: **una Cuenta sin verificar también inicia sesión**. Lo que no puede hacer lo decide la authority `VERIFIED`, no el login.
5. Authorities: `ROLE_USER` siempre, `ROLE_ADMIN` si el rol es `ADMIN`, `VERIFIED` si `users.verified` es verdadero.
6. Al autenticar, Spring cambia el id de sesión y la registra en el `SessionRegistry` (por `sessionManagement().maximumSessions(-1).sessionRegistry(...)`; `-1` es sin tope).

Lo que arma el proveedor de autenticación a partir de los beans `UserDetailsService` y `PasswordEncoder` es comportamiento del framework: en el repo solo están esos dos beans y el `formLogin`.

### 4. Verificación: `GET /verify?token=...`

1. La ruta es pública. `UserService.verifyEmail(token, locale)`:
   - Sin token o con un token que no está en la tabla, devuelve vacío.
   - `markVerified` es `UPDATE users SET verified = TRUE WHERE id = ? AND verified = FALSE`. Si no afecta filas (ya estaba verificada), devuelve vacío y no se manda una segunda bienvenida.
   - Borra todos los enlaces de verificación de la Cuenta.
   - Registra el correo de bienvenida para después del commit.
2. El controller llama a `AuthenticationSessions.refreshIfCurrent`: **solo si** este navegador ya tiene la sesión de esa misma Cuenta, reemplaza el principal por uno nuevo, que ahora trae `VERIFIED`. Así puede publicar sin volver a iniciar sesión.
3. Si el enlace se abre en otro navegador, la Cuenta queda verificada pero **no se inicia sesión**: la vista muestra "correo verificado" y el botón para entrar.
4. La vista `auth/verify` recibe `verified` verdadero o falso; con falso y sesión sin verificar ofrece reenviar.

### 5. Reenvío: `POST /verify/resend`

1. Exige sesión (`authenticated()`) y token CSRF. El botón vive en el tag `resend-verification`, dentro del banner de la cabecera y de las páginas de aviso.
2. `UserService.resendVerification(userId, locale)`:
   - `lockById` hace `SELECT ... FOR UPDATE` sobre la fila de la Cuenta. Dos pedidos en paralelo se ordenan y no pasan juntos el chequeo.
   - Si ya está verificada, devuelve `false`.
   - Si el último enlace tiene menos de un minuto (`RESEND_COOLDOWN`), devuelve `false` y el anterior sigue sirviendo.
   - Si no, emite uno nuevo: borra los anteriores y manda el correo después del commit.
3. El controller deja un atributo flash (`verificationResent` o `verificationThrottled`) y vuelve a la página de origen. El destino sale del header `Referer` pasado por `SameSiteRedirects.pathOf`, que solo acepta el mismo host y una ruta dentro del context path; cualquier otra cosa vuelve a `/`.

### 6. Página de aviso: `GET /verify/required`

Cuando una Cuenta con sesión y sin `VERIFIED` entra a una ruta de Cuenta verificada, [[VerificationAccessDeniedHandler]] la redirige acá en vez de mostrar un 403. El handler relee la Cuenta: si se verificó en otro navegador, refresca el principal y manda a `/`.

### 7. Logout: `POST /logout`

Es un POST con CSRF (el botón está en el perfil). Invalida la sesión HTTP, borra la cookie `JSESSIONID` y redirige a `/login?logout`.

```mermaid
sequenceDiagram
    participant B as Navegador
    participant F as Filtros de Spring Security
    participant C as AuthenticationController
    participant U as UserServiceImpl
    participant D as UserDao y TokenDao
    participant M as EmailService (hilo mail-)
    B->>F: POST /register con _csrf
    F->>C: token CSRF válido
    C->>U: register(email, username, password, locale)
    U->>D: findByEmail, create (verified=false)
    U->>D: deleteByUserId, create token
    U-->>C: User (commit hecho)
    U-)M: afterCommit: sendVerificationEmail
    C->>C: AuthenticationSessions.login
    C-->>B: 302 a / con cookie de sesión
    B->>C: GET /verify?token=...
    C->>U: verifyEmail(token)
    U->>D: markVerified, borrar enlaces
    U-)M: afterCommit: sendWelcomeEmail
    C->>C: refreshIfCurrent (si es la misma Cuenta)
    C-->>B: auth/verify
```

## Datos

| Tabla | Columnas que toca | Restricciones que importan |
|---|---|---|
| `users` | `email`, `username`, `password_hash`, `role`, `verified`, `preferred_locale` | Índice único `users_email_key` (V2). `verified` se llamaba `enabled` hasta V6 |
| `email_verification_tokens` | `user_id`, `token`, `created_at` | `token` único; FK a `users`; `created_at` agregado en V6 para el tope de reenvío |

El esquema completo está en [[Database schema]].

## Estados de una Cuenta

| Estado | Cómo se llega | Qué puede hacer |
|---|---|---|
| Anónimo | Sin sesión | Catálogo, ficha, perfiles públicos, imágenes, sugerencias, formularios de auth |
| Con sesión, sin verificar | Registro o login de una Cuenta con `verified = false` | Navegar y pedir el reenvío. Las rutas de Cuenta verificada lo mandan a `/verify/required` |
| Verificada | Abrir el enlace o completar una recuperación de contraseña | Perfil, consultas, carrito, publicar, comprar y vender |
| Verificada con rol `ADMIN` | Rol cargado en la base | Además edita y elimina publicaciones disponibles ajenas |
| Pendiente (heredada) | Cuenta del flujo viejo, sin contraseña | No inicia sesión ni recibe recuperación; se completa registrándose de nuevo |

## Decisiones y por qué

| Decisión | Alternativa descartada | Motivo | Dónde está escrito |
|---|---|---|---|
| Crear la Cuenta al registrarse y verificar después | Flujo anterior: dejar solo el correo, abrir el enlace y recién ahí elegir nombre y clave | Observación de la cátedra en el sprint 2: el registro estaba "al revés" y obligaba a loguearse de nuevo | `docs/issues/observaciones-sprint-2/01-...md` |
| Una Cuenta sin verificar inicia sesión | `isEnabled()` ligado a `verified` (Spring rechazaría el login) | Poder navegar antes de verificar; el límite lo pone `VERIFIED` por URL | Comentario en [[AuthenticatedUser]] |
| `VERIFIED` como authority y no como rol | Un rol `ROLE_VERIFIED` o un chequeo en cada controller | Una sola lista de rutas en [[SecurityConfig]], legible por el corrector | Comentario en [[SecurityConfig]] |
| El perfil y las bandejas también exigen `VERIFIED` | Solo exigirlo para publicar y comprar | Cualquiera puede registrar un correo ajeno: esa sesión no tiene que ver los datos que cargue después el dueño real | Comentario en [[SecurityConfig]] |
| Un correo con contraseña no se vuelve a registrar, aunque no esté verificado | Permitir pisar una Cuenta sin verificar | Quien llegara segundo se quedaría con la Cuenta ajena | Comentario en [[UserServiceImpl]] |
| El enlace verifica pero no inicia sesión | Loguear al abrir el enlace | Quien vea un correo reenviado no tiene que entrar a la Cuenta | Comentario en [[AuthenticationController]] |
| Reemplazar el principal al verificar | Pedir un nuevo login | Las authorities quedan fijas en el principal de la sesión; sin refrescarlo el cambio no se vería | Comentario en [[AuthenticationSessions]] |
| Un solo enlace vivo y un minuto entre reenvíos | Reenvío libre | Que nadie llene de correos la casilla de otro | Comentario en [[UserServiceImpl]] y migración V6 |
| `PasswordHasher` propio | Inyectar `PasswordEncoder` en `services` | `services` no tiene Spring Security en su classpath; el módulo web adapta | Comentario en [[SecurityConfig]] |
| BCrypt con costo 12 fijo | Subir el costo | Los hashes guardados ya tienen ese costo | Comentario en [[SecurityConfig]] |
| Correo después del commit y asíncrono | Enviar dentro de la transacción | Un rollback no debe dejar un correo de algo que no se guardó; un SMTP lento no debe frenar el registro | [[TransactionCallbacks]], [[Mail delivery]] |
| Sesión solo por cookie | Dejar que el contenedor reescriba URLs con `;jsessionid` | El firewall de Spring Security rechaza el `;` y se caía el CSS | Comentario en `web.xml` |

## Concurrencia y casos borde

- **Dos registros simultáneos con el mismo correo**: uno inserta, el otro choca contra el índice único y recibe "correo ya registrado".
- **Dos registros que completan la misma Cuenta pendiente**: el `UPDATE` condicional deja pasar a uno solo.
- **Doble clic en el enlace**: el segundo `markVerified` no afecta filas, devuelve vacío y se muestra "enlace inválido"; la Cuenta ya quedó verificada por el primero.
- **Reenvíos en paralelo**: el bloqueo de la fila de la Cuenta los serializa; el segundo ve el enlace recién creado y cae en la espera.
- **SMTP caído**: el registro igual termina bien; el error queda en el log y la persona puede pedir el reenvío.
- **Verificación en otro navegador**: la sesión vieja sigue sin `VERIFIED` hasta que pase por `/verify/required` o vuelva a iniciar sesión.
- **Enlace abierto por otra Cuenta con sesión**: `refreshIfCurrent` compara ids y no toca esa sesión.

## Límites conocidos

- El token de verificación **no vence** (quedó fuera de alcance en el issue del sprint 2). Solo deja de servir cuando se usa o se reemplaza.
- Los tokens se guardan en claro en la base. Ver [[Tokens and email links]].
- El `SessionRegistry` vive en memoria: sirve con una sola instancia de la aplicación.
- No hay límite de intentos de login ni bloqueo de cuenta por fallos repetidos.
- El registro sí revela si un correo ya tiene Cuenta (el mensaje de duplicado); la recuperación de contraseña no.
- La verificación ocurre en un `GET`: quien tenga el enlace verifica. No hay un paso de confirmación.
- Nada de esto tiene test automático: `webapp` no tiene suite. Se probó a mano contra PostgreSQL según el issue; este Vault no lo ejecutó.

## Preguntas de defensa

**¿Cómo se inicia sesión después de registrarse si la persona no pasó por el login?**
El controller arma el `Authentication` a mano con el `User` que devuelve el service, lo guarda en el `SecurityContext`, persiste ese contexto en la sesión HTTP y registra la sesión en el `SessionRegistry`. Antes cambia el id de sesión.

**¿Dónde se guarda la sesión?**
En el servidor, en la `HttpSession` del contenedor. El navegador solo guarda la cookie `JSESSIONID`, marcada `HttpOnly`. No hay JWT.

**¿Por qué una Cuenta sin verificar puede loguearse?**
Porque `isEnabled()` devuelve siempre `true`. La verificación se modela como la authority `VERIFIED` y las rutas sensibles la exigen con `hasAuthority`.

**¿Qué pasa si verifico desde el celular y tenía la sesión en la compu?**
La Cuenta queda verificada en la base, pero el principal de la compu sigue sin `VERIFIED`. Al tocar una ruta protegida va a `/verify/required`, que relee la Cuenta, refresca el principal y la deja pasar.

**¿Qué impide que alguien registre mi correo y se quede con mi Cuenta?**
No puede verificar sin acceso a mi casilla, y sin verificar no entra al perfil ni a las consultas. Yo no puedo registrarme encima, pero recupero la Cuenta con "olvidé mi contraseña": eso cambia la clave, verifica y cierra todas las sesiones abiertas.

**¿Cómo se hashea la contraseña?**
BCrypt con costo 12. La sal va dentro del hash. El máximo de 72 caracteres del formulario es por el tope de BCrypt.

**¿Qué es CSRF y dónde está el token?**
Es un token por sesión que Spring Security exige en todo POST. `form:form` lo agrega solo; los formularios HTML comunes usan `<sec:csrfInput/>`. Para los formularios con archivos, `MultipartFilter` corre antes que la cadena de seguridad para que el token del cuerpo multipart ya esté leído.

## Evidencia de código

Registro en el controller, con el login programático:

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>), líneas 70–88.

```java
    @RequestMapping(value = "/register", method = RequestMethod.POST)
    public ModelAndView register(@Valid @ModelAttribute("registerForm") final RegisterForm form,
                                 final BindingResult bindingResult, final Locale locale,
                                 final HttpServletRequest request, final HttpServletResponse response) {
        if (bindingResult.hasErrors()) {
            return registerForm(form);
        }

        final User user;
        try {
            user = userService.register(form.getEmail(), form.getUsername(), form.getPassword(), locale);
        } catch (final DuplicateUserException e) {
            bindingResult.rejectValue("email", "auth.register.email.duplicate");
            // Si el correo es suyo, lo que le sirve es recuperar la cuenta y no crear otra.
            return registerForm(form).addObject("duplicateEmail", true);
        }
        AuthenticationSessions.login(user, request, response, sessionRegistry);
        return new ModelAndView("redirect:/");
    }
```

Reglas del registro en el service:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 126–160.

```java
    @Override
    @Transactional
    public User register(final String email, final String username, final String rawPassword,
                         final Locale locale) {
        final String normalizedEmail = EmailRules.normalize(email);
        final String trimmedUsername = username.trim();
        final Optional<User> existing = userDao.findByEmail(normalizedEmail);
        if (existing.isPresent() && existing.get().getPasswordHash() != null) {
            throw new DuplicateUserException();
        }

        final String passwordHash = passwordHasher.hash(rawPassword);
        final User user;
        if (existing.isPresent()) {
            final long pendingId = existing.get().getId();
            // completePending solo actualiza una cuenta sin clave: si otro registro la completo
            // entre la lectura y este update, devuelve false y este no pisa la clave elegida.
            if (!userDao.completePending(pendingId, trimmedUsername, passwordHash)) {
                throw new DuplicateUserException();
            }
            user = userDao.findById(pendingId).orElseThrow(IllegalStateException::new);
        } else {
            try {
                user = userDao.create(trimmedUsername, normalizedEmail, passwordHash, UserRole.USER,
                        SupportedLocales.languageOf(locale));
            } catch (final DuplicateKeyException e) {
                // Otro registro simultaneo del mismo correo se adelanto.
                throw new DuplicateUserException();
            }
        }

        LOGGER.info("Registered user userId={}", user.getId());
        issueVerificationToken(user, locale);
        return user;
    }
```

Verificación y reenvío:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 162–222.

```java
    @Override
    @Transactional
    public Optional<User> verifyEmail(final String token, final Locale locale) {
        if (token == null) {
            return Optional.empty();
        }
        final Optional<EmailVerificationToken> stored = verificationTokenDao.findByToken(token);
        if (stored.isEmpty()) {
            return Optional.empty();
        }
        final long userId = stored.get().getUserId();

        // markVerified solo actualiza si la cuenta sigue sin verificar: si otro request ya la
        // verifico devuelve false y la bienvenida no se manda dos veces.
        if (!userDao.markVerified(userId)) {
            return Optional.empty();
        }
        verificationTokenDao.deleteByUserId(userId);

        final User user = userDao.findById(userId).orElseThrow(IllegalStateException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Verified user email userId={}", user.getId());
            emailService.sendWelcomeEmail(user, locale);
        });
        return Optional.of(user);
    }

    /*
     * Cualquiera puede registrar un correo ajeno y pedir reenvios en bucle: si el ultimo enlace
     * se mando hace menos de RESEND_COOLDOWN no se manda otro. El anterior sigue sirviendo.
     * El lock sobre la cuenta impide que dos pedidos en paralelo pasen juntos el chequeo.
     */
    @Override
    @Transactional
    public boolean resendVerification(final long userId, final Locale locale) {
        final User user = lockById(userId);
        if (user.isVerified()) {
            return false;
        }
        final LocalDateTime cooldownStart = LocalDateTime.now().minus(RESEND_COOLDOWN);
        final boolean recentlySent = verificationTokenDao.findLatestByUserId(userId)
                .filter(latest -> latest.getCreatedAt().isAfter(cooldownStart))
                .isPresent();
        if (recentlySent) {
            LOGGER.info("Skipped verification resend inside the cooldown userId={}", userId);
            return false;
        }
        issueVerificationToken(user, locale);
        return true;
    }

    // Borra los enlaces anteriores antes de crear el nuevo: solo vale el ultimo que se mando.
    private void issueVerificationToken(final User user, final Locale locale) {
        verificationTokenDao.deleteByUserId(user.getId());
        final String token = generateToken();
        verificationTokenDao.create(user.getId(), token, LocalDateTime.now());
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Sent verification link userId={}", user.getId());
            emailService.sendVerificationEmail(user, token, locale);
        });
    }
```

Login programático, cierre de sesiones y refresco del principal:

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java>), líneas 32–74.

```java
    // Inicia sesion sin pedir la clave, recien elegida en el mismo formulario.
    public static void login(final User user, final HttpServletRequest request, final HttpServletResponse response,
                             final SessionRegistry sessionRegistry) {
        // Un id de sesion nuevo al autenticarse evita que alguien que fijo la cookie antes
        // quede adentro de la cuenta.
        if (request.getSession(false) != null) {
            request.changeSessionId();
        }
        final SecurityContext context = SecurityContextHolder.createEmptyContext();
        final Authentication authentication = authenticationFor(user, null);
        context.setAuthentication(authentication);
        SecurityContextHolder.setContext(context);
        CONTEXT_REPOSITORY.saveContext(context, request, response);
        // El form login registra la sesion solo; esta no pasa por el, asi que se registra aca
        // para poder expirarla si despues cambia la clave.
        sessionRegistry.registerNewSession(request.getSession().getId(), authentication.getPrincipal());
    }

    /*
     * Despues de cambiar o restablecer la clave: expira las otras sesiones de la cuenta y, si
     * este navegador tenia una, la cierra. Sin esto, una sesion iniciada por quien registro el
     * correo antes que su dueno seguiria adentro despues de que el dueno recupere la cuenta.
     */
    public static void logoutEverywhere(final User user, final HttpServletRequest request,
                                        final HttpServletResponse response, final SessionRegistry sessionRegistry) {
        final HttpSession currentSession = request.getSession(false);
        final String currentSessionId = currentSession == null ? null : currentSession.getId();
        sessionRegistry.getAllSessions(new AuthenticatedUser(user), false).stream()
                .filter(session -> !session.getSessionId().equals(currentSessionId))
                .forEach(SessionInformation::expireNow);
        if (currentUser().filter(current -> current.getId() == user.getId()).isPresent()) {
            LOGOUT_HANDLER.logout(request, response, SecurityContextHolder.getContext().getAuthentication());
        }
    }

    // Solo si la sesion ya es de esa cuenta: un enlace abierto en otro navegador no inicia sesion.
    public static void refreshIfCurrent(final User user) {
        currentUser().filter(current -> current.getId() == user.getId()).ifPresent(current -> {
            final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            SecurityContextHolder.getContext().setAuthentication(
                    authenticationFor(user, authentication.getDetails()));
        });
    }
```

Authorities del principal:

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>), líneas 38–49.

```java
    // El administrador conserva lo que puede hacer una cuenta comun y le suma administracion.
    private static List<GrantedAuthority> authoritiesFor(final User user) {
        final List<GrantedAuthority> granted = new ArrayList<>();
        if (user.getRole() == UserRole.ADMIN) {
            granted.add(ROLE_ADMIN);
        }
        granted.add(ROLE_USER);
        if (user.isVerified()) {
            granted.add(VERIFIED_AUTHORITY);
        }
        return List.copyOf(granted);
    }
```

Form login, logout y sesiones:

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>), líneas 124–152.

```java
    @Bean
    public SecurityFilterChain securityFilterChain(final HttpSecurity http, final SessionRegistry sessionRegistry)
            throws Exception {
        http
                .authorizeHttpRequests(authorize -> authorize
                        .requestMatchers(VERIFIED_PATHS).hasAuthority(AuthenticatedUser.VERIFIED)
                        .antMatchers("/verify/resend", "/verify/required").authenticated()
                        .anyRequest().permitAll())
                .formLogin(login -> login
                        .loginPage("/login")
                        .usernameParameter("email")
                        .passwordParameter("password")
                        .defaultSuccessUrl("/", false)
                        .failureUrl("/login?error")
                        .permitAll())
                .logout(logout -> logout
                        .logoutUrl("/logout")
                        .logoutSuccessUrl("/login?logout")
                        .invalidateHttpSession(true)
                        .deleteCookies("JSESSIONID"))
                // Sin limite de sesiones por cuenta: el registro solo sirve para expirarlas.
                .sessionManagement(session -> session
                        .maximumSessions(-1)
                        .sessionRegistry(sessionRegistry)
                        .expiredUrl("/login?sessionExpired"))
                .exceptionHandling(exceptions -> exceptions.accessDeniedHandler(
                        new VerificationAccessDeniedHandler(VERIFIED_PATHS, FORBIDDEN_PAGE)));
        return http.build();
    }
```

Los dos `UPDATE` condicionales:

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>), líneas 118–129.

```java
    @Override
    public boolean completePending(final long id, final String username, final String passwordHash) {
        // El UPDATE condicional hace que solo el primer registro complete la cuenta pendiente:
        // despues la fila ya tiene clave y un segundo registro no la pisa.
        return jdbcTemplate.update("UPDATE users SET username = ?, password_hash = ? "
                        + "WHERE id = ? AND password_hash IS NULL", username, passwordHash, id) == 1;
    }

    @Override
    public boolean markVerified(final long id) {
        return jdbcTemplate.update("UPDATE users SET verified = TRUE WHERE id = ? AND verified = FALSE", id) == 1;
    }
```

Banner de la cabecera:

Fuente exacta en `c3e2a4c`: [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>), líneas 41–55.

```jsp
    <%-- Mientras la cuenta no abra el enlace, cada pagina le recuerda que le falta verificar. --%>
    <sec:authorize access="isAuthenticated() and !principal.verified">
        <div class="verification-banner" role="status">
            <div class="verification-banner__inner">
                <p class="verification-banner__text">
                    <c:choose>
                        <c:when test="${verificationResent}"><spring:message code="auth.verification.resent"/></c:when>
                        <c:when test="${verificationThrottled}"><spring:message code="auth.verification.throttled"/></c:when>
                        <c:otherwise><spring:message code="auth.verification.banner"/></c:otherwise>
                    </c:choose>
                </p>
                <ui:resend-verification variant="ghost"/>
            </div>
        </div>
    </sec:authorize>
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>) · [[AuthenticationController]]
- [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) · [[UserServiceImpl]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>) · [[SecurityConfig]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java>) · [[AuthenticationSessions]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUser.java>) · [[AuthenticatedUser]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticatedUserDetailsService.java>) · [[AuthenticatedUserDetailsService]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>) · [[VerificationAccessDeniedHandler]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java>) · [[SameSiteRedirects]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/form/RegisterForm.java>) · [[RegisterForm]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>) · [[UserJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>) · [[EmailVerificationTokenJdbcDao]]
- [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>)
- [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>)

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
