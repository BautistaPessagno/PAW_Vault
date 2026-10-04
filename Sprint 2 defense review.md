---
title: "Sprint 2 defense review"
categories: ["History", "Navigation"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
tags: ["codemap", "navigation"]
sources: ["docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java", "services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java", "models/src/main/java/ar/edu/itba/paw/models/Post.java", "models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java", "webapp/src/main/webapp/js/autocomplete.js", "webapp/src/main/webapp/js/submit-once.js", "webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java", "persistence/src/main/resources/db/migration/V1__esquema_inicial.sql"]
---

# Sprint 2 defense review

> [!summary] En una frase
> Qué se observó en la defensa del sprint 2 (23 de septiembre) y en qué estado está cada punto en `8929aea`: la mayoría está resuelta, y quedan pendientes el tipo de dato del dinero, el plazo para el comprobante y tres puntos de seguridad que conviene poder explicar.

## Fuentes

| Fuente | Qué aporta | Límite |
|---|---|---|
| Nota "Sprint 2 defensa" de Wispr Flow, 23 de septiembre, 20:26 | Resumen de la reunión: observaciones, próximos pasos y decisiones | Es un resumen generado automáticamente a partir de la grabación. Se leyó el resumen completo; **no** la transcripción, así que puede faltar detalle o matiz |
| `docs/issues/observaciones-sprint-2/` en el repositorio | Las cuatro observaciones que el equipo formalizó y cómo decidió resolverlas | Cubre solo cuenta, búsqueda vacía, sugerencias y autorización |
| [[TODO cambios]] | Apuntes personales tomados después de la defensa | Muy breves |

El estado de cada punto sale de leer el código en `8929aea`. Nada se verificó en ejecución.

## Cuenta y verificación

| Observación | Estado | Qué hay en el código | Nota |
|---|---|---|---|
| La verificación por correo debería llegar después de crear la cuenta, sin bloquear el flujo inicial | **Resuelto** | El registro crea la cuenta con contraseña y la deja con sesión iniciada; el enlace llega después (PR #43, `0870c81d`) | [[Authentication flow]] |
| Después de verificar y crear la contraseña, iniciar sesión automáticamente en vez de pedir login otra vez | **Resuelto** | Registrarse deja la sesión abierta. Abrir el enlace actualiza la sesión en curso para que tenga `VERIFIED`. La recuperación de contraseña sí pide login de nuevo, a propósito: cierra todas las sesiones de la cuenta | [[Authentication flow]], [[Password recovery flow]] |
| Todos los correos llegaron en inglés; falta soporte en español | **A confirmar en ejecución** | Los correos se escriben en el idioma del request (verificación, recuperación) o en el guardado en la cuenta al registrarse (avisos), con español por defecto. Si el navegador declara inglés, llegan en inglés: es el comportamiento buscado, pero conviene probarlo con un navegador en español | [[Mail delivery]], [[Localization]] |

## Venta

| Observación | Estado | Qué hay en el código | Nota |
|---|---|---|---|
| Falta un estado intermedio entre aceptar y concretar la venta, tipo "pendiente de comprobante" | **Resuelto** | `AWAITING_PAYMENT` y `PAYMENT_SUBMITTED` (PR #42) | [[Inquiry and sale flow]] |
| Mientras se espera el pago, bloquear las otras ofertas | **Resuelto** | Aceptar reserva el Post (`RESERVED`); las demás consultas quedan pendientes y no se pueden aceptar | [[Inquiry and sale flow]] |
| Si el comprobante no llega en cierto tiempo, reanudar y reabrir las otras ofertas | **Pendiente** | No hay plazo ni tarea programada. El Post queda reservado hasta que una de las partes cancela | [[Known gaps and document drift]] |
| Estructurar el flujo en pasos: aceptar, subir comprobante, aceptar comprobante, coordinar entrega | **Resuelto** | La página de la venta muestra la acción que toca según estado y papel | [[Inquiry and sale flow]] |
| Mantener un chat en paralelo para coordinar | **Resuelto** | Conversación dentro de cada consulta, con aviso por correo (PR #45) | [[Conversation flow]] |

## Dinero

| Observación | Estado | Qué hay en el código | Nota |
|---|---|---|---|
| Usar `BigDecimal` para el dinero, en base, modelo y cliente | **Pendiente** | El precio es `int` en los modelos e `INTEGER` en `posts` e `inquiries`. No hay ningún uso de `BigDecimal` en el repositorio | [[Database schema]] |
| Base, modelo y cliente deben manejar la misma precisión | **Coincide, sin decimales** | Las tres capas usan pesos enteros, de 1 a 99.999.999 ([[VinylInputRules]]) | [[Publish flow]] |

El resumen de la reunión registra como decisión que "se usará BigDecimal para todo el manejo de dinero". En `8929aea` no está aplicado. Con precios enteros no hay pérdida de precisión, que era el riesgo que se señaló, pero si se vuelve a preguntar hay que poder decir cuál de las dos cosas se eligió y por qué.

## Búsqueda, autocompletado y validaciones

| Observación | Estado | Qué hay en el código | Nota |
|---|---|---|---|
| Cada tecla hace un request al servidor; considerar mover lógica al cliente | **Parcial** | El script espera 150 ms sin teclas antes de pedir y descarta respuestas viejas por número de secuencia. Sigue consultando al servidor en cada pausa; no hay caché en el cliente | [[Search suggestions flow]] |
| Guardar el nombre original y el normalizado para buscar sin tildes | **Resuelto** | `normalized_name` y `search_phrase` en artistas y álbumes; la búsqueda enviada usa la misma normalización que las sugerencias (`a4c39048`) | [[Landing flow]] |
| Validar tipo y tamaño de los archivos subidos | **Resuelto** | Fotos: tipo, tamaño y firma del contenido, en el formulario y en el service. Comprobantes: tipo y tamaño; la firma solo se valida en PDF | [[Cover image flow]], [[Inquiry and sale flow]] |
| El service recorta espacios y valida el largo antes de llegar al DAO | **Vigente** | Normalización con [[SearchText]] y reglas en `models` | [[Validation and errors]] |

## Seguridad

| Observación | Estado | Qué hay en el código | Nota |
|---|---|---|---|
| No exponer si un usuario existe | **Parcial** | "Olvidé mi contraseña" responde igual exista o no la cuenta. El **registro** sí informa que el correo ya tiene cuenta | [[Password recovery flow]], [[Authentication flow]] |
| Recuperación con enlace por correo, de un solo uso y con vencimiento | **Resuelto** | Token aleatorio, una hora de vida, un solo enlace vivo por cuenta, se consume en la misma transacción que cambia la clave | [[Tokens and email links]] |
| Validar el token antes de permitir cambiar la contraseña | **Parcial** | El token se valida al **enviar** el formulario. `GET /reset-password` muestra el formulario sin comprobar que el token exista o esté vigente | [[Password recovery flow]] |
| Centralizar la seguridad de los endpoints en la configuración web o distribuirla con anotaciones, pero no mezclar | **Resuelto con un criterio, no con un solo mecanismo** | Siguen conviviendo dos mecanismos, cada uno con una responsabilidad: las reglas por URL de [[SecurityConfig]] deciden si hace falta cuenta verificada; `@PreAuthorize` decide si el recurso es de quien pregunta | [[Security and authorization]] |
| Bloquear los botones después de enviar, para evitar duplicados por doble clic | **Resuelto** | `submit-once.js` deshabilita los botones; además la base y el service rechazan el duplicado | [[Views and assets]], [[Publish flow]] |

Sobre la mezcla de mecanismos: la observación pedía no mezclar, y el equipo resolvió con "un criterio por capa". Es defendible, pero es el punto con más riesgo de volver a aparecer. La respuesta corta: la URL responde **quién sos** (sesión, verificación) y la anotación responde **si esto es tuyo** (pertenencia), y ninguna regla está en los dos lugares.

## Resumen del estado

| Estado | Puntos |
|---|---|
| Resuelto | 10 |
| Parcial | 4: request por pausa de tecleo, existencia de cuenta en el registro, token no validado al abrir el formulario, dos mecanismos de autorización |
| Pendiente | 2: `BigDecimal` para el dinero, plazo para el comprobante |
| A confirmar en ejecución | 1: idioma de los correos |
| Vigente o coincidente desde antes | 2 |

## Qué preparar para la próxima defensa

1. **Dinero.** Decidir si se migra a `BigDecimal` o se defiende el entero, y por qué.
2. **Plazo del comprobante.** Decidir si se implementa el vencimiento de la reserva o se explica por qué la cancelación manual alcanza.
3. **Autorización.** Poder decir en una frase el criterio de cada capa.
4. **Registro y existencia de cuenta.** Saber explicar por qué el registro informa el duplicado y la recuperación no.
5. **Correo, autenticación y token por dentro.** Los tres relatos de [[Defense guide]] cubren lo que se preguntó sobre cómo funcionan.

## Evidencia de código

### El precio es un entero

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java>), líneas 11–12.

```java
    public static final int MIN_PRICE = 1;
    public static final int MAX_PRICE = 99_999_999;
```

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>), líneas 70–74.

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
```

### El formulario de nueva contraseña se muestra sin validar el token

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>), líneas 144–149.

```java
    @RequestMapping(value = "/reset-password", method = RequestMethod.GET)
    public ModelAndView resetPasswordForm(@RequestParam(name = "token", required = false) final String token,
                                          @ModelAttribute("resetPasswordForm") final ResetPasswordForm form) {
        form.setToken(token);
        return new ModelAndView("auth/reset-password");
    }
```

### La recuperación responde igual exista o no la cuenta

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>), líneas 130–142.

```java
    /*
     * Redirige igual exista o no la cuenta: si respondiera distinto, el formulario serviria
     * para averiguar que correos estan registrados. Quien decide a quien escribirle es el service.
     */
    @RequestMapping(value = "/forgot-password", method = RequestMethod.POST)
    public ModelAndView forgotPassword(@Valid @ModelAttribute("forgotPasswordForm") final ForgotPasswordForm form,
                                       final BindingResult bindingResult, final Locale locale) {
        if (bindingResult.hasErrors()) {
            return forgotPasswordForm(form);
        }
        userService.requestPasswordReset(form.getEmail(), locale);
        return new ModelAndView("redirect:/login?resetLinkSent");
    }
```

### El registro informa el correo duplicado

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>), líneas 79–85.

```java
        try {
            user = userService.register(form.getEmail(), form.getUsername(), form.getPassword(), locale);
        } catch (final DuplicateUserException e) {
            bindingResult.rejectValue("email", "auth.register.email.duplicate");
            // Si el correo es suyo, lo que le sirve es recuperar la cuenta y no crear otra.
            return registerForm(form).addObject("duplicateEmail", true);
        }
```

### Espera antes de pedir sugerencias

Fuente exacta en `8929aea`: [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>), líneas 5–5.

```javascript
    var SEARCH_DELAY_MS = 150;
```

## Archivos para seguir el flujo

- [docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/AuthenticationController.java>) · [[AuthenticationController]]
- [services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/InquiryServiceImpl.java>) · [[InquiryServiceImpl]]
- [models/src/main/java/ar/edu/itba/paw/models/Post.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/Post.java>) · [[Post]]
- [models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/VinylInputRules.java>) · [[VinylInputRules]]
- [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>)
- [webapp/src/main/webapp/js/submit-once.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>)
- [webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/config/SecurityConfig.java>) · [[SecurityConfig]]

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
