---
title: "Database schema"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "16f3aa7784c3320f18efb82ee2b1f315d7632faf"
status: "documented"
tags: ["codemap", "persistence"]
sources: ["persistence/src/main/resources/schema.sql"]
---

# Database schema

Startup uses the four CREATE TABLE IF NOT EXISTS statements below. Every table has a generated numeric primary key. Required business fields are NOT NULL, and unique constraints implement identity. There are no FOREIGN KEY declarations and no release-year CHECK in this startup schema.

| Table | Unique identity besides ID | Logical references |
|---|---|---|
| users | email | None |
| artists | name | None |
| albums | artist_id, title, release_year | artist_id → artists.id |
| posts | user_id, album_id | user_id → users.id; album_id → albums.id |

The service normalizes input before comparisons, while the database constraints compare the stored values. Direct SQL with different casing or whitespace can bypass the intended normalized identity convention. The schema does not normalize automatically.

## Exact startup DDL

[persistence/src/main/resources/schema.sql, lines 1–40](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/main/resources/schema.sql>)

```sql
-- Esquema de quieroVinilos para PostgreSQL.
--
-- Lo ejecuta el DataSourceInitializer de WebConfig en CADA arranque del contexto,
-- por eso toda sentencia tiene que ser idempotente. Es lo que permite cumplir la
-- condicion del enunciado: desplegado contra una base PostgreSQL vacia con
-- permisos adecuados, la aplicacion genera sola todas las tablas que necesita.
--
-- El orden sigue las dependencias del dominio: users y artists antes que albums y posts.
--
-- Espejo funcional de persistence/src/test/resources/schema.sql, que declara lo
-- mismo en dialecto HSQLDB para los tests. Si cambia uno, tiene que cambiar el otro.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT users_email_key UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT artists_name_key UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    cover_path VARCHAR(255) NOT NULL,
    CONSTRAINT albums_artist_title_year_key UNIQUE (artist_id, title, release_year)
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    album_id INTEGER NOT NULL,
    CONSTRAINT posts_user_id_album_id_key UNIQUE (user_id, album_id)
);
```

## Read mapping

[[PostJdbcDao]] aliases columns because several joined tables have `id` columns. The aliases distinguish post_id, user_id and album_id, and the RowMapper passes each to [[PostSummary]] in constructor order. `INNER JOIN` means all referenced rows must exist to show the publication.

There are no DAO update/delete methods. That narrows normal application writes, but it does not guarantee referential integrity. Direct SQL, old data or an invalid DAO caller can still create orphans, as the second-publisher [[PostJdbcDaoTest]] illustrates.

CREATE TABLE IF NOT EXISTS creates missing tables only. It does not add new columns to an existing table or reconcile constraints left by historical setup scripts. A database created using database/albums.sql can have foreign keys absent from a clean startup-created database. The actual local database was not inspected.

[[Schema history and seeds]] compares every SQL path. [[Domain and identity]] provides the logical relationship diagram.
