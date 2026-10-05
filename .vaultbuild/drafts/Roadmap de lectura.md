@title: Roadmap de lectura
@categories: Navigation
@tags: codemap, navigation

> [!summary] En una frase
> Un orden para leer los 472 archivos versionados del proyecto (238 clases Java, 49.452 líneas en total) sin perderse: primero el contexto, después un flujo simple de punta a punta, y luego cada funcionalidad en el orden en que se apoyan unas en otras.

Cada archivo aparece **una sola vez**, con una casilla para marcar. La lista se generó a partir de `git ls-tree` en `c3e2a4c` y el generador falla si un archivo queda sin asignar o aparece dos veces, así que la cobertura es completa.

## Cómo usarlo

1. Abrí la etapa y leé **primero las notas del vault** que indica. Te dan el recorrido, las decisiones y las preguntas de defensa antes de ver el código.
2. Recorré los archivos en el orden de la lista. Dentro de cada etapa el orden sigue al request: web, service, persistencia, vista, tests.
3. Marcá la casilla cuando puedas explicar el archivo sin mirarlo.
4. Cerrá la etapa contestando en voz alta las preguntas del final. Si alguna no sale, volvé a la nota de flujo.

Los enlaces `[[Clase]]` abren la nota de esa clase en el vault, con su resumen, sus métodos, quién la usa y el código completo. Los enlaces con ruta abren el archivo en el repositorio.

## Cómo leer una clase

| Tipo | Qué mirar primero | Qué preguntarte |
|---|---|---|
| Modelo | Campos y constructor | ¿Es una fila de una tabla o una proyección de lectura? ¿Qué reglas lleva adentro? |
| Interfaz de DAO o service | Firmas | ¿Qué recibe y qué devuelve? ¿Qué excepciones declara en los comentarios? |
| DAO JDBC | El SQL y el `RowMapper` | ¿Qué tablas une? ¿Los parámetros están ligados con `?`? ¿Devuelve filas afectadas? |
| Service | Métodos `@Transactional` | ¿Qué valida? ¿Qué bloquea? ¿Qué pasa después del commit? ¿Qué excepción lanza cada rechazo? |
| Controller | `@RequestMapping` y `@PreAuthorize` | ¿Qué ruta, qué método HTTP, quién puede entrar? ¿Queda algo de lógica que debería estar en el service? |
| Formulario y validador | Anotaciones | ¿Qué regla está en el campo y cuál cruza campos? |
| JSP y tag | `<c:out>`, `<c:url>`, `<spring:message>` | ¿Hay algún dato sin escapar o alguna URL armada a mano? |
| Test | Nombre del método | ¿Qué caso cubre? ¿Qué caso falta? |

## Dos formas de recorrerlo

**Completo.** Las 17 etapas en orden. Una etapa por sesión de estudio es un ritmo razonable; las etapas 5 y 9 son las más densas y conviene partirlas en dos.

**Corto, para una defensa.** Si hay poco tiempo, este orden cubre lo que más se pregunta:

1. Etapa 0 (solo `CONTEXT.md` y `CLAUDE.md`) y [[Architecture]].
2. Etapa 5 completa: cuenta, tokens y seguridad.
3. Etapa 6: correo.
4. Etapa 9: consulta y venta, al menos [[InquiryServiceImpl]] con [[Inquiry and sale flow]] al lado.
5. [[Transactions and concurrency]], [[Validation and errors]] y [[Database schema]].
6. [[Defense guide]] para practicar las preguntas.

## Las etapas

| Etapa | Tema | Archivos | Líneas |
|---|---|---|---|
| 0 | Orientación | 10 | 819 |
| 1 | Build, configuración y arranque | 30 | 1.356 |
| 2 | Base de datos | 19 | 1.340 |
| 3 | Dominio: los modelos | 57 | 1.951 |
| 4 | Primer recorrido completo: catálogo y búsqueda | 28 | 4.645 |
| 5 | Cuenta y seguridad | 39 | 3.712 |
| 6 | Correo | 16 | 1.109 |
| 7 | Publicar, editar e imágenes | 40 | 2.933 |
| 8 | Ficha, contacto, direcciones y datos de cobro | 31 | 1.667 |
| 9 | Consulta, venta y conversación | 35 | 5.069 |
| 10 | Reseñas y perfiles | 27 | 2.294 |
| 11 | Carrito | 12 | 1.459 |
| 12 | Errores | 6 | 184 |
| 13 | Interfaz compartida | 20 | 3.467 |
| 14 | Textos | 4 | 1.596 |
| 15 | Herramientas del repositorio | 70 | 7.556 |
| 16 | Historia: especificaciones, planes e issues | 28 | 8.295 |

Las líneas son el total de cada archivo en `c3e2a4c`, incluidos comentarios y líneas en blanco. Sirven para estimar el esfuerzo relativo de cada etapa, no como medida de complejidad.

## Qué conviene saltear en una primera lectura

- Los procedimientos para agentes de la etapa 15 (`.claude/skills`, `.agents/skills`, `.codex/prompts`): son tres copias del mismo contenido y no forman parte de la aplicación.
- Los planes largos de la etapa 16 (`venta-con-comprobante.md` y `perfil-consultas-ui.md` suman más de cinco mil líneas): sirven como consulta puntual.
- `style.css` línea por línea: alcanza con ubicar las secciones.
- Los tres bundles de mensajes completos.

## Etapa 0 — Orientación

*10 archivos · 819 líneas*

**Objetivo.** Saber qué es el producto, qué palabras usa y qué reglas sigue el equipo antes de abrir código.

**Primero, en el vault:** [[Project snapshot]] · [[Domain and identity]] · [[History and specifications]]

### Documentos

- [ ] [README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/README.md>) — Instalación, configuración y funcionalidades. Ojo: la sección de credenciales describe el registro anterior.
- [ ] [CONTEXT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/CONTEXT.md>) — Glosario del dominio y palabras a evitar. Leelo entero: es corto y fija el vocabulario.
- [ ] [CLAUDE.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/CLAUDE.md>) — Reglas del equipo por capa. La mejor síntesis de las convenciones.
- [ ] [AGENTS.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/AGENTS.md>) — Mismo contenido que CLAUDE.md, para otros agentes.
- [ ] [docs/setup.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/setup.md>) — Tecnologías, comandos y reglas de dependencias.
- [ ] [docs/adr/0001-establish-quiero-vinilos-domain.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0001-establish-quiero-vinilos-domain.md>) — Por qué el producto es quieroVinilos.
- [ ] [docs/adr/0002-own-the-album-catalog-locally.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0002-own-the-album-catalog-locally.md>) — Por qué el catálogo de álbumes es propio.
- [ ] [docs/adr/0003-conversation-inside-the-inquiry.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0003-conversation-inside-the-inquiry.md>) — Por qué la conversación vive dentro de la consulta.
- [ ] [docs/adr/0004-freeze-sale-price-at-acceptance.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/adr/0004-freeze-sale-price-at-acceptance.md>)
- [ ] [TODO.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/TODO.md>) — Pendientes al 9 de septiembre. Casi todo está resuelto: leelo como historia.

**Al terminar deberías poder contestar:**

- ¿Qué diferencia hay entre Álbum, Post y Consulta?
- ¿Qué puede hacer una Cuenta sin verificar?
- ¿Qué está prohibido en esta etapa de la cursada?

## Etapa 1 — Build, configuración y arranque

*30 archivos · 1.356 líneas*

**Objetivo.** Entender cómo seis módulos se convierten en un WAR y cómo arranca el contexto de Spring.

**Primero, en el vault:** [[Architecture]] · [[Build and dependencies]] · [[Startup and dependency injection]] · [[Configuration and running]] · [[Logging]]

### Maven

- [ ] [pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/pom.xml>) — Módulos, versiones en propiedades, dependencyManagement y plugin de Jetty.
- [ ] [models/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/pom.xml>) — Sin dependencias del proyecto.
- [ ] [persistence-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/pom.xml>) — Solo depende de models.
- [ ] [persistence/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/pom.xml>) — Spring JDBC y driver; HSQLDB y Flyway en test.
- [ ] [services-contracts/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/pom.xml>) — Solo depende de models.
- [ ] [services/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/pom.xml>) — Mirá el scope runtime de persistence.
- [ ] [webapp/pom.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/pom.xml>) — Dependencias runtime, nombre del WAR, exclusión de logback-test y perfil pampero.
- [ ] [models/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/.mvn/jvm.config>)
- [ ] [models/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/.mvn/maven.config>)
- [ ] [persistence-contracts/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/.mvn/jvm.config>)
- [ ] [persistence-contracts/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/.mvn/maven.config>)
- [ ] [persistence/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/.mvn/jvm.config>)
- [ ] [persistence/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/.mvn/maven.config>)
- [ ] [services-contracts/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/.mvn/jvm.config>)
- [ ] [services-contracts/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/.mvn/maven.config>)
- [ ] [services/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/.mvn/jvm.config>)
- [ ] [services/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/.mvn/maven.config>)
- [ ] [webapp/.mvn/jvm.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/.mvn/jvm.config>)
- [ ] [webapp/.mvn/maven.config](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/.mvn/maven.config>)
- [ ] [models/src/main/resources/.gitkeep](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/resources/.gitkeep>) — Archivo vacío para conservar el directorio.

### Arranque

- [ ] [webapp/src/main/webapp/WEB-INF/web.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/web.xml>) — Listeners, filtros en orden, DispatcherServlet, sesión por cookie y página de 404.
- [ ] [[WebConfig]] `webapp` — Configuración de Spring: escaneo de componentes, `DataSource`, transacciones, Flyway al arrancar, resolver multipart, vistas JSP, `Locale`, i18n, validador, JavaMail, Thymeleaf para correos y el pool de hilos de `@Async`.

