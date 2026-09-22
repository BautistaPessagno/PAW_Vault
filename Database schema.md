---
title: "Database schema"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["persistence/src/main/resources/schema.sql", "persistence/src/test/resources/schema.sql"]
---

# Database schema

WebConfig executes persistence/src/main/resources/schema.sql at every context startup. It now creates eight tables and applies targeted PostgreSQL upgrades and backfills. No Flyway runner or application seed runs at startup.

| Table | Current values and constraints |
|---|---|
| users | Unique email; username; nullable password_hash; role default USER; enabled default false; preferred_locale default es |
| email_verification_tokens | Unique token; user foreign key; no expiry |
| password_reset_tokens | Unique token; unique user_id (one live link per account); user foreign key; required expires_at |
| artists | Display name; unique normalized_name; required search_phrase with index |
| images | Required content_type and BYTEA |
| albums | Unique (artist_id, LOWER(title), release_year) index; required genre with CHECK of fifteen values; required search_phrase with index; legacy cover_image_id |
| posts | Unique user/album; required positive price and NEW/USED condition (CHECKs); stock default 1; image FK; AVAILABLE/SOLD CHECK; created_at |
| inquiries | Nullable post FK plus album and seller FKs copied on deletion; buyer FK; optional message up to 500; created_at; status default PENDING |

The canonical schema still does not add foreign keys for albums.artist_id, albums.cover_image_id, posts.user_id or posts.album_id. Role, locale and inquiry status have no CHECK. TODO.md states that the schema has no foreign keys by team decision; the file does declare FKs for tokens, post images and inquiries, and the inquiry FK is the reason [[Edit and delete flow]] detaches inquiries before deleting a post.

## Upgrades applied at startup

Since `40328f0` startup also changes existing data, always only where a value is missing or invalid:

- email_verification_tokens: an older token_hash column and its constraint are renamed to token; old hashed links stop validating. An obsolete index is dropped.
- artists: normalized_name is added and backfilled as lowercase alphanumerics. Legacy rows that now normalize identically keep the oldest as canonical; the others get a `__legacy_<id>` suffix instead of being merged or deleted. The old name constraint and index are replaced by a unique index on normalized_name.
- artists.search_phrase and albums.search_phrase are added and backfilled with TRANSLATE over common accented letters, then made NOT NULL and indexed. This SQL approximates [[SearchText]]; rows written by the application use the Java rule.
- albums: legacy null genres become OTHER before NOT NULL and the genre CHECK; the exact unique constraint is replaced by the LOWER(title) unique index. albums.cover_path is no longer dropped; the legacy column is left intact.
- posts: null or nonpositive prices become 60000 and null conditions USED before NOT NULL and the price/condition CHECKs. The code comment calls 60000 the agreed migration value.
- inquiries: post_id becomes nullable, and album_id and seller_id columns with FKs are added.

These are targeted upgrades, not a complete legacy migration framework. Textual albums.artist and old posts.publisher_email layouts are not converted. FK or CHECK installation can still fail on incompatible legacy data. The test schema creates a fresh HSQLDB equivalent and does not execute PostgreSQL ALTER, DO or backfill statements; it enforces exact title uniqueness because HSQLDB cannot express the LOWER(title) index.

## Canonical PostgreSQL source

[persistence/src/main/resources/schema.sql, lines 1–304](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/schema.sql>)

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

-- La primera version de la verificacion guardaba el hash del token (token_hash) y un
-- vencimiento (expires_at). El DAO actual inserta token, y SimpleJdbcInsert arma el
-- INSERT con las columnas reales de la tabla: contra la forma vieja mandaba NULL a
-- token_hash. Se renombra la columna y se conservan las filas; esos enlaces ya no
-- validan (guardan un hash, no el token) y una cuenta pendiente pide otro al registrarse.
DO 'BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = ''email_verification_tokens'' AND column_name = ''token_hash''
    ) THEN
        ALTER TABLE email_verification_tokens RENAME COLUMN token_hash TO token;
        ALTER TABLE email_verification_tokens ALTER COLUMN token TYPE VARCHAR(64);
    END IF;
    IF EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''email_verification_tokens_hash_key''
          AND conrelid = ''email_verification_tokens''::regclass
    ) THEN
        ALTER TABLE email_verification_tokens
            RENAME CONSTRAINT email_verification_tokens_hash_key TO email_verification_tokens_token_key;
    END IF;
