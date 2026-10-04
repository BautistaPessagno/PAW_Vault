@title: Schema history and seeds
@categories: Persistence, History
@module: persistence
@files: persistence/src/test/resources/populator.sql, persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java, database/seed_dev_posts.sql, database/demo_posts.tsv, tools/seed_local_data.sh, tools/sql/demo-users.sql, tools/setup_local_postgres.sh
@extra_sources: persistence/src/main/resources/db/migration/V1__esquema_inicial.sql, persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql, persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql, persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql, persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql, persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql, persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql, persistence/src/main/resources/db/migration/V8__post_gallery.sql, persistence/src/main/resources/db/migration/V9__user_avatars.sql, persistence/src/main/resources/db/migration/V10__sale_reviews.sql, persistence/src/main/resources/db/migration/V11__carrito.sql, database/users.sql

> [!summary] En una frase
> El esquema dejó de ser un `schema.sql` que se reejecutaba y pasó a ser una serie de migraciones Flyway; esta nota guarda el texto de las once y explica de dónde salen los datos de prueba y de demostración.

El esquema resultante, tabla por tabla, está en [[Database schema]].

## De `schema.sql` a Flyway

Hasta septiembre el esquema vivía en un `schema.sql` con sentencias `IF NOT EXISTS` que corría en cada arranque. Tenía dos problemas: no podía cambiar una tabla que ya tenía datos, y producción había quedado distinta del archivo (por ejemplo, sin la unicidad del correo). El PR #38 lo reemplazó por Flyway:

- **V1** reproduce el esquema tal como estaba en producción. Las bases que ya existían no la ejecutan: `baselineOnMigrate` las marca en la versión 1 y siguen desde V2.
- **V2 a V4** corrigen lo que producción nunca recibió: unicidad del correo, claves foráneas, identidad del álbum sin índice sobre expresión.
- **V5 en adelante** acompañan funcionalidades.

## Reglas para una migración nueva

| Regla | Motivo |
|---|---|
| Nombre `V<n>__descripcion.sql`, con el siguiente número libre y dos guiones bajos | Flyway ordena por versión; `tools/paw_checks.py flyway` verifica nombres y números repetidos |
| Nunca editar una migración ya aplicada | Flyway guarda un checksum; si cambia, la aplicación no arranca. Se corrige con otra migración |
| Compatible con PostgreSQL y HSQLDB | Los tests de persistence corren las mismas migraciones: sin índices sobre expresiones ni bloques `DO` |
| Nunca `DROP TABLE` ni `TRUNCATE` sobre datos de negocio | Las migraciones corren contra la base real |
| Si dos PR toman el mismo número, el segundo renombra la suya | Dos archivos con la misma versión impiden arrancar |

## Las once migraciones

| Versión | Qué hace | Funcionalidad |
|---|---|---|
| V1 | Esquema inicial: users, tokens, artists, images, albums, posts, inquiries | Base |
| V2 | Índice único sobre `users.email` | [[Authentication flow]] |
| V3 | Claves foráneas de posts y albums | Integridad |
| V4 | `albums.normalized_title` y unicidad por columnas | [[Publish flow]] |
| V5 | Datos de cobro, `addresses`, estado `RESERVED`, dirección, comprobante, precio y `CHECK` de estados en inquiries | [[Inquiry and sale flow]], [[Addresses and payment flow]] |
| V6 | `enabled` → `verified`; `created_at` en los tokens de verificación | [[Authentication flow]], [[Tokens and email links]] |
| V7 | `inquiry_messages`; migra el texto inicial y elimina `inquiries.message` | [[Conversation flow]] |
| V8 | `post_images` | [[Gallery flow]] |
| V9 | `users.avatar_image_id` | [[Profile flow]] |
| V10 | `reviews` | [[Reviews flow]] |
| V11 | `cart_items` | [[Cart flow]] |

V7 es la única que **mueve datos**: copia cada `inquiries.message` no nulo a `inquiry_messages` con el comprador como remitente y la fecha original, y después elimina la columna.

### V1

{{file:persistence/src/main/resources/db/migration/V1__esquema_inicial.sql}}

### V2

{{file:persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql}}

### V3

{{file:persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql}}

### V4

{{file:persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql}}

### V5

{{file:persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql}}

### V6

{{file:persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql}}

### V7

{{file:persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql}}

### V8

{{file:persistence/src/main/resources/db/migration/V8__post_gallery.sql}}

### V9

{{file:persistence/src/main/resources/db/migration/V9__user_avatars.sql}}

### V10

{{file:persistence/src/main/resources/db/migration/V10__sale_reviews.sql}}

### V11

{{file:persistence/src/main/resources/db/migration/V11__carrito.sql}}

## Datos de prueba: `populator.sql`

Los tests de persistence levantan una HSQLDB en memoria, aplican las once migraciones y después cargan `persistence/src/test/resources/populator.sql`. Es la **única** fuente de datos de los tests de DAO: la regla del proyecto prohíbe insertar en el Arrange.

Contiene cuentas en cada situación que los tests necesitan (verificada con datos de cobro, administradora, heredada sin clave, sin verificar), direcciones vigentes y archivadas, tokens, artistas, álbumes, imágenes, publicaciones en cada estado, consultas en cada estado con mensajes y comprobante, reseñas e ítems de carrito. Los ids son fijos para que los tests puedan referirse a ellos.

El archivo no se embebe acá: incluye hashes de contraseñas de prueba. Se lee en el repositorio. La configuración que lo carga:

{{file:persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java}}

## Datos de demostración (desarrollo local)

Nada de esto se ejecuta al arrancar ni se empaqueta en el WAR.

| Archivo | Qué es |
|---|---|
| `tools/setup_local_postgres.sh` | Guía interactiva para macOS con Homebrew: levanta PostgreSQL, crea el rol y la base si faltan y verifica la conexión. No crea tablas (lo hace Flyway) ni carga datos |
| `tools/seed_local_data.sh` | Carga el catálogo de demostración: descarga las tapas, valida su hash y ejecuta todo en una única transacción, por `DATABASE_URL` con `psql` o dentro de un contenedor Docker |
| `database/seed_dev_posts.sql` | SQL que usa el script: artistas, álbumes y publicaciones. Define una función temporal que normaliza `search_phrase` igual que [[SearchText]] |
| `database/demo_posts.tsv` | Las 24 publicaciones de demostración: artista, álbum, año, género, precio, estado, zona, descripción, id de MusicBrainz y hash de la tapa |
| `tools/sql/demo-users.sql` | Dos cuentas de demostración (usuario y administrador). Sus credenciales están en el README del repositorio |
| `database/users.sql` | Resto del esqueleto inicial (una tabla `users` de cuatro columnas). No lo usa nadie |

## Preguntas de defensa

**¿Qué pasa si alguien edita una migración ya aplicada?**
Flyway compara el checksum guardado con el del archivo y falla al arrancar. La corrección va en una migración nueva.

**¿Cómo se incorporaron las bases que ya existían?**
Con `baselineOnMigrate`: Flyway crea su tabla de historial, las marca en la versión 1 sin ejecutar V1 y aplica el resto.

**¿De dónde salen los datos de los tests?**
De `populator.sql`, cargado después de las migraciones sobre una HSQLDB en memoria.

**¿Por qué V4 agrega una columna en vez de un índice sobre `LOWER(title)`?**
Porque HSQLDB no admite índices sobre expresiones y las migraciones tienen que correr en los dos motores.
