---
title: "Database schema"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["persistence/src/main/resources/schema.sql", "persistence/src/test/resources/schema.sql"]
---

# Database schema

WebConfig executes persistence/src/main/resources/schema.sql at every context startup. It creates seven tables and applies targeted PostgreSQL upgrades. No Flyway runner or application seed runs at startup.

| Table | Current values and constraints |
|---|---|
| users | Unique email; username; nullable password_hash; role default USER; enabled default false; preferred_locale default es |
| email_verification_tokens | Unique token; user foreign key; no expiry |
| artists | Unique name |
| images | Required content_type and BYTEA |
| albums | Unique artist/title/year; optional genre and legacy cover_image_id |
| posts | Unique user/album; nullable historical commercial details; stock default 1; image FK; AVAILABLE/SOLD CHECK; created_at |
| inquiries | Post and buyer FKs; optional message up to 500; created_at; status default PENDING |

The canonical schema does not add foreign keys for albums.artist_id, albums.cover_image_id, posts.user_id or posts.album_id. It has no SQL price/year/condition/genre/role/locale or inquiry-status CHECK. Model enums and form validation do not enforce those invariants on arbitrary SQL writers. The older manual bootstrap has different constraints.

Startup adds/backfills username and authentication fields. Existing null enabled values become true only when a hash exists; existing false values remain false. It preserves historical album covers, adds genre and commercial post columns, supplies stock=1 and AVAILABLE defaults, and timestamps older posts at the startup that first adds created_at. It installs the post image FK/status CHECK if absent and adds inquiry status. It also still drops the obsolete albums.cover_path column.

These are targeted upgrades, not a complete legacy migration framework. Textual albums.artist and old posts.publisher_email layouts are not converted here. FK installation can fail on incompatible legacy data. The test schema creates a fresh HSQLDB equivalent and does not execute PostgreSQL ALTER/DO/backfill statements.

## Canonical PostgreSQL source

[persistence/src/main/resources/schema.sql, lines 1–148](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/schema.sql>)