END';
-- expires_at puede seguir presente en instalaciones viejas; el DAO actual no la usa.
DROP INDEX IF EXISTS email_verification_tokens_user_id_id_idx;

-- Recuperacion de contrasena: mismo esquema que los tokens de verificacion, mas la
-- fecha de vencimiento. Va en su propia tabla porque el ciclo de vida es distinto:
-- pedir un enlace de recuperacion no puede invalidar una verificacion pendiente.
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    CONSTRAINT password_reset_tokens_token_key UNIQUE (token),
    CONSTRAINT password_reset_tokens_user_id_key UNIQUE (user_id),
    CONSTRAINT password_reset_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

-- La unicidad de user_id es la que sostiene el "un solo enlace vivo por cuenta": dos
-- pedidos simultaneos para el mismo correo borran cero filas cada uno, no se bloquean
-- entre si y sin la restriccion los dos INSERT entrarian. Se repite fuera del CREATE
-- TABLE porque las bases que ya tienen la tabla no reciben la restriccion de arriba.
CREATE UNIQUE INDEX IF NOT EXISTS password_reset_tokens_user_id_key
    ON password_reset_tokens (user_id);

CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL
);

-- La identidad ignora mayusculas y separadores, pero el nombre conserva la forma
-- elegida para mostrarlo. El backfill permite arrancar sobre bases anteriores.
ALTER TABLE artists ADD COLUMN IF NOT EXISTS normalized_name VARCHAR(255);
UPDATE artists
SET normalized_name = REGEXP_REPLACE(LOWER(name), '[^[:alnum:]]', '', 'g')
WHERE normalized_name IS NULL;
-- La restriccion anterior solo comparaba LOWER(name), por lo que instalaciones
-- legacy pueden contener nombres que ahora normalizan igual (por ejemplo,
-- "The Beatles" y "The-Beatles"). Se conserva la fila mas antigua como
-- identidad canonica y se desambiguan las restantes sin borrar ni reasignar
-- ninguna relacion existente.
WITH duplicate_names AS (
    SELECT id, normalized_name,
           ROW_NUMBER() OVER (PARTITION BY normalized_name ORDER BY id) AS duplicate_position
    FROM artists
)
UPDATE artists AS artist
SET normalized_name = LEFT(artist.normalized_name, 230) || '__legacy_' || artist.id
FROM duplicate_names AS duplicate
WHERE artist.id = duplicate.id AND duplicate.duplicate_position > 1;
ALTER TABLE artists DROP CONSTRAINT IF EXISTS artists_name_key;
DROP INDEX IF EXISTS artists_name_lower_key;
CREATE UNIQUE INDEX IF NOT EXISTS artists_normalized_name_key ON artists (normalized_name);
ALTER TABLE artists ALTER COLUMN normalized_name SET NOT NULL;

-- Texto normalizado que usa el ranking de sugerencias: minusculas, sin acentos y
-- con cada corrida de separadores reducida a un espacio. La aplicacion lo escribe
-- con SearchText; este backfill repite la misma regla en SQL para las filas
-- anteriores a la columna.
ALTER TABLE artists ADD COLUMN IF NOT EXISTS search_phrase VARCHAR(255);
UPDATE artists
SET search_phrase = TRIM(REGEXP_REPLACE(
        TRANSLATE(LOWER(name), 'áàäâãéèëêíìïîóòöôõúùüûñç', 'aaaaaeeeeiiiiooooouuuunc'),
        '[^[:alnum:]]+', ' ', 'g'))
WHERE search_phrase IS NULL;
ALTER TABLE artists ALTER COLUMN search_phrase SET NOT NULL;
CREATE INDEX IF NOT EXISTS artists_search_phrase_idx ON artists (search_phrase);

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
    cover_image_id INTEGER
);

-- Bases creadas antes de que existiera la tabla images pueden conservar cover_path.
-- La aplicacion nueva usa cover_image_id y deja intacto ese dato legacy.
ALTER TABLE albums ADD COLUMN IF NOT EXISTS cover_image_id INTEGER;