### Configuración y logs

- [ ] [webapp/src/main/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/database.properties.example>) — Keys de conexión a la base.
- [ ] [webapp/src/main/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/mail.properties.example>) — Keys de SMTP, timeouts, remitente y URL base.
- [ ] [webapp/src/pampero/resources/database.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/database.properties.example>) — Lo mismo para el servidor de la cátedra.
- [ ] [webapp/src/pampero/resources/mail.properties.example](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/pampero/resources/mail.properties.example>) — Lo mismo para el servidor; mirá la URL base con context path.
- [ ] [webapp/src/main/resources/logback.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback.xml>) — Dos archivos diarios; leé el comentario sobre el nombre.
- [ ] [webapp/src/main/resources/logback-test.xml](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/logback-test.xml>) — Consola en DEBUG para desarrollo.
- [ ] [.gitignore](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.gitignore>) — Qué no se versiona: compilados y propiedades con credenciales.
- [ ] [.worktreeinclude](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.worktreeinclude>) — Propiedades que se copian a un worktree nuevo.

**Al terminar deberías poder contestar:**

- ¿Qué impide que un controller use un DAO?
- ¿Cómo se crean las tablas al arrancar?
- ¿Qué pasa si falta una propiedad de configuración?
- ¿Dónde quedan los logs en el servidor?

## Etapa 2 — Base de datos

*19 archivos · 1.340 líneas*

**Objetivo.** Leer el esquema en el orden en que se construyó y conocer los datos con los que corren los tests.

**Primero, en el vault:** [[Database schema]] · [[Schema history and seeds]]

### Migraciones, en orden

- [ ] [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>) — Tablas base. Leé los comentarios del encabezado y el de inquiries.
- [ ] [persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql>) — Unicidad del correo.
- [ ] [persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql>) — Claves foráneas que faltaban.
- [ ] [persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql>) — Identidad del álbum sin índice sobre expresión.
- [ ] [persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql>) — La más grande: cobro, direcciones, reserva, comprobante, precio, estados.
- [ ] [persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql>) — enabled pasa a verified; fecha en los tokens.
- [ ] [persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql>) — Mensajes; la única que mueve datos.
- [ ] [persistence/src/main/resources/db/migration/V8__post_gallery.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V8__post_gallery.sql>) — Fotos adicionales, tope y orden.
- [ ] [persistence/src/main/resources/db/migration/V9__user_avatars.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V9__user_avatars.sql>) — Foto de perfil.
- [ ] [persistence/src/main/resources/db/migration/V10__sale_reviews.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V10__sale_reviews.sql>) — Reseñas con sus tres restricciones.
- [ ] [persistence/src/main/resources/db/migration/V11__carrito.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V11__carrito.sql>) — Carrito con clave compuesta y cascada.

### Datos de prueba

- [ ] [persistence/src/test/resources/populator.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/resources/populator.sql>) — Datos fijos de los tests de DAO. Ubicá qué cuenta, post y consulta representa cada caso.
- [ ] [[TestConfiguration]] `test` — Contexto de los tests de persistencia: HSQLDB en memoria con sintaxis PostgreSQL, las mismas migraciones Flyway que producción y después los fixtures de `populator.sql`.

### Datos de demostración y base local

- [ ] [tools/setup_local_postgres.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/setup_local_postgres.sh>) — Guía interactiva para preparar PostgreSQL local.
- [ ] [tools/seed_local_data.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/seed_local_data.sh>) — Carga el catálogo de demostración en una transacción.
- [ ] [database/seed_dev_posts.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/seed_dev_posts.sql>) — SQL del catálogo de demostración.
- [ ] [database/demo_posts.tsv](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/demo_posts.tsv>) — Las publicaciones de demostración.
- [ ] [tools/sql/demo-users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/sql/demo-users.sql>) — Dos cuentas de demostración.
- [ ] [database/users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/users.sql>) — Resto del esqueleto inicial; no se usa.

**Al terminar deberías poder contestar:**

- ¿Qué reglas garantiza la base y cuáles el service?
- ¿Por qué las migraciones tienen que correr en HSQLDB?
- ¿Qué pasa con las consultas si se borra una publicación?

## Etapa 3 — Dominio: los modelos

*57 archivos · 1.951 líneas*

**Objetivo.** Conocer los objetos que viajan entre capas. Son inmutables: mirá qué campos tienen y qué reglas llevan adentro.

**Primero, en el vault:** [[Domain and identity]]

### Cuenta

- [ ] [[User]] `models` — La Cuenta: nombre visible, correo, hash de la contraseña, [[UserRole]], si está verificada, idioma preferido y [[PaymentInfo]].
- [ ] [[UserRole]] `models` — Roles de una Cuenta: `USER` y `ADMIN`.
- [ ] [[PaymentInfo]] `models` — Datos de cobro de una Cuenta: CBU o CVU y alias, cualquiera de los dos opcional.
- [ ] [[PaymentInfoRules]] `models` — Formato de los datos de cobro: CBU de 22 dígitos con sus dos dígitos verificadores y alias de 6 a 20 caracteres.
- [ ] [[EmailRules]] `models` — Una sola regla para guardar y buscar un correo: sin espacios y en minúsculas.
- [ ] [[PublicUserProfile]] `models` — Lo único de una Cuenta que se muestra a otros: id, nombre y foto.
- [ ] [[EmailVerificationToken]] `models` — Fila de `email_verification_tokens`: id, Cuenta, token y fecha de emisión.
- [ ] [[PasswordResetToken]] `models` — Fila de `password_reset_tokens`: id, Cuenta, token y vencimiento.

### Catálogo

- [ ] [[Artist]] `models` — Artista del catálogo compartido: id y nombre visible.
- [ ] [[Album]] `models` — La obra del catálogo compartido: título, artista, año de lanzamiento, [[Genre]] y una portada heredada opcional.
- [ ] [[Genre]] `models` — Quince géneros del catálogo, incluido `OTHER`.
- [ ] [[Condition]] `models` — Estado físico del ejemplar: `NEW` o `USED`.
- [ ] [[SearchText]] `models` — Normalización compartida de búsqueda: minúsculas, sin diacríticos y con separadores reducidos a un espacio (`phrase`), o sin espacios (`compact`).
- [ ] [[VinylInputRules]] `models` — Límites numéricos compartidos por el catálogo y la carga: años entre 1000 y 9999 y no futuros, precios entre 1 y 99.999.999, rango de precios ordenado y prensado no anterior al lanzamiento.

### Publicación

- [ ] [[Post]] `models` — La publicación guardada: publicante, álbum, precio, descripción, [[Condition]], año de prensado, zona, foto principal y [[PostStatus]].
- [ ] [[PostStatus]] `models` — Estado de la publicación: `AVAILABLE`, `RESERVED` (hay una venta en curso) o `SOLD`.
- [ ] [[PostSummary]] `models` — La publicación unida a su publicante, álbum y artista en una sola fila: lo que muestran las tarjetas y la ficha.
- [ ] [[PostDetail]] `models` — La ficha de una publicación para quien la mira: resumen, perfil público del vendedor (nulo si no está verificado), fotos y si puede editarla (`isEditable`: disponible y propia o moderador).
- [ ] [[PostPage]] `models` — Una página de publicaciones con su número, el total de páginas y si hay anterior y siguiente.
- [ ] [[PostSort]] `models` — Los diez órdenes del catálogo.
- [ ] [[PostSearchCriteria]] `models` — Filtros combinables del catálogo: texto, orden, género, condición, artista, año y rango de precio.
- [ ] [[SearchResult]] `models` — Resultado de una búsqueda: la query ya normalizada, los criterios tal como el service los aplicó, la página y el total de coincidencias.
- [ ] [[SearchSuggestion]] `models` — Una sugerencia del buscador: tipo, valor y, para un álbum, el artista.
- [ ] [[SearchSuggestionType]] `models` — Tipo de sugerencia: `ARTIST` o `ALBUM`.
- [ ] [[Image]] `models` — Una imagen guardada: id, tipo de contenido y bytes.
- [ ] [[ImageUpload]] `models` — Un archivo subido reducido a tipo de contenido y bytes.
- [ ] [[ImageRules]] `models` — Qué imagen se acepta: PNG, JPEG o WEBP cuya firma de bytes coincide con el tipo declarado, hasta 5 MiB, hasta 5 fotos por publicación, y 26 MiB por request.
- [ ] [[FilterCounts]] `models` — Los números de los chips de filtro de un listado: un mapa valor → cantidad y el total.

### Direcciones

- [ ] [[Address]] `models` — Dirección de envío de una Cuenta: calle, altura, piso, ciudad, [[Province]], código postal y notas, más la marca `archived`.
- [ ] [[Province]] `models` — Las 24 jurisdicciones de Argentina.
- [ ] [[ShippingOptions]] `models` — Lo que necesita un formulario de envío en una sola lectura: las direcciones activas, la propuesta por defecto y si se puede sumar otra.

### Consulta y venta

