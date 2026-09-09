---
title: "Schema history and seeds"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/resources/db/migration/V1__convert_artist_to_entity.sql", "persistence/src/main/resources/db/migration/V2__create_posts.sql", "persistence/src/main/resources/db/migration/V3__seed_initial_post.sql", "database/users.sql", "database/albums.sql", "database/seed_dev_posts.sql", "persistence/src/test/resources/schema.sql", "persistence/src/test/resources/populator.sql"]
---

# Schema history and seeds

There is no Flyway dependency or configured migration runner. [[WebConfig]] loads only `schema.sql`. Files named V1/V2/V3 exist as historical/manual resources; their names alone do not make them execute.

Treat these as different initialization histories. Running every SQL file in filename order would not produce a supported current schema. The manual local setup wizard runs V1 only for a detected legacy artist-text schema and does not complete a publisher_email-to-user_id Post migration.

## V1__convert_artist_to_entity.sql

Historical conversion of textual albums.artist to normalized artists and artist_id. It previews collisions, aborts on duplicate normalized identities, populates artists, adds foreign key/year-check/unique constraints, and drops the text column. It targets the old table shape and is not a fresh-schema initializer.

[persistence/src/main/resources/db/migration/V1__convert_artist_to_entity.sql, lines 1–80](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V1__convert_artist_to_entity.sql>)

```sql
BEGIN;

SELECT LOWER(TRIM(artist)) AS normalized_artist_name,
       LOWER(TRIM(title)) AS normalized_album_title,
       release_year AS album_release_year,
       COUNT(*) AS album_count,
       ARRAY_AGG(id ORDER BY id) AS album_ids
FROM albums
GROUP BY LOWER(TRIM(artist)), LOWER(TRIM(title)), release_year
HAVING COUNT(*) > 1
ORDER BY normalized_artist_name, normalized_album_title, album_release_year;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM (
            SELECT LOWER(TRIM(artist)) AS normalized_artist_name,
                   LOWER(TRIM(title)) AS normalized_album_title,
                   release_year AS album_release_year
            FROM albums
            GROUP BY LOWER(TRIM(artist)), LOWER(TRIM(title)), release_year
            HAVING COUNT(*) > 1
        ) AS normalized_collisions
    ) THEN
        RAISE EXCEPTION 'Normalized album identities collide; migration aborted';
    END IF;
END
$$;

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO artists (name)
SELECT DISTINCT LOWER(TRIM(artist)) AS normalized_artist_name
FROM albums;

ALTER TABLE albums ADD COLUMN artist_id INTEGER;

UPDATE albums AS album
SET artist_id = artist.id
FROM artists AS artist
WHERE artist.name = LOWER(TRIM(album.artist));

UPDATE albums
SET title = LOWER(TRIM(title));

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM albums
        WHERE artist_id IS NULL
    ) THEN
        RAISE EXCEPTION 'Some albums could not be linked to an artist; migration aborted';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM albums
        GROUP BY artist_id, title, release_year
        HAVING COUNT(*) > 1
    ) THEN
        RAISE EXCEPTION 'Duplicate album identities remain; migration aborted';
    END IF;
END
$$;

ALTER TABLE albums ALTER COLUMN artist_id SET NOT NULL;
ALTER TABLE albums
    ADD CONSTRAINT albums_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artists(id);
ALTER TABLE albums
    ADD CONSTRAINT albums_release_year_check CHECK (release_year BETWEEN 1000 AND 9999);
ALTER TABLE albums
    ADD CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year);
ALTER TABLE albums DROP COLUMN artist;

COMMIT;
```

## V2__create_posts.sql

Historical Post design with publisher_email directly on posts, an album foreign key and email/album uniqueness. Current PostJdbcDao expects user_id, so this file is incompatible with the current Post table design.

[persistence/src/main/resources/db/migration/V2__create_posts.sql, lines 1–11](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V2__create_posts.sql>)

```sql
BEGIN;

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    publisher_email VARCHAR(100) NOT NULL,
    album_id INTEGER NOT NULL,
    CONSTRAINT posts_album_id_fkey FOREIGN KEY (album_id) REFERENCES albums(id),
    CONSTRAINT posts_publisher_email_album_id_key UNIQUE (publisher_email, album_id)
);

COMMIT;
```