```sql
-- Esquema de quieroVinilos para PostgreSQL.
--
-- Lo ejecuta el DataSourceInitializer de WebConfig en CADA arranque del contexto,
-- por eso toda sentencia tiene que ser idempotente. Es lo que permite cumplir la
-- condicion del enunciado: desplegado contra una base PostgreSQL vacia con
-- permisos adecuados, la aplicacion genera sola todas las tablas que necesita.
--
-- El orden sigue las dependencias del dominio: users, artists e images antes que albums y posts.
--
-- Espejo funcional de persistence/src/test/resources/schema.sql, que declara lo
-- mismo en dialecto HSQLDB para los tests. Si cambia uno, tiene que cambiar el otro.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'USER',
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    preferred_locale VARCHAR(5) NOT NULL DEFAULT 'es',
    CONSTRAINT users_email_key UNIQUE (email)
);

-- Bases creadas antes de que existiera username no traen la columna. Se agrega
-- nullable, se rellena con la parte local del email y recien ahi se vuelve NOT NULL.
ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(100);
UPDATE users SET username = split_part(email, '@', 1) WHERE username IS NULL;
ALTER TABLE users ALTER COLUMN username SET NOT NULL;

-- Las cuentas creadas antes de la autenticacion se conservan. Al no tener un hash
-- no pueden iniciar sesion hasta completar el reclamo enviado a su correo existente.
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(100);
-- La columna nace con el rol por defecto ya aplicado, asi que no hace falta rellenarla:
-- ninguna base anterior a la autenticacion la tiene.
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'USER';
ALTER TABLE users ADD COLUMN IF NOT EXISTS enabled BOOLEAN;
-- El backfill toca solamente filas sin valor. Asi conserva cualquier bloqueo futuro
-- y activa las cuentas que ya tenian un hash antes de incorporar la verificacion.
UPDATE users SET enabled = (password_hash IS NOT NULL) WHERE enabled IS NULL;
ALTER TABLE users ALTER COLUMN enabled SET DEFAULT FALSE;
ALTER TABLE users ALTER COLUMN enabled SET NOT NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferred_locale VARCHAR(5) NOT NULL DEFAULT 'es';

-- El token es el valor aleatorio que viaja en el enlace del correo. Es unico porque
-- findByToken tiene que identificar una sola cuenta con el.
CREATE TABLE IF NOT EXISTS email_verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    CONSTRAINT email_verification_tokens_token_key UNIQUE (token),
    CONSTRAINT email_verification_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(100) NOT NULL,
    data BYTEA NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    cover_image_id INTEGER,
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year)
);

-- Bases creadas antes de que existiera la tabla images traen cover_path (la portada
-- fija compartida). Se reemplaza por cover_image_id; los albums viejos quedan en NULL y
-- se muestran con el placeholder.
ALTER TABLE albums ADD COLUMN IF NOT EXISTS cover_image_id INTEGER;
ALTER TABLE albums DROP COLUMN IF EXISTS cover_path;

-- Genero de lista fija (enum Genre). Lo fija quien incorpora el album al catalogo;
-- los albums anteriores quedan en NULL y la card no lo muestra.
ALTER TABLE albums ADD COLUMN IF NOT EXISTS genre VARCHAR(30);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    price INTEGER,
    description VARCHAR(1000),
    item_condition VARCHAR(20),
    pressing_year INTEGER,
    zone VARCHAR(100),
    stock INTEGER NOT NULL DEFAULT 1,
    image_id INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id),
    CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT posts_status_check CHECK (status IN ('AVAILABLE', 'SOLD'))
);

-- Datos comerciales del post. Los posts anteriores quedan con NULL (y stock 1) y la
-- card oculta lo que no tenga valor. price es nullable solo por eso: el form lo exige.
-- La columna es item_condition y no condition porque CONDITION es palabra reservada.
ALTER TABLE posts ADD COLUMN IF NOT EXISTS price INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS description VARCHAR(1000);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS item_condition VARCHAR(20);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS pressing_year INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS zone VARCHAR(100);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 1;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS image_id INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE';
DO 'BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''posts_image_fk'' AND conrelid = ''posts''::regclass
    ) THEN
        ALTER TABLE posts ADD CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id);
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''posts_status_check'' AND conrelid = ''posts''::regclass
    ) THEN
        ALTER TABLE posts ADD CONSTRAINT posts_status_check
            CHECK (status IN (''AVAILABLE'', ''SOLD''));
    END IF;
END';

-- Fecha de publicacion, para ordenar el listado. Los posts anteriores a la columna
-- quedan todos con la fecha del arranque que la agrego y se desempatan por id.
ALTER TABLE posts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW();

-- Consultas de compra: quedan registradas antes de avisarle por mail al publicante.
CREATE TABLE IF NOT EXISTS inquiries (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    message VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    CONSTRAINT inquiries_post_fk FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT inquiries_buyer_fk FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Estado de la consulta. Las bases anteriores a la venta de ejemplares unicos traen
-- todas sus consultas sin cerrar: el default las deja pendientes.
ALTER TABLE inquiries ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'PENDING';
```

## Test schema

[persistence/src/test/resources/schema.sql, lines 1–69](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/schema.sql>)

```sql
CREATE TABLE users (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(100),
    role VARCHAR(20) DEFAULT 'USER' NOT NULL,
    enabled BOOLEAN DEFAULT FALSE NOT NULL,
    preferred_locale VARCHAR(5) DEFAULT 'es' NOT NULL,
    CONSTRAINT users_email_key UNIQUE (email)
);

CREATE TABLE email_verification_tokens (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    CONSTRAINT email_verification_tokens_token_key UNIQUE (token),
    CONSTRAINT email_verification_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE artists (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

CREATE TABLE images (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    content_type VARCHAR(100) NOT NULL,
    data LONGVARBINARY NOT NULL
);

CREATE TABLE albums (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    genre VARCHAR(30),
    cover_image_id INTEGER,
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year)
);

CREATE TABLE posts (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    price INTEGER,
    description VARCHAR(1000),
    item_condition VARCHAR(20),
    pressing_year INTEGER,
    zone VARCHAR(100),
    stock INTEGER DEFAULT 1 NOT NULL,
    image_id INTEGER,
    status VARCHAR(20) DEFAULT 'AVAILABLE' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id),
    CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT posts_status_check CHECK (status IN ('AVAILABLE', 'SOLD'))
);

CREATE TABLE inquiries (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    post_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    message VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT inquiries_post_fk FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT inquiries_buyer_fk FOREIGN KEY (buyer_id) REFERENCES users(id)
);
```

[[Schema history and seeds]] · [[Transactions and concurrency]]
