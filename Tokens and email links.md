---
title: "Tokens and email links"
categories: ["Services", "Persistence", "Flows"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java", "models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java", "models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java", "persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java", "persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java", "persistence/src/main/resources/db/migration/V1__esquema_inicial.sql", "persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql", "services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java"]
---

# Tokens and email links

> [!summary] En una frase
> Un token acá es una cadena aleatoria de 256 bits que el servidor guarda en una tabla y manda dentro de un enlace: quien presenta el enlace demuestra que lee esa casilla. No es un JWT ni lleva datos adentro.

En la defensa del sprint 2 se preguntó por "el token". En el proyecto hay cuatro cosas a las que se les puede decir así, y conviene separarlas antes de contestar.

| Nombre | Qué es | Dónde vive | Quién lo genera |
|---|---|---|---|
| Token de verificación | Cadena aleatoria que va en `/verify?token=` | Tabla `email_verification_tokens` | [[UserServiceImpl]] |
| Token de recuperación | Cadena aleatoria que va en `/reset-password?token=` | Tabla `password_reset_tokens` | [[UserServiceImpl]] |
| Id de sesión | Valor de la cookie `JSESSIONID` | Memoria del contenedor (la `HttpSession`) | El contenedor de servlets |
| Token CSRF | Campo oculto `_csrf` de cada formulario POST | Atributo de la sesión HTTP | Spring Security |

Los dos primeros son código del equipo y son el tema de esta nota. Los otros dos son del framework y están en [[Security and authorization]].

## Herramientas

| Herramienta | Para qué |
|---|---|
| `java.security.SecureRandom` | Fuente de aleatoriedad criptográfica para los 32 bytes |
| `Base64.getUrlEncoder().withoutPadding()` | Pasar los bytes a texto que entra en una URL sin escapar (`A-Z a-z 0-9 - _`) |
| Spring JDBC (`SimpleJdbcInsert`, `JdbcTemplate`) | Guardar, buscar y borrar tokens |
| Restricciones `UNIQUE` de PostgreSQL | Garantizar un token por valor y, en recuperación, uno por Cuenta |
| `@Transactional` | Que emitir o consumir un token sea atómico con el cambio de la Cuenta |
| `java.time.Duration` / `LocalDateTime` | Vencimiento del enlace de recuperación y tope de reenvío |

## Cómo se genera

`generateToken()` pide 32 bytes a `SecureRandom` y los codifica en Base64 para URL sin relleno. Son 256 bits de entropía y 43 caracteres de texto. La columna `token` es `VARCHAR(64)`, así que sobra lugar. No lleva el id de la Cuenta, ni fecha, ni firma: es opaco. Toda la información asociada (de quién es, cuándo se creó, cuándo vence) está en la fila de la tabla.

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 36–45.

```java
    // 32 bytes aleatorios: adivinar un enlace de verificacion no es viable por fuerza bruta.
    private static final int TOKEN_BYTES = 32;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    // A diferencia del de verificacion, el enlace de recuperacion abre una cuenta que ya
    // esta en uso: se limita la ventana en la que sirve si el correo queda expuesto.
    private static final Duration RESET_TOKEN_TTL = Duration.ofHours(1);

    // Tiempo minimo entre dos enlaces de verificacion pedidos con el boton de reenviar.
    private static final Duration RESEND_COOLDOWN = Duration.ofMinutes(1);
```

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 354–358.

```java
    private static String generateToken() {
        final byte[] bytes = new byte[TOKEN_BYTES];
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
```

El enlace lo arma [[EmailServiceImpl]] concatenando `app.base-url` con la ruta y el token. La URL base tiene que ser absoluta y viene de configuración porque el envío corre en un hilo sin request (ver [[Mail delivery]]).

## Los dos tokens, lado a lado

| | Verificación | Recuperación |
|---|---|---|
| Tabla | `email_verification_tokens` | `password_reset_tokens` |
| Columnas | `id`, `user_id`, `token`, `created_at` | `id`, `user_id`, `token`, `expires_at` |
| Qué demuestra | Que la persona lee esa casilla | Lo mismo, y además autoriza a cambiar la clave |
| Quién lo dispara | `register`, `resendVerification` | `requestPasswordReset` |
| Vence | No | A la hora (`RESET_TOKEN_TTL`) |
| Cuántos vivos por Cuenta | A lo sumo uno, por borrar antes de crear. El esquema no lo impide | Exactamente uno: `UNIQUE (user_id)` |
| Se consume con | `verifyEmail`: `markVerified` condicional y `deleteByUserId` | `resetPassword`: `deleteByToken` que tiene que afectar una fila |
| Se invalida además cuando | Se pide otro; se completa una recuperación de contraseña | Se pide otro; vence |
| Limpieza de viejos | No hace falta: no se acumulan | `deleteExpired(now)` en cada pedido nuevo, de cualquier Cuenta |
| Freno al abuso | Un minuto entre reenvíos (`RESEND_COOLDOWN`), con la fila de la Cuenta bloqueada | Un enlace por Cuenta; el pedido responde igual exista o no la Cuenta |
| Inicia sesión | No | No: después hay que loguearse con la clave nueva |
| Efecto sobre sesiones | Refresca el principal si es la misma Cuenta | Cierra todas las sesiones de la Cuenta |

## Ciclo de vida

```mermaid
stateDiagram-v2
    direction LR
    state "Verificación" as V {
        [*] --> Vivo: register / resend
        Vivo --> Reemplazado: resend (borra y crea)
        Vivo --> Usado: GET /verify
        Vivo --> Borrado: resetPassword de la Cuenta
        Reemplazado --> [*]
        Usado --> [*]
        Borrado --> [*]
    }
    state "Recuperación" as R {
        [*] --> Activo: forgot-password
        Activo --> Sustituido: otro forgot-password
        Activo --> Vencido: pasa una hora
        Activo --> Consumido: POST /reset-password
        Vencido --> Purgado: próximo forgot-password
        Sustituido --> [*]
        Consumido --> [*]
        Purgado --> [*]
    }
```

En los dos casos "usado" significa que la fila se borra: no hay columna `used`. Un enlace usado y uno inexistente son indistinguibles, y la pantalla muestra el mismo mensaje.

## Esquema

Tablas originales, de la migración V1:

Fuente exacta en `c3e2a4c`: [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>), líneas 21–37.

```sql
CREATE TABLE email_verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    CONSTRAINT email_verification_tokens_token_key UNIQUE (token),
    CONSTRAINT email_verification_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    CONSTRAINT password_reset_tokens_token_key UNIQUE (token),
    CONSTRAINT password_reset_tokens_user_id_key UNIQUE (user_id),
    CONSTRAINT password_reset_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);
```

La fecha del enlace de verificación llegó en V6, junto con el cambio de nombre de `enabled` a `verified`:

Fuente exacta en `c3e2a4c`: [persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql>), líneas 1–9.

```sql
-- La columna enabled siempre guardo si la cuenta verifico su correo: desde que la cuenta
-- existe al registrarse, una cuenta sin verificar tambien inicia sesion, y el nombre viejo
-- confundia. Se renombra sin tocar los datos.
ALTER TABLE users RENAME COLUMN enabled TO verified;

-- Cuando se mando cada enlace de verificacion: el reenvio se frena si el ultimo es muy
-- reciente, asi nadie puede llenar de correos la casilla de otro. Los enlaces que ya
-- existian quedan con la fecha de la migracion.
ALTER TABLE email_verification_tokens ADD COLUMN created_at TIMESTAMP DEFAULT NOW() NOT NULL;
```

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| Token opaco guardado en la base | JWT firmado sin estado | Se necesita un solo uso y poder invalidarlo al pedir otro; con estado en la base eso es un `DELETE` | Inferencia a partir del diseño; el código no menciona JWT |
| 32 bytes de `SecureRandom` | UUID o un contador | Que adivinar un enlace por fuerza bruta no sea viable | Comentario en [[UserServiceImpl]] |
| El de recuperación vence a la hora y el de verificación no | Vencimiento en los dos | El de recuperación abre una Cuenta que ya está en uso: se acota la ventana si el correo queda expuesto. El vencimiento de verificación quedó explícitamente fuera de alcance | Comentario en [[UserServiceImpl]]; "Out of Scope" del issue del sprint 2 |
| El vencimiento lo calcula el service | `DEFAULT now() + interval` en la tabla | La ventana es una regla de negocio, no del almacenamiento | Comentario en [[PasswordResetTokenJdbcDao]] |
| `UNIQUE (user_id)` en recuperación | Solo borrar antes de insertar | Dos pedidos simultáneos borran cero filas cada uno y llegarían los dos al insert; la restricción hace perder a uno | Comentario en [[UserServiceImpl]] |
| Consumir con `DELETE` y exigir una fila afectada | Leer, usar y borrar al final | Dos requests con el mismo token no pueden pisarse la clave | Comentario en [[UserServiceImpl]] |
| Rechazar "misma clave" antes de consumir el enlace | Consumir primero | Quien elige la clave que ya tenía puede reintentar con el mismo correo | Comentario en [[UserServiceImpl]] |
| La recuperación también verifica la Cuenta | Exigir verificación aparte | El enlace llegó al correo: demuestra lo mismo que el de verificación | Comentario en [[UserServiceImpl]] |
| Guardar el token en claro | Guardar solo su hash | El commit `a8468071` (16/9) quitó el SHA-256 que tenía el token de verificación para simplificar el flujo | Historial de Git |

## Concurrencia

- **Dos `forgot-password` a la vez para la misma Cuenta**: el segundo insert viola `UNIQUE (user_id)`, se captura `DuplicateKeyException` y ese pedido termina sin mandar nada. Queda un enlace y un correo.
- **Dos `reset-password` con el mismo token**: el primero borra la fila; el segundo ve cero filas afectadas y devuelve "enlace inválido".
- **Dos `verify` con el mismo token**: el `UPDATE ... AND verified = FALSE` afecta filas una sola vez; la bienvenida sale una vez.
- **Dos reenvíos a la vez**: `lockById` bloquea la fila de la Cuenta y los ordena.

## Límites conocidos

- **Token en claro en la base.** Quien lea la tabla puede usar un enlace de recuperación vigente (a lo sumo una hora) o verificar una Cuenta ajena. Guardar el hash lo evitaría.
- **El token viaja en la URL.** Queda en el historial del navegador y puede aparecer en logs de proxies. El de recuperación es de un solo uso y vence; el formulario lo reenvía como campo oculto escapado con `c:out`.
- **La verificación es un `GET` que cambia estado.** Un cliente de correo que precargue enlaces podría verificar la Cuenta sin que la persona haga clic. El efecto es acotado: solo marca el correo como verificado.
- **Sin tope a los pedidos de recuperación.** Cada pedido reemplaza el enlace y manda un correo; no hay un minuto de espera como en el reenvío de verificación.
- **`LocalDateTime` sin zona.** El vencimiento se compara contra el reloj del servidor de aplicación.
- La limpieza de vencidos depende de que alguien pida una recuperación; no hay tarea programada.

Los primeros cuatro puntos son análisis sobre el código leído, no fallas observadas en ejecución.

## Preguntas de defensa

**¿El token es un JWT?**
No. Es un valor aleatorio sin contenido. El servidor lo busca en una tabla para saber de quién es.

**¿Qué pasa si pido dos enlaces de verificación?**
El segundo borra al primero: solo sirve el último. Y si pasó menos de un minuto no se manda otro.

**¿Por qué el de recuperación vence y el de verificación no?**
Porque el de recuperación permite cambiar la clave de una Cuenta en uso. El de verificación solo marca el correo como verificado, y su vencimiento se dejó fuera de alcance.

**¿Se puede usar dos veces un enlace de recuperación?**
No. Se borra dentro de la misma transacción que cambia la clave, y el borrado tiene que afectar exactamente una fila.

**¿Cómo evitan que el formulario de "olvidé mi contraseña" revele qué correos existen?**
El controller redirige siempre al mismo lugar. El service decide en silencio si manda algo, y loguea sin el correo.

**¿Qué pasa con las sesiones abiertas cuando se cambia la clave?**
Se expiran todas las de esa Cuenta a través del `SessionRegistry`, y la del navegador actual se cierra.

**¿Dónde se arma la URL del enlace?**
En [[EmailServiceImpl]], con `app.base-url` de `mail.properties`. Tiene que incluir el context path del servidor de la cátedra.

## Evidencia de código

Emisión del token de verificación:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 213–222.

```java
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

Emisión del token de recuperación:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 260–292.

```java
    @Override
    @Transactional
    public void requestPasswordReset(final String email, final Locale locale) {
        final Optional<User> found = userDao.findByEmail(EmailRules.normalize(email));
        if (found.isEmpty() || found.get().getPasswordHash() == null) {
            LOGGER.info("Ignored password reset request for an unknown or pending account");
            return;
        }
        final User user = found.get();
        final LocalDateTime now = LocalDateTime.now();

        // Un enlace vencido no vuelve a servir y nadie mas lo saca de la tabla: el pedido
        // aprovecha para limpiar los que quedaron atras, sean de quien sean.
        resetTokenDao.deleteExpired(now);

        // Un solo enlace vivo por cuenta: pedir otro deja sin efecto al anterior. La
        // invariante la sostiene la unicidad de user_id, porque dos pedidos simultaneos
        // borran cero filas cada uno y llegarian los dos al insert.
        resetTokenDao.deleteByUserId(user.getId());
        final String token = generateToken();
        try {
            resetTokenDao.create(user.getId(), token, now.plus(RESET_TOKEN_TTL));
        } catch (final DuplicateKeyException e) {
            // Otro pedido simultaneo para la misma cuenta ya dejo vivo su enlace: con ese
            // correo alcanza, asi que este termina sin enviar nada.
            LOGGER.info("Skipped a concurrent password reset request userId={}", user.getId());
            return;
        }
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Sent password reset link userId={}", user.getId());
            emailService.sendPasswordResetEmail(user, token, locale);
        });
    }
