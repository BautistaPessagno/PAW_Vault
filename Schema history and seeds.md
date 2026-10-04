---
title: "Schema history and seeds"
categories: ["Persistence", "History"]
type: "guide"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/resources/populator.sql", "persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java", "database/seed_dev_posts.sql", "database/demo_posts.tsv", "tools/seed_local_data.sh", "tools/sql/demo-users.sql", "tools/setup_local_postgres.sh", "persistence/src/main/resources/db/migration/V1__esquema_inicial.sql", "persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql", "persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql", "persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql", "persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql", "persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql", "persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql", "persistence/src/main/resources/db/migration/V8__post_gallery.sql", "persistence/src/main/resources/db/migration/V9__user_avatars.sql", "persistence/src/main/resources/db/migration/V10__sale_reviews.sql", "persistence/src/main/resources/db/migration/V11__carrito.sql", "database/users.sql"]
---

# Schema history and seeds

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

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V1__esquema_inicial.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__esquema_inicial.sql>), líneas 1–105.

```sql
-- Esquema de quieroVinilos tal como estaba en produccion al pasar a Flyway.
--
-- Las bases que ya existian (produccion y las locales) no ejecutan este archivo:
-- Flyway las marca en esta version con el baseline de WebConfig. Solo corre sobre
-- una base vacia y sobre la HSQLDB de los tests de persistence.
--
-- Se omite un unico objeto de produccion, el indice unico sobre LOWER(title) de
-- albums: HSQLDB no admite indices sobre expresiones. Lo reemplaza la migracion
-- V4 con una columna normalizada.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(100),
    role VARCHAR(20) DEFAULT 'USER' NOT NULL,
    enabled BOOLEAN DEFAULT FALSE NOT NULL,
    preferred_locale VARCHAR(5) DEFAULT 'es' NOT NULL
);

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

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    search_phrase VARCHAR(255) NOT NULL
);

CREATE UNIQUE INDEX artists_normalized_name_key ON artists (normalized_name);
CREATE INDEX artists_search_phrase_idx ON artists (search_phrase);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(100) NOT NULL,
    data BYTEA NOT NULL
);

CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    cover_image_id INTEGER,
    genre VARCHAR(30) NOT NULL,
    search_phrase VARCHAR(255) NOT NULL,
    CONSTRAINT albums_genre_check CHECK (genre IN ('ROCK', 'POP', 'JAZZ', 'BLUES', 'SOUL_FUNK',
        'HIP_HOP', 'ELECTRONIC', 'CLASSICAL', 'TANGO', 'FOLKLORE', 'CUMBIA', 'REGGAE', 'METAL',
        'PUNK', 'OTHER'))
);

CREATE INDEX albums_search_phrase_idx ON albums (search_phrase);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    description VARCHAR(1000),
    item_condition VARCHAR(20) NOT NULL,
    pressing_year INTEGER,
    zone VARCHAR(100),
    stock INTEGER DEFAULT 1 NOT NULL,
    image_id INTEGER,
    status VARCHAR(20) DEFAULT 'AVAILABLE' NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id),
    CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT posts_price_positive_check CHECK (price > 0),
    CONSTRAINT posts_condition_check CHECK (item_condition IN ('NEW', 'USED')),
    CONSTRAINT posts_status_check CHECK (status IN ('AVAILABLE', 'SOLD'))
);

-- Al eliminar una publicacion sus consultas sobreviven sin post: guardan el album y el
-- vendedor para que la bandeja del comprador siga mostrando que vinilo consulto.
CREATE TABLE inquiries (
    id SERIAL PRIMARY KEY,
    post_id INTEGER,
    album_id INTEGER,
    seller_id INTEGER,
    buyer_id INTEGER NOT NULL,
    message VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT inquiries_post_fk FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT inquiries_album_fk FOREIGN KEY (album_id) REFERENCES albums(id),
    CONSTRAINT inquiries_seller_fk FOREIGN KEY (seller_id) REFERENCES users(id),
    CONSTRAINT inquiries_buyer_fk FOREIGN KEY (buyer_id) REFERENCES users(id)
);
```