- [ ] [[Inquiry]] `models` — La Consulta tal como está guardada: id, post (nulo si la publicación fue eliminada), comprador y [[InquiryStatus]].
- [ ] [[InquiryStatus]] `models` — Estados de la Consulta: `PENDING`, `AWAITING_PAYMENT`, `PAYMENT_SUBMITTED`, `ACCEPTED` (venta confirmada), `REJECTED` y `CANCELLED`.
- [ ] [[InquiryStatusFilter]] `models` — Los cuatro filtros de las bandejas, agrupando estados como los lee una persona: `PENDING`, `IN_PROGRESS` (espera de pago y pago informado), `CONFIRMED` (`ACCEPTED`) y `CLOSED` (rechazada o cancelada).
- [ ] [[InquirySummary]] `models` — La Consulta como la muestran la bandeja y el detalle: partes con su foto, álbum, precio (el actual del post mientras está pendiente y el fijado al aceptar después.
- [ ] [[InquiryDetail]] `models` — La Consulta vista por una de sus partes, con su conversación y la reseña propia.
- [ ] [[InquiryGroup]] `models` — Una publicación y las consultas que la tocaron: la unidad por la que agrupan y paginan las dos bandejas.
- [ ] [[InquiryPage]] `models` — Una página de la bandeja: grupos, número de página y total de páginas.
- [ ] [[InquiryParties]] `models` — Comprador y publicante de una Consulta, sin el resto del resumen.
- [ ] [[Message]] `models` — Un texto de la conversación de una Consulta: autor, cuerpo y fecha.
- [ ] [[MessageRules]] `models` — Qué texto se acepta como Mensaje: normaliza CRLF a LF, recorta y exige hasta 500 caracteres.
- [ ] [[Receipt]] `models` — El comprobante de una venta: tipo de contenido y bytes.
- [ ] [[ReceiptRules]] `models` — Qué comprobante se acepta: PDF, PNG, JPEG o WEBP de hasta 5 MiB.
- [ ] [[ContactState]] `models` — Qué puede hacer una Cuenta con un post: `CONTACTABLE`, `OPEN_INQUIRY`, `UNAVAILABLE` u `OWN_POST`.
- [ ] [[PostContactOptions]] `models` — Lo que la ficha de un post le ofrece a quien la mira: el [[ContactState]], la Consulta abierta si la hay y si ya está en su carrito.
- [ ] [[PostView]] `models` — La pantalla de un post: su [[PostDetail]] y las [[PostContactOptions]] de quien mira.

### Reseñas y perfil público

- [ ] [[Review]] `models` — Calificación de una parte a la otra en una venta confirmada: consulta, autor, destinatario, nombre y foto del autor, puntaje, comentario, si está activa y fecha.
- [ ] [[ReviewRules]] `models` — Puntaje de 1 a 5 y comentario opcional de hasta 500 caracteres, con la misma normalización que un Mensaje.
- [ ] [[ReviewStats]] `models` — Cantidad y promedio de las reseñas activas de una Cuenta.
- [ ] [[ReviewPage]] `models` — Una página de reseñas del perfil público para un rol ([[ReviewSubjectRole]]): las reseñas, las estadísticas de ese rol, el número de página y si hay anterior o siguiente.
- [ ] [[ReviewSubjectRole]] `models` — Rol que tenía la persona calificada en la venta: `SELLER` o `BUYER`.
- [ ] [[PublicProfile]] `models` — El perfil público de una Cuenta: identidad, publicaciones a la venta paginadas y una [[ReviewPage]] con las reseñas del rol elegido.

### Carrito

- [ ] [[Cart]] `models` — El carrito tal como se muestra: los grupos por publicante, la cantidad de vinilos y el total con los precios actuales.
- [ ] [[CartItem]] `models` — Un vinilo dentro del carrito, con lo que muestra la pantalla: post, publicante, título, artista, año, imagen opcional y precio actual.
- [ ] [[CartSellerGroup]] `models` — Los vinilos del carrito que son de un mismo publicante.
- [ ] [[CartCheckout]] `models` — Lo que necesita la pantalla del carrito: el [[Cart]] y las [[ShippingOptions]] del comprador.
- [ ] [[CartCheckoutResult]] `models` — Resultado de enviar el carrito: cuántas Consultas se crearon y cuántos vinilos se omitieron porque dejaron de estar disponibles.

**Al terminar deberías poder contestar:**

- ¿Cuáles son entidades y cuáles proyecciones de lectura?
- ¿Qué reglas viven en clases *Rules y por qué en models?
- ¿Qué estados tiene una publicación y cuáles una consulta?

## Etapa 4 — Primer recorrido completo: catálogo y búsqueda

*28 archivos · 4.645 líneas*

**Objetivo.** Seguir un request de solo lectura por todas las capas. Es el flujo más simple para fijar el patrón controller, service, DAO, JSP.

**Primero, en el vault:** [[Landing flow]] · [[Search suggestions flow]] · [[Paginated listings]]

### Web

- [ ] [[LandingController]] `webapp` — Catálogo en `GET /`: liga los filtros de la URL ignorando valores de enum inválidos y delega todo en [[PostService]].
- [ ] [[ListingQueries]] `webapp` — Sanea el parámetro `from` (la query del listado de origen): solo acepta caracteres de una query ya codificada.
- [ ] [[PostOrigin]] `webapp` — De dónde se llegó a una ficha: perfil público o perfil propio.
- [ ] [[CatalogFilterForm]] `webapp` — Filtros del catálogo ligados desde la URL: texto, orden, género, condición, artista, año y precios.
- [ ] [[CatalogFilterValidator]] `webapp` — Valida año y precios de los filtros y que el rango esté ordenado, colgando cada error de su campo.
- [ ] [[ValidCatalogFilters]] `webapp` — Anotación de clase que aplica [[CatalogFilterValidator]].
- [ ] [[SearchSuggestionController]] `webapp` — `GET /search/suggestions`: sugerencias de álbum y artista en JSON, con la etiqueta del tipo traducida en el servidor.
- [ ] [[SearchSuggestionDto]] `webapp` — Forma JSON de una sugerencia del buscador: `value`, `type`, `typeLabel` y `detail`.
- [ ] [[ArtistSuggestionController]] `webapp` — `GET /artists/suggestions`: devuelve en JSON hasta cinco artistas para el autocompletado del formulario de publicar.
- [ ] [[ArtistSuggestionDto]] `webapp` — Forma JSON de una sugerencia de artista: solo `value`.

### Service

- [ ] [[PostService]] `services-contracts` — Contrato de publicaciones: ficha, búsqueda paginada, sugerencias, listados por publicante (el privado con filtro opcional por [[PostStatus]] y sus conteos), alta, edición y borrado (estas dos reciben quién actúa), más las operaciones internas de la venta (`lockById`, `lockByIds`, `reserve`, `release`, `markSold`) que exigen una transacción abierta.
- [ ] [[PostServiceImpl]] `services` — Publicaciones.
- [ ] [[Pagination]] `services` — Aritmética de páginas compartida: páginas para un total y offset de una página.
- [ ] [[PageNotFoundException]] `services-contracts` — Número de página menor que 1 o mayor que el total.
- [ ] [[InvalidSearchQueryException]] `services-contracts` — El texto de búsqueda supera los 255 caracteres.
- [ ] [[PostNotFoundException]] `services-contracts` — La publicación no existe.

### Persistencia

- [ ] [[PostDao]] `persistence-contracts` — Contrato de publicaciones: búsqueda y conteo con filtros, sugerencias, listados por publicante (el privado filtrado por un conjunto de estados, con conteo por estado para los chips), lectura con bloqueo de una o varias filas, alta, edición, cambio de estado con guarda y borrado.
- [ ] [[PostJdbcDao]] `persistence` — Publicaciones con Spring JDBC.

### Vista

- [ ] [webapp/src/main/webapp/WEB-INF/views/landing/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/landing/index.jsp>) — Filtros, orden, grilla, estado vacío y paginación.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/vinyl-card.tag>) — La tarjeta de un vinilo; el componente más reutilizado.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/pagination.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination.tag>) — Flechas que conservan parámetros y ancla.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/pagination-link.tag>) — Un enlace de página.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/post-badge.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/post-badge.tag>) — Estado de una publicación.
- [ ] [webapp/src/main/webapp/js/catalog.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/catalog.js>) — Envía el orden al cambiar el select; pliega filtros en pantallas angostas.
- [ ] [webapp/src/main/webapp/js/autocomplete.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/autocomplete.js>) — Sugerencias: espera, número de secuencia, JSON y nodos armados con textContent.

### Tests

- [ ] [[PaginationTest]] `test` — Páginas para totales vacíos, exactos y con resto.
- [ ] [[PostServiceImplTest]] `test` — Normalización de la búsqueda, filtros inválidos, paginación, publicar, editar con galería, eliminar, autorización por publicante o ADMIN en el service, "Mis publicaciones" filtrada por estado y bloqueos.
- [ ] [[PostJdbcDaoTest]] `test` — Búsqueda con filtros, órdenes, comodines literales, conteo, sugerencias, listado del publicante filtrado por estado y conteo por estado, bloqueo, cambio de estado con guarda, edición y borrado.

**Al terminar deberías poder contestar:**

- ¿Cómo llega un filtro de la URL a la cláusula WHERE?
- ¿Cómo se evita la inyección SQL en una consulta con filtros opcionales?
- ¿Por qué las sugerencias devuelven JSON?
- ¿Cómo se calcula la paginación?

## Etapa 5 — Cuenta y seguridad

*39 archivos · 3.712 líneas*

**Objetivo.** El tema más preguntado en la defensa: registro, login, verificación, tokens, recuperación y quién puede entrar a qué.

**Primero, en el vault:** [[Authentication flow]] · [[Tokens and email links]] · [[Password recovery flow]] · [[Security and authorization]]

### Configuración de seguridad

