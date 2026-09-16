---
title: "Schema history and seeds"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-16"
commit: "40328f0a23ce3814ab62a9f0124a6ba1e6ae71be"
status: "documented"
sources: ["database/users.sql", "database/albums.sql", "database/seed_dev_posts.sql", "persistence/src/test/resources/populator.sql", "tools/sql/demo-users.sql"]
---

# Schema history and seeds

The canonical runtime schema lives in persistence/src/main/resources/schema.sql. The deleted Flyway migrations remain historical Git evidence. Manual bootstrap files are not the current startup schema.

| Path | Role |
|---|---|
| database/users.sql | Old manual user table bootstrap |
| database/albums.sql | One-time catalog/post bootstrap with older foreign keys and year CHECK |
| database/seed_dev_posts.sql | Optional idempotent development catalog/posts, with no images or credentials |
| persistence/src/test/resources/populator.sql | HSQLDB fixtures for users, tokens, catalog, images, commercial/sold posts and inquiry states |
| tools/sql/demo-users.sql | Optional manual enabled USER/ADMIN accounts; outside classpath, never automatic, preserves existing emails |

Startup adds the current auth/commercial/inquiry columns to supported older layouts. Old manual catalog FKs differ from a fresh canonical database. Earlier seeded users lack hashes and remain disabled until claimed through email verification. A new publication of an existing seeded album can now store its own photo; the old album cover is merely a fallback.

The test fixture includes realistic related user rows, dated publications, nullable old details, AVAILABLE/SOLD posts and PENDING/ACCEPTED/REJECTED inquiries. Those fixtures do not exercise PostgreSQL upgrades. Demo credentials are documented in the source README; their values are not copied into this vault. No SQL was run for this refresh.

## database/users.sql

[database/users.sql, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/users.sql>)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT users_email_key UNIQUE (email)
);
```

## database/albums.sql

[database/albums.sql, lines 1–57](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/albums.sql>)

```sql
BEGIN;

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

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
    CONSTRAINT albums_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artists(id),
    CONSTRAINT albums_cover_image_id_fkey FOREIGN KEY (cover_image_id) REFERENCES images(id),
    CONSTRAINT albums_release_year_check CHECK (release_year BETWEEN 1000 AND 9999),
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year)
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT posts_album_id_fkey FOREIGN KEY (album_id) REFERENCES albums(id),
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id)
);

INSERT INTO artists (name)
VALUES ('illya kuryaki and the valderramas');

INSERT INTO albums (title, artist_id, release_year)
SELECT 'versus', id, 1997
FROM artists
WHERE name = 'illya kuryaki and the valderramas';

INSERT INTO users (username, email)
VALUES ('bpessagno', 'bpessagno@itba.edu.ar')
ON CONFLICT (email) DO NOTHING;

INSERT INTO posts (user_id, album_id)
SELECT publisher.id, album.id
FROM albums AS album
JOIN artists AS artist ON artist.id = album.artist_id
JOIN users AS publisher ON publisher.email = 'bpessagno@itba.edu.ar'
WHERE album.title = 'versus'
  AND artist.name = 'illya kuryaki and the valderramas'
  AND album.release_year = 1997;

COMMIT;
```

## database/seed_dev_posts.sql

[database/seed_dev_posts.sql, lines 1–49](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/seed_dev_posts.sql>)

```sql
-- Datos de desarrollo: cuatro álbumes publicados, para probar el listado y el
-- flujo de contacto ("Me interesa comprarlo") sin cargarlos a mano por el form.
--
-- El usuario de desarrollo es bpessagno (bpessagno@itba.edu.ar).
--
-- Es idempotente: correrlo dos veces no duplica nada.
--
-- Títulos y nombres van en minúscula a propósito: AlbumServiceImpl y
-- ArtistServiceImpl normalizan con trim().toLowerCase() y buscan por igualdad
-- exacta, así que sembrar con mayúsculas crea identidades duplicadas cuando el
-- mismo álbum se publica después desde /publish.
--
-- Los álbumes sembrados no tienen portada (cover_image_id NULL) y la landing los
-- muestra con el placeholder. Para probar portadas reales, publicá desde /publish
-- adjuntando una imagen.

BEGIN;

INSERT INTO users (username, email)
VALUES ('bpessagno', 'bpessagno@itba.edu.ar')
ON CONFLICT (email) DO NOTHING;

INSERT INTO artists (name) VALUES
  ('charly garcia'),
  ('soda stereo'),
  ('spinetta jade'),
  ('sumo')
ON CONFLICT (name) DO NOTHING;