```

Consumo del token de recuperación:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>), líneas 294–328.

```java
    @Override
    @Transactional
    public Optional<User> resetPassword(final String token, final String newPassword, final Locale locale) {
        if (token == null) {
            return Optional.empty();
        }
        final Optional<PasswordResetToken> stored = resetTokenDao.findByToken(token);
        if (stored.isEmpty() || stored.get().getExpiresAt().isBefore(LocalDateTime.now())) {
            return Optional.empty();
        }
        final long userId = stored.get().getUserId();

        // Mismo criterio que changePassword. Se rechaza antes de reclamar el enlace para que
        // quien elija la clave que ya tenia pueda reintentar con el mismo correo.
        final User current = userDao.findById(userId).orElseThrow(UserNotFoundException::new);
        if (passwordHasher.matches(newPassword, current.getPasswordHash())) {
            throw new UnchangedPasswordException();
        }

        // Reclamar el enlace dentro de la transaccion antes de tocar la clave impide que dos
        // requests concurrentes que leyeron el mismo token lo usen para pisarse entre si.
        if (resetTokenDao.deleteByToken(token) != 1) {
            return Optional.empty();
        }
        // El enlace llego al correo, asi que demuestra lo mismo que el de verificacion.
        userDao.markVerified(userId);
        verificationTokenDao.deleteByUserId(userId);
        final User updated = userDao.updatePassword(userId, passwordHasher.hash(newPassword))
                .orElseThrow(UserNotFoundException::new);
        TransactionCallbacks.afterCommit(() -> {
            LOGGER.info("Reset password userId={}", userId);
            emailService.sendPasswordChangedEmail(updated, locale);
        });
        return Optional.of(updated);
    }