- [ ] [[SecurityConfig]] `webapp` — Configuración de Spring Security: BCrypt 12 y su adaptador `PasswordHasher`, beans de pertenencia para `@PreAuthorize`, la lista única de rutas de Cuenta verificada, form login por correo, logout, registro de sesiones y el handler que distingue "verificá tu correo" de 403.
- [ ] [[AuthenticatedUser]] `webapp` — El principal de la sesión: adapta la Cuenta a `UserDetails`.
- [ ] [[AuthenticatedUserDetailsService]] `webapp` — Carga la Cuenta por correo para el login.
- [ ] [[AuthenticationSessions]] `webapp` — Tres operaciones sobre la sesión: iniciar sesión sin pasar por el login (registro), refrescar el principal (verificación, cambio de nombre) y cerrar todas las sesiones de una Cuenta (cambio o recuperación de clave).
- [ ] [[SameSiteRedirects]] `webapp` — Convierte el header `Referer` en una ruta de regreso segura: mismo host, dentro del context path y sin `//` ni barra invertida.
- [ ] [[VerificationAccessDeniedHandler]] `webapp` — Una Cuenta sin verificar que entra a una ruta de Cuenta verificada va a `/verify/required`.
- [ ] [[PasswordHasher]] `services-contracts` — Hashear y comparar contraseñas sin que `services` dependa de Spring Security.

### Web

- [ ] [[AuthenticationController]] `webapp` — Login (solo la vista), registro con inicio de sesión automático, verificación por enlace, página de aviso, reenvío con espera y recuperación de contraseña en dos pasos.
- [ ] [[LoginForm]] `webapp` — Bean con correo y contraseña para dibujar el formulario de login.
- [ ] [[RegisterForm]] `webapp` — Registro: correo, nombre, contraseña con [[ValidPassword]] y confirmación con [[MatchingPasswords]].
- [ ] [[ForgotPasswordForm]] `webapp` — Pedido de recuperación: solo el correo, obligatorio, con formato y hasta 100 caracteres.
- [ ] [[ResetPasswordForm]] `webapp` — Recuperación: token oculto obligatorio, contraseña nueva con [[ValidPassword]] y confirmación.
- [ ] [[ValidPassword]] `webapp` — Restricción compuesta de contraseña: obligatoria, de 12 a 72 caracteres (el tope de BCrypt), con al menos una letra y un número.
- [ ] [[MatchingPasswords]] `webapp` — Restricción de clase para formularios con contraseña y confirmación ([[PasswordsMatching]]).
- [ ] [[MatchingPasswordsValidator]] `webapp` — Compara contraseña y confirmación y cuelga el error del campo de confirmación.
- [ ] [[PasswordsMatching]] `webapp` — Interfaz con los dos getters que necesita [[MatchingPasswordsValidator]].

### Service

- [ ] [[UserService]] `services-contracts` — Contrato de Cuentas: registro, verificación y reenvío, nombre, avatar, cambio y recuperación de contraseña, datos de cobro y bloqueo de fila para serializar operaciones de una misma Cuenta.
- [ ] [[UserServiceImpl]] `services` — Cuentas: registro con Cuenta sin verificar, verificación, reenvío con espera de un minuto, cambio y recuperación de contraseña, nombre, avatar y datos de cobro.
- [ ] [[DuplicateUserException]] `services-contracts` — El correo ya pertenece a una Cuenta con contraseña, o un registro simultáneo se adelantó.
- [ ] [[UserNotFoundException]] `services-contracts` — La Cuenta no existe, o no tiene perfil público.
- [ ] [[UnchangedPasswordException]] `services-contracts` — La contraseña nueva es igual a la actual, en el cambio desde el perfil o en la recuperación.
- [ ] [[InvalidCurrentPasswordException]] `services-contracts` — La contraseña actual no coincide, o cambió entre la lectura y el `UPDATE`.

### Persistencia

- [ ] [[UserDao]] `persistence-contracts` — Contrato de Cuentas: buscar por id o correo, lectura con bloqueo, proyección pública, alta, y actualizaciones condicionales (`completePending`, `markVerified`, `updatePasswordIfMatches`) que resuelven carreras en la base.
- [ ] [[UserJdbcDao]] `persistence` — Cuentas con Spring JDBC.
- [ ] [[EmailVerificationTokenDao]] `persistence-contracts` — Contrato de los tokens de verificación: crear con fecha, buscar por token, buscar el último de una Cuenta y borrar los de una Cuenta.
- [ ] [[EmailVerificationTokenJdbcDao]] `persistence` — Tokens de verificación con Spring JDBC: inserta con su fecha, busca por token, trae el último de una Cuenta y borra por Cuenta.
- [ ] [[PasswordResetTokenDao]] `persistence-contracts` — Contrato de los tokens de recuperación: crear con vencimiento, buscar, borrar por token, borrar por Cuenta y purgar vencidos.
- [ ] [[PasswordResetTokenJdbcDao]] `persistence` — Tokens de recuperación con Spring JDBC.

### Vistas

- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/register.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/register.jsp>) — Formulario de registro.
- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/login.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/login.jsp>) — Login: mirá los nombres de los campos y el token CSRF.
- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify.jsp>) — Resultado de abrir el enlace de verificación.
- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/verify-required.jsp>) — Pantalla para la cuenta sin verificar.
- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/forgot-password.jsp>) — Pedido de recuperación.
- [ ] [webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/auth/reset-password.jsp>) — Nueva contraseña con el token en un campo oculto.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/resend-verification.tag>) — Botón de reenvío: POST con CSRF.

### Tests

- [ ] [[UserServiceImplTest]] `test` — Registro (nuevo, duplicado, pendiente, carrera), verificación, reenvío con espera, cambio y recuperación de contraseña y datos de cobro, con DAOs simulados.
- [ ] [[UserJdbcDaoTest]] `test` — Altas, búsquedas por correo normalizado y las actualizaciones condicionales de la Cuenta (`completePending`, `markVerified`, cambio de clave).
- [ ] [[EmailVerificationTokenJdbcDaoTest]] `test` — Crear, buscar por token, último de una Cuenta y borrado de tokens de verificación.
- [ ] [[PasswordResetTokenJdbcDaoTest]] `test` — Crear, unicidad por Cuenta, borrado por token y por Cuenta y purga de vencidos.

**Al terminar deberías poder contestar:**

- ¿Qué pasa, paso a paso, cuando alguien se registra?
- ¿Cómo se genera, guarda y consume un token?
- ¿Cómo se guarda la contraseña?
- ¿Dónde se decide que una ruta exige cuenta verificada?
- ¿Qué pasa con las sesiones al cambiar la clave?
- ¿Cómo protegen contra CSRF?

## Etapa 6 — Correo

*16 archivos · 1.109 líneas*

**Objetivo.** Cómo sale un mail sin frenar el request ni avisar algo que después se revirtió.

**Primero, en el vault:** [[Mail delivery]] · [[Transactions and concurrency]] · [[Localization]]

### Service

- [ ] [[EmailService]] `services-contracts` — Contrato de envío de correos: siete operaciones, cada una con el `Locale` como parámetro porque el envío corre en otro hilo.
- [ ] [[EmailServiceImpl]] `services` — Arma y envía los siete correos: plantilla Thymeleaf, asunto de i18n, `MimeMessage` HTML en UTF-8.
- [ ] [[TransactionCallbacks]] `services` — Difiere una acción hasta después del commit de la transacción en curso.
- [ ] [[SupportedLocales]] `services` — Idiomas que la aplicación sabe hablar (`es`, `en`, `fr`).

### Cargas de los avisos

- [ ] [[PostInterestNotification]] `services-contracts` — Carga del correo de "consulta nueva": publicante, quién consulta, mensaje opcional y la lista de vinilos (`InterestedPost`) con la Consulta de cada uno.
- [ ] [[InquiryUpdateNotification]] `services-contracts` — Carga del correo de un cambio de Consulta: evento, consulta, destinatario y datos del álbum.
- [ ] [[InquiryEvent]] `services-contracts` — Los seis cambios de una Consulta que disparan correo: `ACCEPTED`, `RECEIPT_UPLOADED`, `RECEIPT_REQUESTED`, `CONFIRMED`, `CANCELLED` y `REJECTED`.
- [ ] [[MessageNotification]] `services-contracts` — Carga del correo de "mensaje nuevo": consulta, destinatario, quién escribió, el texto y los datos del álbum.

### Plantillas

- [ ] [services/src/main/resources/mail/email-verification.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/email-verification.html>) — Enlace de verificación.
- [ ] [services/src/main/resources/mail/inquiry-message.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/inquiry-message.html>) — Mensaje nuevo.
- [ ] [services/src/main/resources/mail/inquiry-update.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/inquiry-update.html>) — Cambio de estado de una consulta.
- [ ] [services/src/main/resources/mail/password-changed.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/password-changed.html>) — Aviso de cambio de contraseña.
- [ ] [services/src/main/resources/mail/password-reset.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/password-reset.html>) — Enlace de recuperación.
- [ ] [services/src/main/resources/mail/post-interest.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/post-interest.html>) — Consulta recibida.
- [ ] [services/src/main/resources/mail/welcome.html](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/resources/mail/welcome.html>) — Bienvenida.

### Tests

- [ ] [[EmailServiceImplTest]] `test` — Plantillas reales con un remitente falso: enlaces, asuntos por idioma, escape del texto, un vinilo o varios, y errores que no se propagan.

**Al terminar deberías poder contestar:**

- ¿En qué hilo se envía un correo y por qué?
- ¿Qué pasa si el SMTP está caído?
- ¿Por qué el envío se dispara después del commit?
- ¿En qué idioma llega y cómo se arma el enlace?

## Etapa 7 — Publicar, editar e imágenes

*40 archivos · 2.933 líneas*

**Objetivo.** El primer flujo de escritura: formulario con archivos, catálogo que se crea al publicar y fotos guardadas en la base.

**Primero, en el vault:** [[Publish flow]] · [[Edit and delete flow]] · [[Cover image flow]] · [[Gallery flow]]

### Web