### V2

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V2__email_unico_en_users.sql>), líneas 1–4.

```sql
-- El login y el registro identifican la cuenta por email. En produccion la tabla users
-- se creo antes de que schema.sql declarara esta unicidad, asi que nunca la recibio.
-- IF NOT EXISTS porque las bases locales si la tienen, como constraint con este nombre.
CREATE UNIQUE INDEX IF NOT EXISTS users_email_key ON users (email);
```

### V3

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V3__fks_de_posts_y_albums.sql>), líneas 1–6.

```sql
-- Referencias que el esquema nunca declaro. Antes de agregarlas se verifico que ni
-- produccion ni las bases locales tuvieran filas huerfanas.
ALTER TABLE posts ADD CONSTRAINT posts_user_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE posts ADD CONSTRAINT posts_album_fk FOREIGN KEY (album_id) REFERENCES albums(id);
ALTER TABLE albums ADD CONSTRAINT albums_artist_fk FOREIGN KEY (artist_id) REFERENCES artists(id);
ALTER TABLE albums ADD CONSTRAINT albums_cover_image_fk FOREIGN KEY (cover_image_id) REFERENCES images(id);
```

### V4

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V4__titulo_normalizado_en_albums.sql>), líneas 1–12.

```sql
-- La identidad de un album es (artista, titulo, anio) sin distinguir mayusculas. Produccion
-- la sostenia con un indice unico sobre LOWER(title), que HSQLDB no admite. Se persiste
-- el titulo en minuscula, igual que artists.normalized_name, y la unicidad pasa a ser
-- sobre columnas. El backfill usa la misma regla que el indice viejo, asi que ninguna
-- fila existente puede chocar.
ALTER TABLE albums ADD COLUMN normalized_title VARCHAR(255);
UPDATE albums SET normalized_title = LOWER(title);
ALTER TABLE albums ALTER COLUMN normalized_title SET NOT NULL;

DROP INDEX IF EXISTS albums_artist_title_lower_year_key;
ALTER TABLE albums ADD CONSTRAINT albums_artist_normalized_title_year_key
    UNIQUE (artist_id, normalized_title, release_year);
```

### V5

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V5__venta_con_comprobante.sql>), líneas 1–50.

```sql
-- Venta con comprobante de pago: datos de cobro, libreta de direcciones, reserva del post
-- y comprobante en la consulta. Traduce lo que main agrego a schema.sql antes de pasar a
-- Flyway. Las consultas anteriores quedan con las columnas nuevas en NULL.

-- Datos de cobro: quien compra los ve para transferir. Opcionales hasta que la cuenta
-- quiera aceptar una consulta.
ALTER TABLE users ADD COLUMN cbu VARCHAR(22);
ALTER TABLE users ADD COLUMN alias VARCHAR(20);

-- Una direccion no se edita ni se borra: se archiva, porque una consulta puede seguir
-- apuntandola.
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    street VARCHAR(100) NOT NULL,
    street_number VARCHAR(10) NOT NULL,
    apartment VARCHAR(20),
    city VARCHAR(100) NOT NULL,
    province VARCHAR(30) NOT NULL,
    postal_code VARCHAR(10) NOT NULL,
    notes VARCHAR(200),
    archived BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT addresses_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX addresses_user_id_idx ON addresses (user_id);

-- Un post reservado espera la transferencia de una consulta.
ALTER TABLE posts DROP CONSTRAINT posts_status_check;
ALTER TABLE posts ADD CONSTRAINT posts_status_check
    CHECK (status IN ('AVAILABLE', 'RESERVED', 'SOLD'));

-- Direccion de envio que eligio el comprador.
ALTER TABLE inquiries ADD COLUMN address_id INTEGER;
ALTER TABLE inquiries ADD CONSTRAINT inquiries_address_fk
    FOREIGN KEY (address_id) REFERENCES addresses(id);

-- Comprobante de la transferencia: uno por consulta, se reemplaza entero al subir otro.
ALTER TABLE inquiries ADD COLUMN receipt_content_type VARCHAR(100);
ALTER TABLE inquiries ADD COLUMN receipt_data BYTEA;
ALTER TABLE inquiries ADD COLUMN receipt_uploaded_at TIMESTAMP;

-- Precio publicado al momento de consultar: es el monto a transferir aunque despues el
-- vendedor edite el post. Las consultas anteriores usan el del post.
ALTER TABLE inquiries ADD COLUMN price INTEGER;

-- Un estado fuera del enum romperia InquiryStatus.valueOf al leer la consulta.
ALTER TABLE inquiries ADD CONSTRAINT inquiries_status_check
    CHECK (status IN ('PENDING', 'AWAITING_PAYMENT', 'PAYMENT_SUBMITTED', 'ACCEPTED',
        'REJECTED', 'CANCELLED'));
```