-- Genero de lista fija (enum Genre). Los albums legacy sin clasificar se conservan
-- bajo OTHER para poder exigir el dato sin inventar un genero concreto.
ALTER TABLE albums ADD COLUMN IF NOT EXISTS genre VARCHAR(30);
UPDATE albums SET genre = 'OTHER' WHERE genre IS NULL;
ALTER TABLE albums ALTER COLUMN genre SET NOT NULL;

-- Misma regla que artists.search_phrase, sobre el titulo del album.
ALTER TABLE albums ADD COLUMN IF NOT EXISTS search_phrase VARCHAR(255);
UPDATE albums
SET search_phrase = TRIM(REGEXP_REPLACE(
        TRANSLATE(LOWER(title), 'áàäâãéèëêíìïîóòöôõúùüûñç', 'aaaaaeeeeiiiiooooouuuunc'),
        '[^[:alnum:]]+', ' ', 'g'))
WHERE search_phrase IS NULL;
ALTER TABLE albums ALTER COLUMN search_phrase SET NOT NULL;
CREATE INDEX IF NOT EXISTS albums_search_phrase_idx ON albums (search_phrase);

DO 'BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''albums_genre_check'' AND conrelid = ''albums''::regclass
    ) THEN
        ALTER TABLE albums ADD CONSTRAINT albums_genre_check
            CHECK (genre IN (''ROCK'', ''POP'', ''JAZZ'', ''BLUES'', ''SOUL_FUNK'', ''HIP_HOP'',
                ''ELECTRONIC'', ''CLASSICAL'', ''TANGO'', ''FOLKLORE'', ''CUMBIA'', ''REGGAE'',
                ''METAL'', ''PUNK'', ''OTHER''));
    END IF;
END';

-- Misma regla que artists: el titulo conserva el case del usuario y la identidad
-- (artista, titulo, anio) se compara en minuscula.
ALTER TABLE albums DROP CONSTRAINT IF EXISTS albums_artist_title_year_key;
CREATE UNIQUE INDEX IF NOT EXISTS albums_artist_title_lower_year_key
    ON albums (artist_id, LOWER(title), release_year);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    description VARCHAR(1000),
    item_condition VARCHAR(20) NOT NULL,
    pressing_year INTEGER,
    zone VARCHAR(100),
    stock INTEGER NOT NULL DEFAULT 1,
    image_id INTEGER,
    status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id),
    CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT posts_price_positive_check CHECK (price > 0),
    CONSTRAINT posts_condition_check CHECK (item_condition IN ('NEW', 'USED')),
    CONSTRAINT posts_status_check CHECK (status IN ('AVAILABLE', 'SOLD'))
);

-- Datos comerciales del post. El precio es obligatorio; cualquier instalacion legacy
-- debe completar sus precios antes de desplegar esta version.
-- La columna es item_condition y no condition porque CONDITION es palabra reservada.
ALTER TABLE posts ADD COLUMN IF NOT EXISTS price INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS description VARCHAR(1000);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS item_condition VARCHAR(20);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS pressing_year INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS zone VARCHAR(100);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 1;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS image_id INTEGER;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE';
-- Los precios inexistentes o no positivos eran validos en versiones anteriores.
-- Se preservan esas publicaciones con el valor de migracion acordado antes de
-- exigir el contrato actual.
UPDATE posts SET price = 60000 WHERE price IS NULL OR price <= 0;
UPDATE posts SET item_condition = 'USED' WHERE item_condition IS NULL;
ALTER TABLE posts ALTER COLUMN price SET NOT NULL;
ALTER TABLE posts ALTER COLUMN item_condition SET NOT NULL;
DO 'BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''posts_price_positive_check'' AND conrelid = ''posts''::regclass
    ) THEN
        ALTER TABLE posts ADD CONSTRAINT posts_price_positive_check CHECK (price > 0);
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''posts_condition_check'' AND conrelid = ''posts''::regclass
    ) THEN
        ALTER TABLE posts ADD CONSTRAINT posts_condition_check
            CHECK (item_condition IN (''NEW'', ''USED''));
    END IF;
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
    post_id INTEGER,
    album_id INTEGER,
    seller_id INTEGER,
    buyer_id INTEGER NOT NULL,
    message VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    CONSTRAINT inquiries_post_fk FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT inquiries_album_fk FOREIGN KEY (album_id) REFERENCES albums(id),
    CONSTRAINT inquiries_seller_fk FOREIGN KEY (seller_id) REFERENCES users(id),
    CONSTRAINT inquiries_buyer_fk FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Estado de la consulta. Las bases anteriores a la venta de ejemplares unicos traen