- [ ] [[PublishController]] `webapp` — Publicar, editar y eliminar.
- [ ] [[PublishForm]] `webapp` — Formulario de publicar y editar: título, artista, año, género, precio, condición, zona, prensado, descripción, fotos nuevas y fotos a retirar.
- [ ] [[PublishFormValidator]] `webapp` — Reglas cruzadas de publicar: años válidos y no futuros, precio en rango, prensado no anterior al lanzamiento y hasta 5 fotos válidas.
- [ ] [[ValidPublishForm]] `webapp` — Anotación de clase que aplica [[PublishFormValidator]].
- [ ] [[ImageFiles]] `webapp` — Puente entre `MultipartFile` y [[ImageUpload]]: detecta archivo presente, valida con [[ImageRules]] mirando el tamaño antes de leer los bytes y convierte.
- [ ] [[PostAccessHandler]] `webapp` — Bean `postAccess` de `@PreAuthorize`: quien edita o elimina es el publicante.
- [ ] [[ImageController]] `webapp` — Sirve imágenes desde el recurso al que pertenecen (post, usuario, álbum) con caché de un año.
- [ ] [[ImageNotFoundException]] `webapp` — La imagen no existe o no pertenece al recurso de la URL.
- [ ] [[MultipartExceptionHandlerFilter]] `webapp` — Filtro que envuelve al multipart: si el request excede el tamaño máximo, redirige al formulario de origen con un aviso en lugar de un error 500.

### Services

- [ ] [[ArtistService]] `services-contracts` — Contrato del catálogo de artistas: buscar o crear por identidad normalizada, resolver al editar y sugerencias para el autocompletado.
- [ ] [[ArtistServiceImpl]] `services` — Busca o crea el artista por identidad: el nombre en minúsculas, solo letras y dígitos.
- [ ] [[AlbumService]] `services-contracts` — Contrato del catálogo de álbumes: buscar o crear por identidad, y resolver al editar actualizando título y género.
- [ ] [[AlbumServiceImpl]] `services` — Busca o crea el álbum por artista, título y año.
- [ ] [[ImageService]] `services-contracts` — Contrato de imágenes: lectura por pertenencia (post, avatar, álbum), alta validada, borrado condicional y galería.
- [ ] [[ImageServiceImpl]] `services` — Valida tipo, tamaño y firma antes de guardar.
- [ ] [[DuplicatePostException]] `services-contracts` — La Cuenta ya publicó ese álbum.
- [ ] [[ConcurrentPublishException]] `services-contracts` — Otra publicación simultánea creó el mismo artista o álbum.
- [ ] [[InvalidPostDataException]] `services-contracts` — Defensa del contrato de [[PostServiceImpl]]: año o precio fuera de rango.
- [ ] [[InvalidImageException]] `services-contracts` — La imagen no cumple [[ImageRules]], o al editar se intenta retirar una foto ajena o superar el tope.
- [ ] [[PostUnavailableException]] `services-contracts` — La publicación ya no está disponible para consultar, editar o eliminar.

### Persistencia

- [ ] [[ArtistDao]] `persistence-contracts` — Contrato de persistencia de artistas: buscar o crear por nombre normalizado, actualizar el nombre visible y sugerencias.
- [ ] [[ArtistJdbcDao]] `persistence` — Artistas con Spring JDBC.
- [ ] [[AlbumDao]] `persistence-contracts` — Contrato de persistencia de álbumes: buscar por artista, título y año sin distinguir mayúsculas, crear y actualizar título y género.
- [ ] [[AlbumJdbcDao]] `persistence` — Álbumes con Spring JDBC.
- [ ] [[ImageDao]] `persistence-contracts` — Contrato de imágenes: crear, borrar si nadie la referencia y buscar exigiendo pertenencia a un post, un usuario o un álbum.
- [ ] [[ImageJdbcDao]] `persistence` — Imágenes con Spring JDBC.
- [ ] [[PostImageDao]] `persistence-contracts` — Contrato de la galería: ids de las fotos adicionales en orden, agregar una en una posición y borrar las de un post.
- [ ] [[PostImageJdbcDao]] `persistence` — Galería con Spring JDBC: lista los ids por `display_order`, agrega y borra por post.
- [ ] [[DuplicatePostKeyException]] `persistence-contracts` — Marca de persistencia: el `INSERT` o `UPDATE` de un post violó la unicidad `(user_id, album_id)`.

### Vista

- [ ] [webapp/src/main/webapp/WEB-INF/views/publish/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/publish/index.jsp>) — Publicar y editar comparten vista.
- [ ] [webapp/src/main/webapp/js/publish-preview.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/publish-preview.js>) — Vista previa de la tarjeta mientras se completa el formulario.
- [ ] [webapp/src/main/webapp/images/covers/placeholder.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/covers/placeholder.svg>) — Tapa por defecto.

### Tests

- [ ] [[ArtistServiceImplTest]] `test` — Identidad normalizada, edición del nombre visible y sugerencias.
- [ ] [[AlbumServiceImplTest]] `test` — Buscar o crear y resolver al editar.
- [ ] [[ImageServiceImplTest]] `test` — Validación de tipo, tamaño y firma, y reemplazo de galería.
- [ ] [[InMemoryImageService]] `test` — Doble de [[ImageService]] en memoria para los tests de services: aplica las mismas [[ImageRules]] y permite assertear el estado guardado sin `Mockito.verify`.
- [ ] [[ArtistJdbcDaoTest]] `test` — Buscar o crear por nombre normalizado, nombre visible y sugerencias sin tildes.
- [ ] [[AlbumJdbcDaoTest]] `test` — Identidad sin distinguir mayúsculas, alta y actualización de metadatos.
- [ ] [[ImageJdbcDaoTest]] `test` — Lectura por pertenencia a post, usuario y álbum, y borrado condicional.
- [ ] [[PostImageJdbcDaoTest]] `test` — Orden de la galería, alta y borrado por post.

**Al terminar deberías poder contestar:**

- ¿Qué pasa si dos personas publican el mismo álbum nuevo a la vez?
- ¿Cómo se valida que un archivo sea una imagen?
- ¿Dónde se guardan las fotos y cómo se sirven?
- ¿Quién puede editar o borrar una publicación?

## Etapa 8 — Ficha, contacto, direcciones y datos de cobro

*31 archivos · 1.667 líneas*

**Objetivo.** Cómo un comprador abre una consulta y qué datos propios necesita cada parte.

**Primero, en el vault:** [[Post detail flow]] · [[Contact flow]] · [[Addresses and payment flow]]

### Ficha

- [ ] [[PostController]] `webapp` — Ficha pública `GET /post/{id}`: pide a [[CartService]] la ficha con lo que se le ofrece a quien mira y resuelve a dónde volver.
- [ ] [webapp/src/main/webapp/WEB-INF/views/post/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/detail.jsp>) — Ficha: galería, vendedor, acciones según quién mira.
- [ ] [webapp/src/main/webapp/js/post-gallery.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/post-gallery.js>) — Cambia la foto principal al tocar una miniatura.

### Contacto

- [ ] [[PostContactController]] `webapp` — Formulario de contacto de una publicación: carga el post contactable y las opciones de envío, y envía la consulta con dirección guardada o nueva.
- [ ] [[ContactForm]] `webapp` — Formulario de contacto: hereda la dirección de [[ShippingAddressForm]] y suma el mensaje opcional de hasta 500 caracteres.
- [ ] [[ShippingAddressForm]] `webapp` — Dirección de envío de una Consulta: una guardada (`addressId`) o una nueva con estos mismos campos.
- [ ] [[ShippingAddressValidator]] `webapp` — Con dirección guardada elegida no valida nada.
- [ ] [[ValidShippingAddress]] `webapp` — Anotación de clase que aplica [[ShippingAddressValidator]].
- [ ] [[LineBreakNormalizingEditor]] `webapp` — Editor de binding que normaliza CRLF a LF y recorta.
- [ ] [[ContactRules]] `services` — La única definición de "se puede consultar": disponible, ajeno y sin una Consulta abierta del comprador.
- [ ] [[OpenInquiryExistsException]] `services-contracts` — El comprador ya tiene una Consulta abierta sobre ese post.
- [ ] [webapp/src/main/webapp/WEB-INF/views/post/contact.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/post/contact.jsp>) — Mensaje y elección de dirección.

### Direcciones

- [ ] [[AddressService]] `services-contracts` — Contrato de la libreta: direcciones activas y opciones de envío en una lectura, alta con tope de 3, reemplazo (archiva y crea) y baja lógica.
- [ ] [[AddressServiceImpl]] `services` — Libreta de direcciones con tope de 3 activas.
- [ ] [[AddressDao]] `persistence-contracts` — Contrato de persistencia de direcciones: crear, buscar por id, listar activas de una Cuenta, archivar y contar activas.
- [ ] [[AddressJdbcDao]] `persistence` — Direcciones con Spring JDBC.
- [ ] [[AddressForm]] `webapp` — Formulario de una dirección de la libreta: calle, altura, ciudad, provincia y código postal obligatorios, con sus largos máximos.
- [ ] [[AddressAccessHandler]] `webapp` — Bean `addressAccess` de `@PreAuthorize`: solo el dueño edita o elimina una dirección.
- [ ] [[AddressLimitExceededException]] `services-contracts` — La Cuenta ya tiene el máximo de direcciones activas.
- [ ] [[AddressNotFoundException]] `services-contracts` — La dirección no existe, es de otra Cuenta o está archivada.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/address-fields.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address-fields.tag>) — Campos de una dirección.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/address.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/address.tag>) — Muestra una dirección, completa o recortada.

### Datos de cobro