### V6

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V6__cuenta_verificada.sql>), líneas 1–9.

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

### V7

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V7__mensajes_de_consulta.sql>), líneas 1–18.

```sql
-- Cada Consulta tiene su Conversacion. El texto con el que se creaba la Consulta pasa a ser
-- su primer Mensaje, con la misma fecha, y la columna deja de existir.
CREATE TABLE inquiry_messages (
    id SERIAL PRIMARY KEY,
    inquiry_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    body VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT inquiry_messages_inquiry_fk FOREIGN KEY (inquiry_id) REFERENCES inquiries(id),
    CONSTRAINT inquiry_messages_sender_fk FOREIGN KEY (sender_id) REFERENCES users(id)
);
CREATE INDEX inquiry_messages_inquiry_id_idx ON inquiry_messages (inquiry_id);

-- inquiries.message ya se guardaba recortado y en NULL si quedaba vacio.
INSERT INTO inquiry_messages (inquiry_id, sender_id, body, created_at)
SELECT id, buyer_id, message, created_at FROM inquiries WHERE message IS NOT NULL;

ALTER TABLE inquiries DROP COLUMN message;
```

### V8

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V8__post_gallery.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V8__post_gallery.sql>), líneas 1–13.

```sql
-- posts.image_id remains the primary photo; album.cover_image_id remains the fallback.
-- Only the additional photos live here, in their displayed order.
CREATE TABLE post_images (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    display_order INTEGER NOT NULL,
    CONSTRAINT post_images_post_fk FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    CONSTRAINT post_images_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT post_images_post_order_key UNIQUE (post_id, display_order),
    CONSTRAINT post_images_image_id_key UNIQUE (image_id),
    CONSTRAINT post_images_order_check CHECK (display_order BETWEEN 1 AND 4)
);
```

### V9

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V9__user_avatars.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V9__user_avatars.sql>), líneas 1–3.

```sql
ALTER TABLE users ADD COLUMN avatar_image_id INTEGER;
ALTER TABLE users ADD CONSTRAINT users_avatar_image_fk
    FOREIGN KEY (avatar_image_id) REFERENCES images(id);
```