INSERT INTO albums (title, artist_id, release_year)
SELECT seed.title, artist.id, seed.release_year
FROM (VALUES
  ('clics modernos',              'charly garcia', 1983),
  ('cancion animal',              'soda stereo',   1990),
  ('alma de diamante',            'spinetta jade', 1980),
  ('divididos por la felicidad',  'sumo',          1985)
) AS seed(title, artist_name, release_year)
JOIN artists AS artist ON artist.name = seed.artist_name
ON CONFLICT (artist_id, title, release_year) DO NOTHING;

INSERT INTO posts (user_id, album_id)
SELECT publisher.id, album.id
FROM albums AS album
JOIN artists AS artist ON artist.id = album.artist_id
JOIN users AS publisher ON publisher.email = 'bpessagno@itba.edu.ar'
WHERE artist.name IN ('charly garcia', 'soda stereo', 'spinetta jade', 'sumo')
ON CONFLICT (user_id, album_id) DO NOTHING;

COMMIT;
```

## persistence/src/test/resources/populator.sql

[persistence/src/test/resources/populator.sql, lines 1–64](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/populator.sql>)

```sql
INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (1, 'bpessagno', 'bpessagno@itba.edu.ar', '$2a$12$FpiCwPCeBQTF3ihFUejq2Oz4HO.SYw2n4z1fgYoZ3bpZI67EDcIFm', 'USER', TRUE, 'es');

INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (2, 'tgorganchian', 'tgorganchian@itba.edu.ar', '$2a$12$InUBNvxsWcA9mXYXqKOoAuysB1rA4gF.dteOO/IUP6YvMKzYvtvru', 'ADMIN', TRUE, 'fr');

INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (3, 'legacy', 'legacy@example.com', NULL, 'USER', FALSE, 'en');

INSERT INTO email_verification_tokens (id, user_id, token)
VALUES (1, 3, 'pending-user-verification-token');

INSERT INTO artists (id, name)
VALUES (1, 'illya kuryaki and the valderramas');

INSERT INTO artists (id, name)
VALUES (2, 'soda stereo');

INSERT INTO images (id, content_type, data)
VALUES (1, 'image/png', X'89504E470D0A1A0A');

INSERT INTO albums (id, title, artist_id, release_year, genre, cover_image_id)
VALUES (1, 'versus', 1, 1997, 'HIP_HOP', 1);

INSERT INTO albums (id, title, artist_id, release_year, genre, cover_image_id)
VALUES (2, 'cancion animal', 2, 1990, 'ROCK', NULL);

-- created_at no sigue el orden de los ids a proposito: asi los tests de orden
-- distinguen "mas nuevo" (fecha) de "id mas alto".
-- Post anterior a las columnas comerciales: todo NULL y stock por default.
INSERT INTO posts (id, user_id, album_id, created_at)
VALUES (1, 1, 1, '2026-02-15 10:00:00');

-- Post con todos los datos comerciales cargados.
INSERT INTO posts (id, user_id, album_id, price, description, item_condition, pressing_year, zone, stock, created_at)
VALUES (2, 2, 1, 45000, 'Prensado japones, tapa con leve desgaste.', 'USED', 2015, 'Palermo', 2, '2026-01-01 10:00:00');

-- Post de otro album y otro artista, el mas reciente y el mas barato.
INSERT INTO posts (id, user_id, album_id, price, created_at)
VALUES (3, 1, 2, 30000, '2026-03-01 10:00:00');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (1, 2, 1, '¿Aceptarías una oferta?', '2026-03-02 10:00:00', 'PENDING');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (2, 2, 3, NULL, '2026-03-03 10:00:00', 'PENDING');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (3, 3, 2, 'Me interesa.', '2026-03-04 10:00:00', 'PENDING');

-- Segunda consulta del mismo comprador, sobre otra publicacion y mas reciente: es la
-- que distingue "mas nueva primero" de "unico resultado".
INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (4, 1, 2, NULL, '2026-03-05 10:00:00', 'PENDING');

-- Ejemplar ya vendido, con la consulta que lo cerro y la competidora que quedo rechazada.
INSERT INTO posts (id, user_id, album_id, price, status, created_at)
VALUES (4, 3, 2, 20000, 'SOLD', '2026-01-15 10:00:00');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (5, 4, 1, 'Me lo llevo.', '2026-03-06 10:00:00', 'ACCEPTED');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (6, 4, 2, NULL, '2026-03-07 10:00:00', 'REJECTED');
```

[Optional demo seed](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/sql/demo-users.sql>)

[[Database schema]] · [[Authentication flow]] · [[Testing and evidence]]