- [ ] [[PaymentForm]] `webapp` — Datos de cobro: CBU y alias, los dos opcionales (vaciarlos borra los datos).
- [ ] [[PaymentFormValidator]] `webapp` — Vacío es válido.
- [ ] [[ValidPaymentForm]] `webapp` — Anotación de clase que aplica [[PaymentFormValidator]].
- [ ] [[InvalidPaymentInfoException]] `services-contracts` — CBU o alias con formato inválido que llegó al service salteando el formulario.
- [ ] [[PaymentInfoRequiredException]] `services-contracts` — No se pueden vaciar los datos de cobro con una venta abierta: el comprador se quedaría sin dónde transferir.
- [ ] [[MissingPaymentInfoException]] `services-contracts` — El publicante quiso aceptar una consulta sin datos de cobro.

### Tests

- [ ] [[ContactRulesTest]] `test` — Las combinaciones de estado del post, dueño y consulta abierta, con y sin sesión.
- [ ] [[AddressServiceImplTest]] `test` — Opciones de envío, tope de direcciones, reemplazo, archivado y pertenencia.
- [ ] [[AddressJdbcDaoTest]] `test` — Alta, activas por Cuenta, archivado con guarda y conteo.

**Al terminar deberías poder contestar:**

- ¿Qué se valida antes de crear una consulta?
- ¿Por qué una dirección se archiva en vez de borrarse?
- ¿Cómo se sostiene el tope de tres direcciones con dos pestañas abiertas?
- ¿Qué ve el vendedor de la dirección antes de aceptar?

## Etapa 9 — Consulta, venta y conversación

*35 archivos · 5.069 líneas*

**Objetivo.** El corazón del negocio: una máquina de estados con bloqueos, comprobante, mensajes y un correo por cada cambio.

**Primero, en el vault:** [[Inquiry and sale flow]] · [[Conversation flow]] · [[Status filters flow]] · [[Transactions and concurrency]]

### Web

- [ ] [[InquiryController]] `webapp` — Bandejas con filtro por estado (`status`), página de la consulta y un endpoint por transición de la venta, además de mensajes, reseñas y descarga del comprobante con headers de seguridad.
- [ ] [[InquiryAccessHandler]] `webapp` — Bean `inquiryAccess` de `@PreAuthorize`: comprador, publicante o cualquiera de las dos partes de una consulta.
- [ ] [[MessageForm]] `webapp` — Un Mensaje nuevo: texto obligatorio hasta 500 caracteres.
- [ ] [[ReceiptForm]] `webapp` — Formulario del comprobante: un archivo validado con [[ValidReceipt]].
- [ ] [[ReceiptValidator]] `webapp` — Valida el comprobante con [[ReceiptRules]] mirando el tamaño antes de leer los bytes.
- [ ] [[ValidReceipt]] `webapp` — Anotación de campo que aplica [[ReceiptValidator]].

### Service

- [ ] [[InquiryService]] `services-contracts` — Contrato de consultas y ventas: contactar, envío en lote del carrito, bandejas agrupadas con filtro opcional por [[InquiryStatusFilter]] y sus conteos, transiciones de la venta, comprobante, conversación, reseñas, consultas de pertenencia para [[InquiryAccessHandler]] y `findSaleToResume`, la venta a la que vuelve el vendedor después de cargar sus datos de cobro.
- [ ] [[InquiryServiceImpl]] `services` — Consultas, ventas, conversación y reseñas.
- [ ] [[InquiryNotFoundException]] `services-contracts` — La Consulta no existe.
- [ ] [[InvalidInquiryStateException]] `services-contracts` — La transición no encontró la Consulta o el post en el estado esperado.
- [ ] [[InvalidMessageException]] `services-contracts` — El texto del Mensaje no cumple [[MessageRules]].
- [ ] [[InvalidReceiptException]] `services-contracts` — El comprobante no cumple [[ReceiptRules]].
- [ ] [[ReceiptNotFoundException]] `services-contracts` — La Consulta no tiene comprobante cargado.
- [ ] [[ForbiddenOperationException]] `services-contracts` — La operación existe pero no le corresponde a quien la pide: consultar un post propio, operar una consulta o una dirección ajena.

### Persistencia

- [ ] [[InquiryDao]] `persistence-contracts` — Contrato de consultas: crear una o varias en lote, bandejas paginadas por publicación y filtradas por un conjunto de estados, conteo por estado para los chips, resumen y partes, transiciones de estado con guarda, `startSale` (pasa a espera de pago y fija el precio en un solo `UPDATE`), comprobante, consultas abiertas de un comprador, rechazo de las demás pendientes y desenganche al eliminar un post.
- [ ] [[InquiryJdbcDao]] `persistence` — Consultas con Spring JDBC.
- [ ] [[MessageDao]] `persistence-contracts` — Contrato de mensajes de una conversación: crear y listar por consulta en orden de llegada.
- [ ] [[MessageJdbcDao]] `persistence` — Mensajes con Spring JDBC.

### Vistas

- [ ] [webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/received.jsp>) — Bandeja del vendedor, agrupada por publicación.
- [ ] [webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/sent.jsp>) — Bandeja del comprador.
- [ ] [webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/inquiry/detail.jsp>) — La página de la venta: acciones según estado y rol, conversación, reseña.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-nav.tag>) — Pestañas recibidas y enviadas.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inquiry-status.tag>) — Estado de la consulta como texto.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-group-header.tag>) — Cabecera de un grupo de la bandeja: miniatura, título y estado. Elige la URL de la tapa según exista o no el post.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/inbox-last-message.tag>) — Último mensaje de la conversación.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/filter-chips.tag>) — Chips de filtro con su cantidad; el chip activo lleva a la URL sin filtro.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/confirm-dialog.tag>) — Diálogo de confirmación.
- [ ] [webapp/src/main/webapp/js/confirm-action.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>) — Abre el diálogo antes de enviar un formulario destructivo.
- [ ] [webapp/src/main/webapp/js/submit-once.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/submit-once.js>) — Evita el doble envío.
- [ ] [webapp/src/main/webapp/js/sale-detail.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/sale-detail.js>) — Página de la venta: alto de la conversación, scroll al último mensaje, Enter para enviar y cancelar la edición de la reseña.

### Tests

- [ ] [[InquiryServiceImplTest]] `test` — Contactabilidad, alta, bandejas (también filtradas), cada transición de la venta con sus estados inválidos (incluida una aceptación cuya transición falla), direcciones parciales, mensajes, reseñas, alta en lote, venta a la que volver y avisos después del commit.
- [ ] [[InquiryStatusFilterTest]] `test` — Que [[InquiryStatusFilter]] sume bien por filtro, que cada estado caiga en exactamente un filtro y que sin consultas los conteos queden vacíos.
- [ ] [[InquiryJdbcDaoTest]] `test` — Bandejas agrupadas y paginadas (incluidos posts eliminados), filtro por estado (grupos mixtos, sin coincidencias, conteo de grupos) y conteo por estado, guardas de estado, `startSale` con precio fijado, precio actual mientras está pendiente, avatares de las partes, comprobante, consultas abiertas, alta en lote y desenganche.
- [ ] [[MessageJdbcDaoTest]] `test` — Alta de mensajes y orden por llegada.
- [ ] [[ReceiptTest]] `test` — Que [[Receipt]] no comparta su arreglo de bytes: cambiar el original o el devuelto no altera el comprobante.

**Al terminar deberías poder contestar:**

- ¿Qué estados tiene una consulta y quién puede pasar de uno a otro?
- ¿Qué pasa si el vendedor acepta dos consultas a la vez?
- ¿Qué fila se bloquea y por qué esa?
- ¿Dónde se guarda el comprobante y quién puede descargarlo?
- ¿Cuándo se cierra una conversación?

## Etapa 10 — Reseñas y perfiles

*27 archivos · 2.294 líneas*

**Objetivo.** Lo que pasa después de una venta y las dos caras del perfil: la privada y la pública.

**Primero, en el vault:** [[Reviews flow]] · [[Profile flow]] · [[Public profile flow]]

### Reseñas

- [ ] [[ReviewService]] `services-contracts` — Contrato de reseñas.
- [ ] [[ReviewServiceImpl]] `services` — Guarda (actualizando la fila existente o creando) y quita (borrado lógico) reseñas con propagación `MANDATORY`.
- [ ] [[ReviewDao]] `persistence-contracts` — Contrato de reseñas: buscar la de un autor en una venta, listar las activas de una Cuenta por rol y con `LIMIT`/`OFFSET`, estadísticas por rol, crear, actualizar (reactivando) y desactivar.
- [ ] [[ReviewJdbcDao]] `persistence` — Reseñas con Spring JDBC.
- [ ] [[ReviewForm]] `webapp` — Reseña: puntaje obligatorio de 1 a 5 y comentario opcional hasta 500.
- [ ] [[InvalidReviewException]] `services-contracts` — La reseña no cumple [[ReviewRules]].
- [ ] [webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/star-rating-input.tag>) — Estrellas como radios accesibles.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/rating.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/rating.tag>) — Estrellas de solo lectura con relleno parcial para promedios.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/review-content.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/review-content.tag>) — Puntaje, comentario y, opcional, autor de una reseña.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/user-byline.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/user-byline.tag>) — Foto y nombre de una Cuenta con enlace a su perfil público.

### Perfil privado

- [ ] [[ProfileController]] `webapp` — Perfil privado: nombre, foto, contraseña, datos de cobro y libreta de direcciones, con las publicaciones propias paginadas y filtrables por estado (`postStatus`).
- [ ] [[ProfileForm]] `webapp` — Edición del nombre visible: obligatorio y hasta 100 caracteres.
- [ ] [[ChangePasswordForm]] `webapp` — Cambio de contraseña desde el perfil: clave actual obligatoria, nueva con [[ValidPassword]] y confirmación con [[MatchingPasswords]].
- [ ] [[AvatarForm]] `webapp` — Formulario de la foto de perfil: un archivo o la marca `remove`.
- [ ] [[AvatarFormValidator]] `webapp` — Quitar la foto no necesita archivo.
- [ ] [[ValidAvatarForm]] `webapp` — Anotación de clase que aplica [[AvatarFormValidator]].
- [ ] [webapp/src/main/webapp/WEB-INF/views/profile/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/index.jsp>) — Perfil privado: cuenta, contraseña, cobro, direcciones, publicaciones.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/account-nav.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/account-nav.tag>) — Menú de la cuenta en la cabecera.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/avatar.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/avatar.tag>) — Foto o inicial.
- [ ] [webapp/src/main/webapp/js/account-edit.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/account-edit.js>) — Filas editables del perfil y diálogo de la foto.