## V3__seed_initial_post.sql

Historical idempotent seed for the publisher_email Post design. It depends on V2-era columns and is not compatible with the current startup schema.

[persistence/src/main/resources/db/migration/V3__seed_initial_post.sql, lines 1–12](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/db/migration/V3__seed_initial_post.sql>)

```sql
BEGIN;

INSERT INTO posts (publisher_email, album_id)
SELECT 'vendedor@example.com', album.id
FROM albums AS album
JOIN artists AS artist ON artist.id = album.artist_id
WHERE album.title = 'versus'
  AND artist.name = 'illya kuryaki and the valderramas'
  AND album.release_year = 1997
ON CONFLICT (publisher_email, album_id) DO NOTHING;

COMMIT;
```

## users.sql

Manual users table creation. It lacks IF NOT EXISTS and inserts no rows.

[database/users.sql, lines 1–6](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/users.sql>)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT users_email_key UNIQUE (email)
);
```

## albums.sql

Manual fresh catalog setup in an explicit transaction. It creates artists, albums and posts with foreign keys and an album year check, then seeds Versus, its artist, a user and a Post. It assumes users already exists and the other tables do not.

[database/albums.sql, lines 1–50](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/albums.sql>)

```sql
BEGIN;

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    cover_path VARCHAR(255) NOT NULL,
    CONSTRAINT albums_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES artists(id),
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

INSERT INTO albums (title, artist_id, release_year, cover_path)
SELECT 'versus', id, 1997, '/images/covers/versus.png'
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

## seed_dev_posts.sql

Optional development seed. It adds four named artists/albums and links matching albums to the development publisher using ON CONFLICT guards. All covers use versus.png. The final artist-name filter can include additional albums by those artists already in the database. It is not automatically run at startup.

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
-- Todas las tapas apuntan a versus.png, la única imagen que existe hoy en
-- webapp/src/main/webapp/images/covers/. Para tapas reales: dejá los archivos
-- ahí, actualizá cover_path acá y rebuildeá (Jetty sirve desde webapp/target/).

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

INSERT INTO albums (title, artist_id, release_year, cover_path)
SELECT seed.title, artist.id, seed.release_year, seed.cover_path
FROM (VALUES
  ('clics modernos',              'charly garcia', 1983, '/images/covers/versus.png'),
  ('cancion animal',              'soda stereo',   1990, '/images/covers/versus.png'),
  ('alma de diamante',            'spinetta jade', 1980, '/images/covers/versus.png'),
  ('divididos por la felicidad',  'sumo',          1985, '/images/covers/versus.png')
) AS seed(title, artist_name, release_year, cover_path)
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

## schema.sql

Test-only table definitions use HSQLDB identity syntax. They mirror the current startup tables, including the absence of foreign keys and year checks. They are not the historical migration end state.

[persistence/src/test/resources/schema.sql, lines 1–28](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/schema.sql>)

```sql
CREATE TABLE users (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT users_email_key UNIQUE (email)
);

CREATE TABLE artists (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

CREATE TABLE albums (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    cover_path VARCHAR(255) NOT NULL,
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year)
);

CREATE TABLE posts (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id)
);
```

## populator.sql

Test fixture creates one User, Artist, Album and Post, all ID 1. It is applied after the HSQLDB schema. No second User is present, which matters for the second-publisher DAO test.

[persistence/src/test/resources/populator.sql, lines 1–11](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/populator.sql>)

```sql
INSERT INTO users (id, username, email)
VALUES (1, 'bpessagno', 'bpessagno@itba.edu.ar');

INSERT INTO artists (id, name)
VALUES (1, 'illya kuryaki and the valderramas');

INSERT INTO albums (id, title, artist_id, release_year, cover_path)
VALUES (1, 'versus', 1, 1997, '/images/covers/versus.png');

INSERT INTO posts (id, user_id, album_id)
VALUES (1, 1, 1);
```


[[Database schema]] · [[Development tools]] · [[Known gaps and document drift]]
