---
title: "Schema history and seeds"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["database/users.sql", "database/albums.sql", "database/seed_dev_posts.sql", "persistence/src/test/resources/populator.sql"]
---

# Schema history and seeds

The canonical runtime schema is [[Database schema]]. The old V1/V2/V3 SQL files under persistence/src/main/resources/db/migration are deleted at ff96f27; no Flyway directory or dependency remains. Their prior contents are historical Git evidence, not scripts available for execution in this checkout.

## Current SQL paths

| Path | Purpose and limits |
|---|---|
| persistence/src/main/resources/schema.sql | Startup create/targeted upgrade; no seed rows or foreign keys |
| database/users.sql | Manual user bootstrap, required before database/albums.sql |
| database/albums.sql | One-time manual tables and initial artist/album/post, with foreign keys and year CHECK |
| database/seed_dev_posts.sql | Optional idempotent four-album development seed; normalized identities and no cover bytes |
| persistence/src/test/resources/schema.sql | Fresh HSQLDB schema without PostgreSQL upgrade statements |
| persistence/src/test/resources/populator.sql | User, artist, binary image, album and Post fixtures |

The seed albums have null cover_image_id and use the placeholder. Publishing an existing seeded identity does not replace its absent cover; a new catalog identity is needed to exercise cover creation through the current form. database/albums.sql uses plain CREATE and is not the idempotent startup script.

The local setup helper no longer runs an artist migration. It stops on the unsupported textual artist schema and does not establish readiness of every Post/Image column on an existing database. No SQL in this note was executed for this refresh.

## Manual album/bootstrap SQL

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

## Development seed

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

## Test fixture

[persistence/src/test/resources/populator.sql, lines 1–14](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/populator.sql>)

```sql
INSERT INTO users (id, username, email)
VALUES (1, 'bpessagno', 'bpessagno@itba.edu.ar');

INSERT INTO artists (id, name)
VALUES (1, 'illya kuryaki and the valderramas');

INSERT INTO images (id, content_type, data)
VALUES (1, 'image/png', X'89504E470D0A1A0A');

INSERT INTO albums (id, title, artist_id, release_year, cover_image_id)
VALUES (1, 'versus', 1, 1997, 1);

INSERT INTO posts (id, user_id, album_id)
VALUES (1, 1, 1);
```

[[Development tools]] · [[Known gaps and document drift]]