### Perfil público

- [ ] [[PublicProfileController]] `webapp` — `GET /users/{id}`: perfil público con publicaciones a la venta y reseñas paginadas por rol (`reviewRole`, `reviewPage`).
- [ ] [[PublicProfileService]] `services-contracts` — Contrato del perfil público: una operación que compone Cuenta, publicaciones y una página de reseñas del rol pedido.
- [ ] [[PublicProfileServiceImpl]] `services` — Compone el perfil público con la Cuenta verificada, sus publicaciones disponibles y una página de sus reseñas para el rol pedido.
- [ ] [webapp/src/main/webapp/WEB-INF/views/profile/public.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/public.jsp>) — Perfil público: reputación, publicaciones, reseñas.

### Tests

- [ ] [[ReviewServiceImplTest]] `test` — Guardar, reemplazar, quitar, reglas de la reseña y páginas por rol (primera, segunda, vacía e inválida).
- [ ] [[ReviewJdbcDaoTest]] `test` — Alta, actualización que reactiva, desactivación, listado y estadísticas por rol, paginación con `OFFSET` y foto del autor.
- [ ] [[PublicProfileServiceImplTest]] `test` — Composición del perfil público con la página de reseñas del rol pedido.

**Al terminar deberías poder contestar:**

- ¿Quién puede reseñar a quién y cuándo?
- ¿Cómo se cambia la contraseña con sesión iniciada y qué pasa después?
- ¿Qué datos de una cuenta son públicos?

## Etapa 11 — Carrito

*12 archivos · 1.459 líneas*

**Objetivo.** La funcionalidad más nueva: junta todo lo anterior (contacto, direcciones, bloqueos, correo) en una operación en lote.

**Primero, en el vault:** [[Cart flow]]

### Web

- [ ] [[CartController]] `webapp` — Carrito: ver, agregar desde la ficha (vuelve al listado de origen), quitar y enviar.
- [ ] [[CartCountAdvice]] `webapp` — Deja en cada request, para Cuentas verificadas, un contador perezoso del carrito que la cabecera lee.
- [ ] [[CartExceptionAdvice]] `webapp` — Solo para [[CartController]] y con prioridad sobre [[ErrorResponseAdvice]]: convierte los motivos por los que el carrito no puede agregar o enviar en una redirección a la pantalla de origen con su aviso.
- [ ] [webapp/src/main/webapp/WEB-INF/views/cart/index.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/cart/index.jsp>) — Carrito agrupado por publicante. Mirá la URL de la tapa (línea 53).

### Service y persistencia

- [ ] [[CartService]] `services-contracts` — Contrato del carrito: agregar, quitar, pantalla de envío, contador, la ficha de un post con lo que se le ofrece a quien mira, y enviar con una dirección guardada o nueva.
- [ ] [[CartServiceImpl]] `services` — Carrito de consultas.
- [ ] [[CartAddRejectedException]] `services-contracts` — El post no se pudo agregar al carrito.
- [ ] [[NothingToSendException]] `services-contracts` — Al enviar el carrito, ningún post se podía consultar.
- [ ] [[CartItemDao]] `persistence-contracts` — Contrato de persistencia del carrito: agregar, quitar, quitar varios, saber si un post está, y listar o contar filtrando por estado del post y por consultas que lo ocultan.
- [ ] [[CartItemJdbcDao]] `persistence` — Carrito con Spring JDBC.

### Tests

- [ ] [[CartServiceImplTest]] `test` — Agregar con cada motivo de rechazo (incluido un post que se vende antes del bloqueo), tope, pantalla de envío, envío parcial, nada para enviar y dirección nueva.
- [ ] [[CartItemJdbcDaoTest]] `test` — Agregar, repetidos, quitar, quitar varios y el filtro de consultables por estado del post y consultas abiertas.

**Al terminar deberías poder contestar:**

- ¿Qué pasa al enviar el carrito si un vinilo ya no está disponible?
- ¿Por qué los posts se bloquean en orden de id?
- ¿Cuántos correos salen y a quién?

## Etapa 12 — Errores

*6 archivos · 184 líneas*

**Objetivo.** Cómo una excepción de negocio se convierte en una respuesta HTTP.

**Primero, en el vault:** [[Validation and errors]]

### Handlers y páginas

- [ ] [[ErrorResponseAdvice]] `webapp` — Único lugar donde las excepciones de negocio se vuelven respuestas: no encontrado → 404, ajeno → 403, dato que saltea la validación (imagen, reseña, datos del post o de cobro) o parámetro mal tipado → 400.
- [ ] [[ErrorController]] `webapp` — Vistas de 403 y 404 a las que hacen forward Spring Security y el contenedor.
- [ ] [webapp/src/main/webapp/WEB-INF/views/error/400.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/400.jsp>) — Pedido inválido.
- [ ] [webapp/src/main/webapp/WEB-INF/views/error/403.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/403.jsp>) — Sin permiso.
- [ ] [webapp/src/main/webapp/WEB-INF/views/error/404.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/404.jsp>) — No encontrado.
- [ ] [webapp/src/main/webapp/WEB-INF/views/error/409.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/error/409.jsp>) — Conflicto: el estado cambió.

**Al terminar deberías poder contestar:**

- ¿Cuándo responde 403 y cuándo 404?
- ¿Qué es un 409 en este proyecto?
- ¿Dónde se valida y por qué dos veces?

## Etapa 13 — Interfaz compartida

*20 archivos · 3.467 líneas*

**Objetivo.** Los componentes JSP, estilos e imágenes que usan todas las páginas.

**Primero, en el vault:** [[UI components]] · [[UI styles and tokens]] · [[Views and assets]]

### Estructura de página

- [ ] [webapp/src/main/webapp/WEB-INF/tags/head.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/head.tag>) — Cabecera HTML común: estilos y scripts.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/site-header.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/site-header.tag>) — Barra superior: marca, buscador, acciones, aviso de verificación.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/brand.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/brand.tag>) — Marca.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/back-link.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/back-link.tag>) — Enlace de volver.

### Texto y acciones

- [ ] [webapp/src/main/webapp/WEB-INF/tags/h1.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h1.tag>) — Título.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/h3.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/h3.tag>) — Subtítulo con nivel configurable.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/p.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/p.tag>) — Párrafo.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/span.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/span.tag>) — Texto en línea.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/icon.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/icon.tag>) — Iconos SVG de una lista cerrada.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/button.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/button.tag>) — Botón o enlace con variantes.

### Controles de formulario

- [ ] [webapp/src/main/webapp/WEB-INF/tags/text-input.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/text-input.tag>) — Campo ligado a un form con etiqueta, pista y error.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/input-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/input-control.tag>) — Input sin ligar, con soporte de sugerencias.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/textarea.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/textarea.tag>) — Área de texto ligada.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/select.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select.tag>) — Select ligado.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/select-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/select-control.tag>) — Select sin ligar.
- [ ] [webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/segmented-control.tag>) — Grupo de radios.

### Estilos e imágenes

- [ ] [webapp/src/main/webapp/css/tokens.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/tokens.css>) — Variables de color, tipografía y espacio.
- [ ] [webapp/src/main/webapp/css/components.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/components.css>) — Estilos de los componentes.
- [ ] [webapp/src/main/webapp/css/style.css](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/css/style.css>) — Estilos por página. Largo: recorrelo por secciones.
- [ ] [webapp/src/main/webapp/images/logo.svg](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/images/logo.svg>) — Isotipo.

**Al terminar deberías poder contestar:**

- ¿Cómo se evita XSS en las vistas?
- ¿Por qué todas las URL pasan por c:url?
- ¿Qué funciona sin JavaScript?

## Etapa 14 — Textos

*4 archivos · 1.596 líneas*

**Objetivo.** Los bundles de mensajes. No hace falta leerlos enteros: recorré los prefijos y compará un mismo bloque en los tres idiomas.

**Primero, en el vault:** [[Localization]]

### Bundles

- [ ] [webapp/src/main/resources/i18n/messages.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages.properties>) — Por defecto, español.
- [ ] [webapp/src/main/resources/i18n/messages_en.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_en.properties>) — Inglés.
- [ ] [webapp/src/main/resources/i18n/messages_fr.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_fr.properties>) — Francés.
- [ ] [webapp/src/main/resources/i18n/messages_es.properties](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/resources/i18n/messages_es.properties>) — Vacío a propósito.

**Al terminar deberías poder contestar:**

- ¿Cómo se elige el idioma de una página y el de un correo?
- ¿Qué pasa si falta una key?

## Etapa 15 — Herramientas del repositorio

*70 archivos · 7.556 líneas*

**Objetivo.** Chequeos previos al commit y material para agentes de código. No forma parte de la aplicación.

**Primero, en el vault:** [[Development tools]] · [[Repository tooling]] · [[Testing and evidence]]

### Chequeos

- [ ] [tools/paw_checks.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/paw_checks.py>) — Tres chequeos estáticos.
- [ ] [tools/git-hooks/pre-commit](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/git-hooks/pre-commit>) — Corre los chequeos antes del commit.

### Hooks de Claude Code

