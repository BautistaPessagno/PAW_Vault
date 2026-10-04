> [!summary] En una frase
> Banco de preguntas para preparar una defensa: tres relatos cortos de los temas que más costaron en el sprint 2 (cuenta, token, correo) y un índice de todas las preguntas del vault con enlace a su respuesta.

## Cómo usar esta nota

1. Leé cada relato y repetilo en voz alta sin mirar. Si te trabás, abrí la nota enlazada.
2. Recorré el índice por tema. Cada pregunta enlaza a la nota donde está respondida, con el código que la respalda.
3. Para cualquier pregunta, la respuesta completa tiene cuatro partes: **qué herramienta** se usa, **qué pasa paso a paso**, **por qué se decidió así** y **qué límite tiene**. Las notas de flujo están armadas con esas cuatro secciones.

En la defensa del sprint 2 las preguntas apuntaron a cómo funcionan por dentro el correo, la autenticación y el token. [[Sprint 2 defense review]] recorre cada observación de esa defensa y su estado actual, a partir del resumen de la grabación y del issue `docs/issues/observaciones-sprint-2/`. Antes de practicar, leé ahí la sección "Qué preparar para la próxima defensa".

## Relato 1: qué pasa cuando alguien se registra

1. `POST /register` llega a [[AuthenticationController]]. Spring liga el [[RegisterForm]] y Bean Validation revisa correo, nombre y contraseña (12 a 72 caracteres, una letra y un número, y que la repetición coincida).
2. El controller llama a `UserService.register`, que es `@Transactional`. El service normaliza el correo, rechaza un correo que ya tiene contraseña, **hashea la contraseña con BCrypt de costo 12** y crea la fila en `users` con `verified = false` y el idioma del navegador.
3. En la misma transacción genera un **token de verificación** y lo guarda.
4. Registra el envío del correo para **después del commit**.
5. De vuelta en el controller, la cuenta queda **con sesión iniciada sin pasar por el login**: se arma el `Authentication`, se cambia el id de sesión, se guarda el `SecurityContext` en la `HttpSession` y se anota la sesión en el `SessionRegistry`.
6. La cuenta puede navegar, pero las rutas que operan (publicar, perfil, consultas, carrito) exigen la autoridad `VERIFIED`. Sin ella, [[VerificationAccessDeniedHandler]] la manda a la pantalla de verificación pendiente.
7. Al abrir el enlace, `GET /verify?token=...` busca el token, marca `verified = true` con un `UPDATE` condicional, borra los tokens de esa cuenta y manda la bienvenida después del commit. Si hay sesión abierta, se actualiza el principal para que tenga `VERIFIED` sin volver a loguearse.

Por qué así: la cátedra observó que el registro anterior estaba al revés (verificar antes de crear la cuenta). Detalle en [[Authentication flow]].

## Relato 2: qué es el token y cómo se usa

- **Qué es.** 32 bytes de `SecureRandom` codificados en Base64 para URL, sin relleno: 43 caracteres. No es un JWT: no lleva datos adentro. El servidor lo busca en una tabla para saber de qué cuenta es.
- **Dónde se guarda.** En `email_verification_tokens` o `password_reset_tokens`, en claro, con una restricción de unicidad.
- **Cómo viaja.** En la URL de un enlace que se manda por correo. La URL se arma con `app.base-url`.
- **Cómo se consume.** El de verificación se borra al verificar. El de recuperación se borra en la misma transacción que cambia la contraseña, y el borrado tiene que afectar exactamente una fila: si dos pedidos llegan a la vez, uno solo gana.
- **Cuánto dura.** El de recuperación, una hora. El de verificación no vence, pero pedir uno nuevo invalida el anterior, y no se puede pedir otro antes de un minuto.
- **Qué límite tiene.** Se guarda en claro: quien lea la tabla puede usar un enlace vigente.

Detalle en [[Tokens and email links]] y [[Password recovery flow]].

## Relato 3: cómo sale un correo

1. Un service, dentro de su transacción, decide que hay que avisar algo. No lo manda: lo **registra para después del commit** con [[TransactionCallbacks]]. Si la transacción se revierte, no sale nada.
2. Tras el commit se llama a un método de [[EmailServiceImpl]] marcado `@Async`. Spring lo entrega a un **pool de hilos** (2 a 5 hilos, cola de 50) y el request responde sin esperar.
3. El `Locale` se resolvió **antes**, en el hilo del request, y viaja como parámetro: en el hilo del pool no hay request.
4. El hilo del pool arma el HTML con **Thymeleaf** (las JSP necesitan un request; Thymeleaf produce un `String`), toma los textos del mismo `MessageSource` y arma los enlaces con `app.base-url`.
5. `JavaMailSender` lo envía por SMTP con tres timeouts.
6. Si el SMTP falla, el `try/catch` lo deja en el log como `ERROR`. La operación de negocio ya estaba confirmada y no se reintenta. Si el pool está saturado, la tarea se descarta con un `WARN`.

Detalle en [[Mail delivery]].

## Índice de preguntas

Generado a partir de la sección "Preguntas de defensa" de cada nota.