-- todas sus consultas sin cerrar: el default las deja pendientes.
ALTER TABLE inquiries ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'PENDING';

-- Al eliminar una publicacion sus consultas sobreviven sin post: guardan el album y el
-- vendedor para que la bandeja del comprador siga mostrando que vinilo consulto.
ALTER TABLE inquiries ALTER COLUMN post_id DROP NOT NULL;
ALTER TABLE inquiries ADD COLUMN IF NOT EXISTS album_id INTEGER;
ALTER TABLE inquiries ADD COLUMN IF NOT EXISTS seller_id INTEGER;
DO 'BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''inquiries_album_fk'' AND conrelid = ''inquiries''::regclass
    ) THEN
        ALTER TABLE inquiries ADD CONSTRAINT inquiries_album_fk FOREIGN KEY (album_id) REFERENCES albums(id);
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = ''inquiries_seller_fk'' AND conrelid = ''inquiries''::regclass
    ) THEN
        ALTER TABLE inquiries ADD CONSTRAINT inquiries_seller_fk FOREIGN KEY (seller_id) REFERENCES users(id);
    END IF;
END';
```

## Test schema

[persistence/src/test/resources/schema.sql, lines 1–96](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/schema.sql>)

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

CREATE TABLE password_reset_tokens (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token VARCHAR(64) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    CONSTRAINT password_reset_tokens_token_key UNIQUE (token),
    CONSTRAINT password_reset_tokens_user_id_key UNIQUE (user_id),
    CONSTRAINT password_reset_tokens_user_fk FOREIGN KEY (user_id) REFERENCES users(id)
);

-- La identidad normalizada se persiste igual que en PostgreSQL. La constraint
-- exacta alcanza porque el service ya elimina case, espacios y puntuacion.
CREATE TABLE artists (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    search_phrase VARCHAR(255) NOT NULL,
    CONSTRAINT artists_normalized_name_key UNIQUE (normalized_name)
);

CREATE TABLE images (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    content_type VARCHAR(100) NOT NULL,
    data LONGVARBINARY NOT NULL
);

-- Igual que artists: PostgreSQL exige la unicidad sobre LOWER(title) y HSQLDB no
-- puede, asi que la constraint es exacta y el dedupe insensible a mayusculas se
-- ejercita solo por el LOWER() del DAO.
CREATE TABLE albums (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    genre VARCHAR(30) NOT NULL,
    search_phrase VARCHAR(255) NOT NULL,
    cover_image_id INTEGER,
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year),
    CONSTRAINT albums_genre_check CHECK (genre IN ('ROCK', 'POP', 'JAZZ', 'BLUES', 'SOUL_FUNK',
        'HIP_HOP', 'ELECTRONIC', 'CLASSICAL', 'TANGO', 'FOLKLORE', 'CUMBIA', 'REGGAE', 'METAL',
        'PUNK', 'OTHER'))
);

CREATE TABLE posts (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id),
    CONSTRAINT posts_image_fk FOREIGN KEY (image_id) REFERENCES images(id),
    CONSTRAINT posts_price_positive_check CHECK (price > 0),
    CONSTRAINT posts_condition_check CHECK (item_condition IN ('NEW', 'USED')),
    CONSTRAINT posts_status_check CHECK (status IN ('AVAILABLE', 'SOLD'))
);

CREATE TABLE inquiries (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    post_id INTEGER,
    album_id INTEGER,
    seller_id INTEGER,
    buyer_id INTEGER NOT NULL,
    message VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT inquiries_post_fk FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT inquiries_album_fk FOREIGN KEY (album_id) REFERENCES albums(id),
    CONSTRAINT inquiries_seller_fk FOREIGN KEY (seller_id) REFERENCES users(id),
    CONSTRAINT inquiries_buyer_fk FOREIGN KEY (buyer_id) REFERENCES users(id)
);
```

[[Schema history and seeds]] · [[Transactions and concurrency]]