- [ ] [.claude/hooks/commit-gate.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/commit-gate.py>)
- [ ] [.claude/hooks/db-server-guard.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/db-server-guard.py>)
- [ ] [.claude/hooks/i18n-parity-posttool.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/i18n-parity-posttool.py>)
- [ ] [.claude/hooks/skill-autolaunch.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/hooks/skill-autolaunch.py>)

### Procedimientos para agentes (lectura opcional)

- [ ] [.claude/skills/PROJECT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/PROJECT.md>)
- [ ] [.claude/skills/README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/README.md>)
- [ ] [.claude/skills/bug/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/bug/SKILL.md>)
- [ ] [.claude/skills/corrector-eyes/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/corrector-eyes/SKILL.md>)
- [ ] [.claude/skills/design/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/design/SKILL.md>)
- [ ] [.claude/skills/enhancer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/enhancer/SKILL.md>)
- [ ] [.claude/skills/feature-engineering/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/feature-engineering/SKILL.md>)
- [ ] [.claude/skills/feature-engineering/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/feature-engineering/context.md>)
- [ ] [.claude/skills/forensic-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/forensic-audit/SKILL.md>)
- [ ] [.claude/skills/frontend-analyzer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/SKILL.md>)
- [ ] [.claude/skills/frontend-analyzer/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/context.md>)
- [ ] [.claude/skills/frontend-analyzer/scripts/research.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/frontend-analyzer/scripts/research.py>)
- [ ] [.claude/skills/general-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/general-audit/SKILL.md>)
- [ ] [.claude/skills/good-practice/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/good-practice/SKILL.md>)
- [ ] [.claude/skills/handoff/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/handoff/SKILL.md>)
- [ ] [.claude/skills/i18n-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/i18n-sync/SKILL.md>)
- [ ] [.claude/skills/implementation/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/implementation/SKILL.md>)
- [ ] [.claude/skills/jdbc-to-jpa/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/jdbc-to-jpa/SKILL.md>)
- [ ] [.claude/skills/planning/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/planning/SKILL.md>)
- [ ] [.claude/skills/pre-delivery/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/pre-delivery/SKILL.md>)
- [ ] [.claude/skills/skillset-port/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/skillset-port/SKILL.md>)
- [ ] [.claude/skills/smoke/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/smoke/SKILL.md>)
- [ ] [.claude/skills/wiki-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.claude/skills/wiki-sync/SKILL.md>)
- [ ] [.agents/skills/PROJECT.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/PROJECT.md>)
- [ ] [.agents/skills/README.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/README.md>)
- [ ] [.agents/skills/bug/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/bug/SKILL.md>)
- [ ] [.agents/skills/corrector-eyes/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/corrector-eyes/SKILL.md>)
- [ ] [.agents/skills/design/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/design/SKILL.md>)
- [ ] [.agents/skills/enhancer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/enhancer/SKILL.md>)
- [ ] [.agents/skills/feature-engineering/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/feature-engineering/SKILL.md>)
- [ ] [.agents/skills/feature-engineering/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/feature-engineering/context.md>)
- [ ] [.agents/skills/forensic-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/forensic-audit/SKILL.md>)
- [ ] [.agents/skills/frontend-analyzer/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/SKILL.md>)
- [ ] [.agents/skills/frontend-analyzer/context.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/context.md>)
- [ ] [.agents/skills/frontend-analyzer/scripts/research.py](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/frontend-analyzer/scripts/research.py>)
- [ ] [.agents/skills/general-audit/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/general-audit/SKILL.md>)
- [ ] [.agents/skills/good-practice/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/good-practice/SKILL.md>)
- [ ] [.agents/skills/handoff/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/handoff/SKILL.md>)
- [ ] [.agents/skills/i18n-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/i18n-sync/SKILL.md>)
- [ ] [.agents/skills/implementation/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/implementation/SKILL.md>)
- [ ] [.agents/skills/jdbc-to-jpa/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/jdbc-to-jpa/SKILL.md>)
- [ ] [.agents/skills/planning/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/planning/SKILL.md>)
- [ ] [.agents/skills/pre-delivery/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/pre-delivery/SKILL.md>)
- [ ] [.agents/skills/skillset-port/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/skillset-port/SKILL.md>)
- [ ] [.agents/skills/smoke/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/smoke/SKILL.md>)
- [ ] [.agents/skills/wiki-sync/SKILL.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.agents/skills/wiki-sync/SKILL.md>)
- [ ] [.codex/prompts/bug.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/bug.md>)
- [ ] [.codex/prompts/corrector-eyes.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/corrector-eyes.md>)
- [ ] [.codex/prompts/design.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/design.md>)
- [ ] [.codex/prompts/enhancer.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/enhancer.md>)
- [ ] [.codex/prompts/feature-engineering.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/feature-engineering.md>)
- [ ] [.codex/prompts/forensic-audit.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/forensic-audit.md>)
- [ ] [.codex/prompts/frontend-analyzer.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/frontend-analyzer.md>)
- [ ] [.codex/prompts/general-audit.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/general-audit.md>)
- [ ] [.codex/prompts/good-practice.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/good-practice.md>)
- [ ] [.codex/prompts/handoff.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/handoff.md>)
- [ ] [.codex/prompts/i18n-sync.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/i18n-sync.md>)
- [ ] [.codex/prompts/implementation.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/implementation.md>)
- [ ] [.codex/prompts/jdbc-to-jpa.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/jdbc-to-jpa.md>)
- [ ] [.codex/prompts/planning.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/planning.md>)
- [ ] [.codex/prompts/pre-delivery.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/pre-delivery.md>)
- [ ] [.codex/prompts/skillset-port.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/skillset-port.md>)
- [ ] [.codex/prompts/smoke.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/smoke.md>)
- [ ] [.codex/prompts/wiki-sync.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/.codex/prompts/wiki-sync.md>)

**Al terminar deberías poder contestar:**

- ¿Qué verifica cada chequeo y qué error evita?
- ¿Qué prueban los tests y qué no?

## Etapa 16 — Historia: especificaciones, planes e issues

*28 archivos · 8.295 líneas*

**Objetivo.** Para entender por qué algo es como es. Leé la especificación de una funcionalidad después de haber leído su código.

**Primero, en el vault:** [[History and specifications]] · [[Recent changes 2026-10-05]] · [[Recent changes 2026-10-04]] · [[Known gaps and document drift]]

### Especificaciones

- [ ] [docs/specs/feature_cambio-contrasena_20260920.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_cambio-contrasena_20260920.md>)
- [ ] [docs/specs/feature_contacto-post_20260904.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_contacto-post_20260904.md>)
- [ ] [docs/specs/feature_perfil-consultas-ui_20260921.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_perfil-consultas-ui_20260921.md>)
- [ ] [docs/specs/feature_publicacion-albumes_20260904.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_publicacion-albumes_20260904.md>)
- [ ] [docs/specs/feature_venta-con-comprobante_20260924.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/feature_venta-con-comprobante_20260924.md>) — Especificación de la venta.
- [ ] [docs/specs/landing-quiero-vinilos.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/specs/landing-quiero-vinilos.md>)

### Planes

- [ ] [docs/plans/carrito-consultas.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/carrito-consultas.md>) — Plan del carrito.
- [ ] [docs/plans/entrega-intermedia/02-configuracion-y-deploy.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/02-configuracion-y-deploy.md>)
- [ ] [docs/plans/entrega-intermedia/03-autenticacion-permisos.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/03-autenticacion-permisos.md>)
- [ ] [docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/04-venta-ejemplar-unico.md>)
- [ ] [docs/plans/entrega-intermedia/05-filtros-publicaciones.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/05-filtros-publicaciones.md>)
- [ ] [docs/plans/entrega-intermedia/06-selling-flow.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/entrega-intermedia/06-selling-flow.md>)
- [ ] [docs/plans/perfil-consultas-ui.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/perfil-consultas-ui.md>) — Plan del rediseño de perfil y consultas. Muy largo.
- [ ] [docs/plans/venta-con-comprobante.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/plans/venta-con-comprobante.md>) — Plan de la venta. Muy largo: usalo como consulta.

### Issues

- [ ] [docs/issues/01-mostrar-primer-album-en-landing.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/01-mostrar-primer-album-en-landing.md>)
- [ ] [docs/issues/02-completar-catalogo-inicial.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/02-completar-catalogo-inicial.md>)
- [ ] [docs/issues/03-terminar-landing-editorial-responsive.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/03-terminar-landing-editorial-responsive.md>)
- [ ] [docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/conversacion-consulta/01-conversacion-de-una-consulta.md>) — Diseño de la conversación.
- [ ] [docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/observaciones-sprint-2/01-cuenta-verificada-busqueda-suggestions-autorizacion.md>) — Las cuatro observaciones de la cátedra y su resolución. Lectura obligada antes de la defensa.
- [ ] [docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/01-convertir-artist-en-entidad.md>)
- [ ] [docs/issues/publicacion-albumes/02-publicar-album-nuevo.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/02-publicar-album-nuevo.md>)
- [ ] [docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/03-reutilizar-catalogo-en-publicaciones.md>)
- [ ] [docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-albumes/04-rechazar-posts-duplicados.md>)
- [ ] [docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-mailing/01-contactar-publicante-desde-post.md>)
- [ ] [docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/publicacion-mailing/02-recuperarse-de-fallo-de-entrega.md>)
- [ ] [docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/01-seguimiento-de-consultas-por-publicacion.md>)
- [ ] [docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/02-confirmar-venta-de-ejemplar-unico.md>)
- [ ] [docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/docs/issues/selling-flow/03-avisar-al-comprador-aceptado.md>)

**Al terminar deberías poder contestar:**

- ¿Qué observó la cátedra en el sprint 2 y cómo se resolvió?
- ¿Qué documentos del repositorio quedaron desactualizados?