### V10

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V10__sale_reviews.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V10__sale_reviews.sql>), líneas 1–17.

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    inquiry_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    body VARCHAR(500),
    active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT reviews_inquiry_fk FOREIGN KEY (inquiry_id) REFERENCES inquiries(id),
    CONSTRAINT reviews_author_fk FOREIGN KEY (author_id) REFERENCES users(id),
    CONSTRAINT reviews_subject_fk FOREIGN KEY (subject_id) REFERENCES users(id),
    CONSTRAINT reviews_once_per_party_key UNIQUE (inquiry_id, author_id),
    CONSTRAINT reviews_rating_check CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT reviews_not_self_check CHECK (author_id <> subject_id)
);
CREATE INDEX reviews_subject_active_idx ON reviews (subject_id, active, created_at);
```

### V11

Fuente exacta en `8929aea`: [persistence/src/main/resources/db/migration/V11__carrito.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/resources/db/migration/V11__carrito.sql>), líneas 1–12.

```sql
-- El carrito de cada Cuenta: los Posts que eligio para consultar juntos. La clave compuesta
-- impide repetir un Post. Un item es descartable: si se elimina la publicacion, se va con ella.
CREATE TABLE cart_items (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT cart_items_pkey PRIMARY KEY (user_id, post_id),
    CONSTRAINT cart_items_user_fk FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT cart_items_post_fk FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE INDEX cart_items_post_id_idx ON cart_items (post_id);
```

## Datos de prueba: `populator.sql`

Los tests de persistence levantan una HSQLDB en memoria, aplican las once migraciones y después cargan `persistence/src/test/resources/populator.sql`. Es la **única** fuente de datos de los tests de DAO: la regla del proyecto prohíbe insertar en el Arrange.

Contiene cuentas en cada situación que los tests necesitan (verificada con datos de cobro, administradora, heredada sin clave, sin verificar), direcciones vigentes y archivadas, tokens, artistas, álbumes, imágenes, publicaciones en cada estado, consultas en cada estado con mensajes y comprobante, reseñas e ítems de carrito. Los ids son fijos para que los tests puedan referirse a ellos.

El archivo no se embebe acá: incluye hashes de contraseñas de prueba. Se lee en el repositorio. La configuración que lo carga:

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>), líneas 1–59.

```java
package ar.edu.itba.paw.persistence;

import org.flywaydb.core.Flyway;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.DependsOn;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.jdbc.datasource.init.DataSourceInitializer;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import javax.sql.DataSource;

@Configuration
@EnableTransactionManagement
@ComponentScan({ "ar.edu.itba.paw.persistence" })
public class TestConfiguration {

    @Bean
    public DataSource dataSource() {
        final SimpleDriverDataSource dataSource = new SimpleDriverDataSource();
        dataSource.setDriverClass(org.hsqldb.jdbc.JDBCDriver.class);
        dataSource.setUrl("jdbc:hsqldb:mem:paw;sql.syntax_pgs=true");
        dataSource.setUsername("sa");
        dataSource.setPassword("");
        return dataSource;
    }

    // Las mismas migraciones que corre WebConfig en produccion, sobre la base vacia.
    @Bean(initMethod = "migrate")
    public Flyway flyway(final DataSource dataSource) {
        return Flyway.configure()
                .dataSource(dataSource)
                .locations("classpath:db/migration")
                .load();
    }

    // Los fixtures se cargan recien con el esquema migrado.
    @Bean
    @DependsOn("flyway")
    public DataSourceInitializer dataSourceInitializer(final DataSource dataSource) {
        final ResourceDatabasePopulator populator = new ResourceDatabasePopulator();
        populator.addScript(new ClassPathResource("populator.sql"));

        final DataSourceInitializer initializer = new DataSourceInitializer();
        initializer.setDataSource(dataSource);
        initializer.setDatabasePopulator(populator);
        return initializer;
    }

    @Bean
    public PlatformTransactionManager transactionManager(final DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
}
```

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

## Archivos para seguir el flujo

- [persistence/src/test/resources/populator.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/resources/populator.sql>)
- [persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>) · [[TestConfiguration]]
- [database/seed_dev_posts.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/seed_dev_posts.sql>)
- [database/demo_posts.tsv](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/database/demo_posts.tsv>)
- [tools/seed_local_data.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/seed_local_data.sh>)
- [tools/sql/demo-users.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/sql/demo-users.sql>)
- [tools/setup_local_postgres.sh](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/tools/setup_local_postgres.sh>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
