---
title: "Defense guide"
categories: ["Navigation", "Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
tags: ["codemap", "navigation"]
---

# Defense guide

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

### Cuenta y seguridad

**[[Authentication flow#Preguntas de defensa|Authentication flow]]**

- ¿Cómo se inicia sesión después de registrarse si la persona no pasó por el login?
- ¿Dónde se guarda la sesión?
- ¿Por qué una Cuenta sin verificar puede loguearse?
- ¿Qué pasa si verifico desde el celular y tenía la sesión en la compu?
- ¿Qué impide que alguien registre mi correo y se quede con mi Cuenta?
- ¿Cómo se hashea la contraseña?
- ¿Qué es CSRF y dónde está el token?

**[[Tokens and email links#Preguntas de defensa|Tokens and email links]]**

- ¿El token es un JWT?
- ¿Qué pasa si pido dos enlaces de verificación?
- ¿Por qué el de recuperación vence y el de verificación no?
- ¿Se puede usar dos veces un enlace de recuperación?
- ¿Cómo evitan que el formulario de "olvidé mi contraseña" revele qué correos existen?
- ¿Qué pasa con las sesiones abiertas cuando se cambia la clave?
- ¿Dónde se arma la URL del enlace?

**[[Password recovery flow#Preguntas de defensa|Password recovery flow]]**

- ¿Qué diferencia hay entre cambiar y recuperar la contraseña?
- ¿Por qué `updatePassword` no compara el hash anterior?
- ¿Qué pasa si el correo no existe?
- ¿Por qué recuperar la contraseña verifica la Cuenta?
- ¿Y las sesiones que ya estaban abiertas?

**[[Security and authorization#Preguntas de defensa|Security and authorization]]**

- ¿Dónde se decide quién puede hacer qué?
- ¿Por qué 404 y no 403 cuando el recurso no existe?
- ¿Cómo sabe `@PreAuthorize` cuál es `#inquiryId`?
- ¿Qué diferencia hay entre `hasRole('ADMIN')` y `hasAuthority('VERIFIED')`?
- ¿Cómo se protegen de CSRF?
- ¿Y de XSS?
- ¿Cómo evitan que suban un ejecutable con extensión de imagen?
- ¿Qué pasa si alguien cambia el id de una imagen en la URL?
- ¿Qué pasa con las sesiones si cambio la contraseña?


### Correo

**[[Mail delivery#Preguntas de defensa|Mail delivery]]**

- ¿En qué hilo se manda el correo?
- ¿Qué pasa si el servidor de correo está caído?
- ¿Por qué no mandan el correo dentro de la transacción?
- ¿Cómo sabe el correo en qué idioma escribirse?
- ¿Por qué Thymeleaf si las vistas son JSP?
- ¿Qué pasa si se registran mil personas a la vez?
- ¿De dónde sale la URL del enlace?
- ¿Cómo funciona `@Async`?


### Venta

**[[Inquiry and sale flow#Preguntas de defensa|Inquiry and sale flow]]**

- ¿Qué pasa si dos personas quieren comprar el mismo disco?
- ¿Cómo evitan vender dos veces el mismo ejemplar?
- ¿Por qué `FOR UPDATE` si ya tienen el `UPDATE` condicional?
- ¿Dónde se guarda el comprobante y quién lo ve?
- ¿Qué estado HTTP devuelve una transición inválida?
- ¿Qué pasa si el mail no sale?

**[[Contact flow#Preguntas de defensa|Contact flow]]**

- ¿Puedo consultar dos veces por el mismo disco?
- ¿Qué pasa si consulto mi propia publicación?
- ¿Por qué hay un validador propio en vez de `@NotBlank`?
- ¿Por qué normalizan los saltos de línea?

**[[Conversation flow#Preguntas de defensa|Conversation flow]]**

- ¿Por qué el controller llama al service aunque el formulario tenga errores?
- ¿Cómo traen el último mensaje de cada consulta sin N+1?
- ¿Cuándo se cierra una conversación?
- ¿Quién recibe el correo?

**[[Reviews flow#Preguntas de defensa|Reviews flow]]**

- ¿Quién puede calificar a quién?
- ¿Qué pasa si quito la reseña y vuelvo a calificar?
- ¿Por qué `ReviewService` tiene `MANDATORY`?
- ¿Cómo se calcula el promedio?

**[[Cart flow#Preguntas de defensa|Cart flow]]**

- ¿El carrito es una compra?
- ¿Qué pasa si uno de los vinilos se vendió mientras tenía el carrito abierto?
- ¿Cómo evitan un interbloqueo al bloquear varios posts?
- ¿Cuántas consultas SQL hace el envío de 20 vinilos?
- ¿Dónde está definido qué se puede consultar?
- ¿Por qué el contador de la cabecera no es un atributo de modelo?
- ¿Cuántos correos recibe un publicante si le consultan cinco vinilos desde un carrito?

**[[Addresses and payment flow#Preguntas de defensa|Addresses and payment flow]]**

- ¿Por qué no se edita la dirección directamente?
- ¿Qué pasa si acepto una consulta sin tener CBU?
- ¿Cómo validan un CBU?
- ¿Qué impide tener cuatro direcciones si mando dos altas a la vez?


### Catálogo y publicaciones

**[[Landing flow#Preguntas de defensa|Landing flow]]**

- ¿Cómo buscan sin distinguir tildes ni mayúsculas?
- ¿Cómo evitan inyección SQL si el `WHERE` es dinámico?
- ¿Qué pasa si pido la página 9999, o la 0?
- ¿Por qué los filtros van por `GET`?
- ¿Por qué cuentan antes de listar?

**[[Search suggestions flow#Preguntas de defensa|Search suggestions flow]]**

- ¿Qué devuelve el endpoint y por qué JSON?
- ¿Cómo se convierte la lista de Java a JSON?
- ¿Cómo evitan XSS en el desplegable?
- ¿Cómo ordenan las sugerencias?

**[[Post detail flow#Preguntas de defensa|Post detail flow]]**

- ¿Por qué los botones se deciden en el modelo y no en la JSP?
- ¿Por qué la ficha pasa por `CartService`?
- ¿Cómo vuelve la ficha al listado con los mismos filtros?
- ¿Qué pasa si esconden el botón pero llamo a la URL de editar?

**[[Publish flow#Preguntas de defensa|Publish flow]]**

- ¿Qué pasa si dos personas publican a la vez el mismo artista nuevo?
- ¿Por qué la validación está en el formulario y también en el service?
- ¿Cómo deciden si dos artistas son el mismo?
- ¿Dónde quedan las fotos?

**[[Edit and delete flow#Preguntas de defensa|Edit and delete flow]]**

- ¿Qué pasa con las consultas si borro la publicación?
- ¿Por qué no puedo editar una publicación reservada?
- ¿Cómo modera un administrador?
- ¿Qué diferencia hay entre 403, 404 y 409 acá?

**[[Cover image flow#Preguntas de defensa|Cover image flow]]**

- ¿Dónde guardan las imágenes?
- ¿Cómo validan que sea una imagen?
- ¿Qué pasa si subo algo de 100 MB?
- ¿Por qué el filtro multipart va antes que el de seguridad?
- ¿Puedo ver cualquier imagen cambiando el id?

**[[Gallery flow#Preguntas de defensa|Gallery flow]]**

- ¿Por qué dos lugares para las fotos?
- ¿Qué garantiza que no haya más de cinco?
- ¿Qué pasa con las fotos al borrar la publicación?


### Perfiles

**[[Profile flow#Preguntas de defensa|Profile flow]]**

- ¿Cómo se entera la cabecera de que cambié el nombre?
- ¿Qué pasa si cambio la clave con otra sesión abierta en el celular?
- ¿Por qué el `UPDATE` de la clave lleva el hash viejo en el `WHERE`?
- ¿Qué pasa con la foto anterior?

**[[Public profile flow#Preguntas de defensa|Public profile flow]]**

- ¿Qué datos de una Cuenta son públicos?
- ¿Qué pasa si pido el perfil de una Cuenta sin verificar?
- ¿Por qué existe `PublicProfileService`?


### Arquitectura y datos

**[[Domain and identity#Preguntas de defensa|Domain and identity]]**

- ¿Qué diferencia hay entre Álbum y Post?
- ¿Hay una entidad Venta?
- ¿Por qué los modelos no tienen setters?
- ¿Qué es una proyección?
- ¿Cómo distinguen comprador de vendedor?

**[[Architecture#Preguntas de defensa|Architecture]]**

- ¿Por qué hay módulos de contratos separados?
- ¿Qué impide que un controller use un DAO?
- ¿Por qué las reglas de validación están en `models`?
- ¿Cómo evitan dependencias circulares entre services?

**[[Startup and dependency injection#Preguntas de defensa|Startup and dependency injection]]**

- ¿Cómo se crean las tablas?
- ¿Qué pasa si falta `mail.properties`?
- ¿Cómo se inyectan las dependencias?
- ¿Por qué `@EnableAsync` y `@EnableTransactionManagement`?

**[[Database schema#Preguntas de defensa|Database schema]]**

- ¿Cómo se crea y evoluciona el esquema?
- ¿Por qué los tests usan HSQLDB si producción es PostgreSQL?
- ¿Dónde se guardan las imágenes?
- ¿Qué pasa con las consultas si se borra una publicación?
- ¿Cómo evitan dos reservas de la misma publicación?

**[[Schema history and seeds#Preguntas de defensa|Schema history and seeds]]**

- ¿Qué pasa si alguien edita una migración ya aplicada?
- ¿Cómo se incorporaron las bases que ya existían?
- ¿De dónde salen los datos de los tests?
- ¿Por qué V4 agrega una columna en vez de un índice sobre `LOWER(title)`?

**[[Transactions and concurrency#Preguntas de defensa|Transactions and concurrency]]**

- ¿Dónde ponen `@Transactional` y por qué?
- ¿Qué pasa si dos compradores consultan el mismo vinilo a la vez?
- ¿Y si el vendedor acepta dos consultas a la vez?
- ¿Por qué el correo sale después del commit?
- ¿Qué es `Propagation.MANDATORY`?
- ¿Por qué un savepoint?

**[[Validation and errors#Preguntas de defensa|Validation and errors]]**

- ¿Dónde validan?
- ¿Por qué validar dos veces?
- ¿Cómo validan que dos contraseñas coincidan?
- ¿Cómo deciden entre 403 y 404?
- ¿Qué pasa si suben un archivo enorme?

**[[Paginated listings#Preguntas de defensa|Paginated listings]]**

- ¿Cómo paginan?
- ¿Qué pasa si pido la página 9999?
- ¿Cómo paginan la bandeja si agrupa por publicación?
- ¿Dónde se valida el número de página?


### Interfaz

**[[UI components#Preguntas de defensa|UI components]]**

- ¿Cómo evitan XSS en las vistas?
- ¿Por qué usan `c:url`?
- ¿Qué es un tag file?
- ¿Dónde va el token CSRF?

**[[UI styles and tokens#Preguntas de defensa|UI styles and tokens]]**

- ¿Usan algún framework de CSS?
- ¿Cómo hicieron el modo oscuro?
- ¿Cómo se sirven los CSS?

**[[Views and assets#Preguntas de defensa|Views and assets]]**

- ¿Por qué las JSP están bajo `WEB-INF`?
- ¿Hay lógica en las vistas?
- ¿Qué pasa si el navegador no tiene JavaScript?
- ¿Cómo evitan XSS en el JavaScript?


### Operación

**[[Build and dependencies#Preguntas de defensa|Build and dependencies]]**

- ¿Cómo se construye y se despliega?
- ¿Por qué las versiones están en el POM raíz?
- ¿Usan Thymeleaf para las vistas?
- ¿Por qué `services` tiene `persistence` como dependencia runtime?

**[[Configuration and running#Preguntas de defensa|Configuration and running]]**

- ¿Dónde están las credenciales?
- ¿Cómo sabe el correo qué URL poner en un enlace?
- ¿Qué cambia entre local y producción?

**[[Localization#Preguntas de defensa|Localization]]**

- ¿Cómo decide la aplicación en qué idioma responder?
- ¿En qué idioma llega un correo?
- ¿Qué pasa si falta una traducción?
- ¿Por qué hay un `messages_es` vacío?

**[[Logging#Preguntas de defensa|Logging]]**

- ¿Qué usan para loguear?
- ¿Dónde quedan los logs?
- ¿Qué loguean y qué no?
- ¿Por qué algunos logs se emiten después del commit?

**[[Testing and evidence#Preguntas de defensa|Testing and evidence]]**

- ¿Qué testean y cómo?
- ¿Por qué no usan `verify`?
- ¿Cómo se aíslan los tests de DAO entre sí?
- ¿Los tests garantizan que funciona en producción?


Total: 168 preguntas en 36 notas.

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