```

DAO de recuperación:

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java>), líneas 46–85.

```java
    @Override
    public PasswordResetToken create(final long userId, final String token, final LocalDateTime expiresAt) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("token", token);
        parameters.put("expires_at", Timestamp.valueOf(expiresAt));
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new PasswordResetToken(id.longValue(), userId, token, expiresAt);
    }

    /*
     * Devuelve el token aunque este vencido: quien decide si todavia sirve es el service.
     */
    @Override
    public Optional<PasswordResetToken> findByToken(final String token) {
        return jdbcTemplate.query(SELECT + "WHERE token = ?", ROW_MAPPER, token)
                .stream()
                .findAny();
    }

    @Override
    public int deleteByToken(final String token) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE token = ?", token);
    }

    @Override
    public int deleteByUserId(final long userId) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE user_id = ?", userId);
    }

    /*
     * Igual que en create, el corte llega del service: el DAO solo borra lo que quedo atras.
     */
    @Override
    public int deleteExpired(final LocalDateTime now) {
        return jdbcTemplate.update("DELETE FROM password_reset_tokens WHERE expires_at < ?",
                Timestamp.valueOf(now));
    }

}
```

DAO de verificación:

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>), líneas 43–74.

```java
    @Override
    public EmailVerificationToken create(final long userId, final String token, final LocalDateTime createdAt) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("token", token);
        parameters.put("created_at", Timestamp.valueOf(createdAt));
        final Number id = jdbcInsert.executeAndReturnKey(parameters);
        return new EmailVerificationToken(id.longValue(), userId, token, createdAt);
    }

    @Override
    public Optional<EmailVerificationToken> findByToken(final String token) {
        return jdbcTemplate.query(SELECT + "WHERE token = ?", ROW_MAPPER, token)
                .stream()
                .findAny();
    }

    // Normalmente hay uno solo por cuenta, pero nada en el esquema impide que haya mas.
    @Override
    public Optional<EmailVerificationToken> findLatestByUserId(final long userId) {
        return jdbcTemplate.query(SELECT + "WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT 1",
                        ROW_MAPPER, userId)
                .stream()
                .findFirst();
    }

    @Override
    public int deleteByUserId(final long userId) {
        return jdbcTemplate.update("DELETE FROM email_verification_tokens WHERE user_id = ?", userId);
    }

}
```

Armado de los enlaces:

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>), líneas 74–89.

```java
    @Async
    @Override
    public void sendVerificationEmail(final User user, final String token, final Locale locale) {
        try {
            final Context context = new Context(locale);
            context.setVariable("verificationUrl", baseUrl + "/verify?token=" + token);
            final String body = templateEngine.process(VERIFICATION_TEMPLATE, context);
            final String subject = messageSource.getMessage("email.verification.subject", null, locale);
            final MimeMessage message = createMessage(user.getEmail(), null, subject, body);

            mailSender.send(message);
            LOGGER.info("Verification email sent userId={}", user.getId());
        } catch (final MessagingException | RuntimeException exception) {
            LOGGER.error("Verification email delivery failed userId={}", user.getId(), exception);
        }
    }
```

## Archivos para seguir el flujo

- [services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/UserServiceImpl.java>) · [[UserServiceImpl]]
- [models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java>) · [[EmailVerificationToken]]
- [models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java>) · [[PasswordResetToken]]
- [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java>) · [[EmailVerificationTokenDao]]
- [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java>) · [[PasswordResetTokenDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenJdbcDao.java>) · [[EmailVerificationTokenJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenJdbcDao.java>) · [[PasswordResetTokenJdbcDao]]
- [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>)
- [persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql>)
- [services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/EmailServiceImpl.java>) · [[EmailServiceImpl]]

Fuente inspeccionada: `c3e2a4c`, 2026-10-05. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
