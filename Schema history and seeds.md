---
title: "Schema history and seeds"
categories: ["Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["database/users.sql", "database/seed_dev_posts.sql", "database/demo_posts.tsv", "persistence/src/test/resources/populator.sql", "tools/sql/demo-users.sql"]
---

# Schema history and seeds

The canonical runtime schema lives in persistence/src/main/resources/schema.sql. The deleted Flyway migrations remain historical Git evidence. database/albums.sql, the old one-time catalog bootstrap, was deleted in this range; tools/setup_local_postgres.sh now applies the canonical schema instead.

| Path | Role |
|---|---|
| database/users.sql | Old manual user table bootstrap, no longer used by the setup script |
| database/demo_posts.tsv | Manifest of 24 demo publications: artist, album, year, genre, price, condition, pressing year, zone, description, MusicBrainz release-group ID and expected SHA-256 of the cover |
| database/seed_dev_posts.sql | Idempotent reference data and a temporary pg_temp.seed_demo_post function; inserts 200 artists and is only run inside tools/seed_local_data.sh |
| persistence/src/test/resources/populator.sql | HSQLDB fixtures for users, verification and reset tokens, catalog with search phrases, images, AVAILABLE/SOLD posts and inquiries including detached ones |
| tools/sql/demo-users.sql | Optional manual enabled USER/ADMIN accounts; outside the classpath, never automatic, preserves existing emails |

tools/seed_local_data.sh validates the manifest (exactly 24 rows of 12 columns), downloads each cover from the Cover Art Archive, checks MIME type, size and checksum, and only then opens one transaction that loads the demo users, the seed SQL and one call per row. A final DO block requires 24 unique seeded posts, at least 200 artists and valid prices, statuses and images. It targets the `paw-pg` Docker container by default. README warns to review Cover Art Archive rights before using the covers outside a local environment.

The seed SQL inserts artists with name and normalized_name and albums with title, artist, year and genre, but not search_phrase. schema.sql now declares search_phrase NOT NULL without a default on both tables. A static reading therefore suggests the seed fails on a database already created by the current startup schema; this was not executed. [[Known gaps and document drift]] records it.

The test fixture includes realistic related user rows, dated publications, AVAILABLE/SOLD posts, PENDING/ACCEPTED/REJECTED inquiries and rows for paged inbox groups. Those fixtures do not exercise PostgreSQL upgrades. Demo credentials are documented in the source README; their values are not copied into this vault. No SQL was run for this refresh.

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

## database/demo_posts.tsv

[database/demo_posts.tsv, lines 1–25](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/demo_posts.tsv>)

```text
key	artist	album	release_year	genre	price	condition	pressing_year	zone	description	release_group_mbid	sha256
artaud	Pescado Rabioso	Artaud	1973	ROCK	35000	USED	1973	Villa Crespo	Edición nacional cuidada, con leves marcas de uso.	8e50433a-c1d5-3019-a48d-0d6b97a5f32b	bb4b94af7d53b7c11069e14d50622e9bee42576127545b19aab9fbc52c1c1c37
cancion-animal	Soda Stereo	Canción Animal	1990	ROCK	48000	USED	1990	Palermo	Prensado argentino con tapa y sobre interior conservados.	fdf231ee-2d2b-3238-8adc-352475606e6a	8275cbcdfc62a6ab98204c8df3944931cfd3e2a409d81eb7795632436db7f965
bocanada	Gustavo Cerati	Bocanada	1999	ROCK	55000	USED	1999	Colegiales	Copia de época en muy buen estado general.	22d84dc0-84cb-3934-8aa6-4af8fa6671f8	58f3f1f59403165219335ab3e72ccb3ebf9ec2d840d2eb2acef28d99e6d87361
clics-modernos	Charly García	Clics Modernos	1983	ROCK	42000	USED	1983	Almagro	Vinilo probado, sin saltos y con desgaste normal en la tapa.	33eaf398-1164-32e3-9055-3bcbff8f3b12	1a9973d8bc427a24268cb8423e200ec17edd21b913faa33c2a0fbc03288991e8
el-amor-despues-del-amor	Fito Páez	El amor después del amor	1992	ROCK	38000	USED	1992	Caballito	Edición argentina completa y bien conservada.	4126c357-fb4d-3e30-97c6-6c8b0e09781a	444bf6283145be69df02f83dd0ed551c17e32347eb8a5c9f962667f199b3fd2c
oktubre	Patricio Rey y sus Redonditos de Ricota	Oktubre	1986	ROCK	46000	USED	1986	Boedo	Prensado nacional con sonido limpio y tapa original.	8b916008-5ced-3e29-a69b-73ecd2fd915c	9cc1a6cf65ded70594d43d93770f1c45a8a57f5611004c9cc054da2fccca9aed
jessico	Babasónicos	Jessico	2001	ROCK	34000	USED	2001	Chacarita	Primera edición argentina, reproducida y revisada.	b5353410-b2d1-362a-b64e-c2deb99770e5	fcf640ca3248270a6df202bcdbad4f2422f3a3bf52edef2bdd6d9f90a9262ec1
re	Café Tacvba	Re	1994	ROCK	52000	USED	1994	Belgrano	Edición latinoamericana difícil de conseguir.	05548ae5-6e3d-3e7b-baee-5e03a80fe5d2	27894c69f98f51aac9b20bde6466e6f609d740605dc3ceb7ca717abd5cf81d4c
abbey-road	The Beatles	Abbey Road	1969	ROCK	65000	USED	2019	Recoleta	Reedición de 180 gramos, abierta y reproducida pocas veces.	9162580e-5df4-32de-80cc-f45a8d8a9b1d	8ad081259802fbc4390a4171016daa11d8db1b555f591f06b6eda2d08d5466a6
dark-side	Pink Floyd	The Dark Side of the Moon	1973	ROCK	72000	NEW	2016	Palermo	Reedición sellada de 180 gramos.	f5093c06-23e3-404f-aeaa-40f72885ee3a	852e90de98088902e8e0393579c1b0e63a0f3e135e013477f9a4093968be53e0
rumours	Fleetwood Mac	Rumours	1977	ROCK	58000	USED	1977	Núñez	Copia de época con insert y marcas superficiales leves.	416bb5e5-c7d1-3977-8fd7-7c9daf6c2be6	5fa6bc8ad6679a9b0759965020a7c4153b1e80a812177d974aa358c8ca974e0a
thriller	Michael Jackson	Thriller	1982	POP	50000	USED	1982	Flores	Edición original en excelente estado de reproducción.	f32fab67-77dd-3937-addc-9062e28e4c37	71defd5a9c234af928c5db58943a29659ee8e88a64cfd14a1e0d0ef3fd2ee401
purple-rain	Prince	Purple Rain	1984	POP	54000	USED	1984	San Telmo	Prensado de época con funda interior original.	b93a7c47-a6d4-33f2-9034-53fdd991f4ba	9d98e3fd42e0d3497647f631de820c8683e8942ae5598d185e7099f7969de2e0
nevermind	Nirvana	Nevermind	1991	ROCK	60000	USED	1991	Villa Urquiza	Edición europea cuidada, sin saltos ni ruido fuerte.	1b022e01-4da6-387b-8658-8678046e4cef	9e1697896f1af13a76701bc5cb151fbb1207efd6c6a45fd64b77cc8b30c8ca14
ok-computer	Radiohead	OK Computer	1997	ROCK	68000	NEW	2017	Colegiales	Reedición aniversario sin uso.	b1392450-e666-3926-a536-22c65f834433	cf91d0583ed512a594d9b2c66efa0245b49b8cbac0f7868f9bf5a80705c087ce
miseducation	Lauryn Hill	The Miseducation of Lauryn Hill	1998	HIP_HOP	62000	NEW	2016	Caballito	Reedición doble, nueva y conservada en funda protectora.	8691d12c-abd8-385c-b1eb-d841190124f7	ef405e8fc1e8144034818fc12ad7c419d06a4315147744f4f162074053588930
discovery	Daft Punk	Discovery	2001	ELECTRONIC	70000	NEW	2021	Palermo	Reedición doble sellada.	48117b90-a16e-34ca-a514-19c702df1158	679288ee17aebafd7f1d43b9d9bd59120f27f903e591f67f6dabdb0ebe28c4b4
back-to-black	Amy Winehouse	Back to Black	2006	SOUL_FUNK	49000	NEW	2015	Recoleta	Reedición de 180 gramos, sin abrir.	6eac2e57-ee50-36f8-b0c4-c4c847a2c098	21b597f031ee1532442dee283df0fd8f1cf838eb0807fe53d815f3ec7acb34c3
am	Arctic Monkeys	AM	2013	ROCK	44000	NEW	2013	Belgrano	Edición estándar nueva, guardada verticalmente.	a348ba2f-f8b3-4686-b928-e63d8d94d543	215f348d3eb8a7601a80df9715b273f3855460e5a52f7ffbfbbfc8b8ddfdf944
to-pimp-a-butterfly	Kendrick Lamar	To Pimp a Butterfly	2015	HIP_HOP	75000	NEW	2022	Almagro	Reedición doble sellada.	d9103c72-3807-4378-9ce7-b6f3e8fdd547	975ab57fbe76cd65ebe023805867b8173ed3453780c80501b9a277e2419325ef
ziggy-stardust	David Bowie	The Rise and Fall of Ziggy Stardust and the Spiders From Mars	1972	ROCK	66000	USED	1972	San Telmo	Edición de época con tapa desplegable bien conservada.	6c9ae3dd-32ad-472c-96be-69d0a3536261	4746e207e47538717b00cd685a02e327b5017e33b58656eccfee96d5e39edeae
queen-is-dead	The Smiths	The Queen Is Dead	1986	ROCK	57000	USED	1986	Villa Crespo	Prensado europeo con funda interior.	d8dde278-482c-3cc8-a530-fea70476f3a5	8c21c019ee5b42235ae8100a61ae6c8b547a56060b973a8c148ff205362561c0
is-this-it	The Strokes	Is This It	2001	ROCK	43000	NEW	2020	Chacarita	Reedición nueva con arte internacional.	efea26d1-a016-30f6-b8e2-bc8c02336b0a	ec35748ec94aad811009f4ae1e40ddc3907f7dc44bfe0d88d7a06774050ab4ed
demon-days	Gorillaz	Demon Days	2005	ELECTRONIC	47000	NEW	2017	Núñez	Reedición doble nueva y completa.	f959a46a-a136-3134-9412-6572b23fad95	c5cd0a884a5857e9a5c1498c3c4fe5f978dcecade2054d0c812fd3d3dc21a908
```

## database/seed_dev_posts.sql

[database/seed_dev_posts.sql, lines 1–182](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/database/seed_dev_posts.sql>)

```sql
-- Datos de referencia y helpers temporales para el seed manual de desarrollo.
--
-- No es DDL estructural y no se ejecuta al iniciar la aplicacion. La estructura
-- vive exclusivamente en persistence/src/main/resources/schema.sql. El wrapper
-- tools/seed_local_data.sh descarga y valida las tapas antes de incluir este
-- archivo dentro de una unica transaccion.

INSERT INTO artists (name, normalized_name)
SELECT seed.name, REGEXP_REPLACE(LOWER(seed.name), '[^[:alnum:]]', '', 'g')
FROM (VALUES
    -- Argentina y Latinoamerica (60)
    ('Pescado Rabioso'), ('Soda Stereo'), ('Gustavo Cerati'), ('Charly García'),
    ('Fito Páez'), ('Patricio Rey y sus Redonditos de Ricota'), ('Babasónicos'),
    ('Café Tacvba'), ('Luis Alberto Spinetta'), ('Almendra'), ('Invisible'),
    ('Spinetta Jade'), ('Sumo'), ('Divididos'), ('Los Fabulosos Cadillacs'),
    ('Virus'), ('Serú Girán'), ('Sui Generis'), ('Mercedes Sosa'),
    ('Astor Piazzolla'), ('Atahualpa Yupanqui'), ('León Gieco'),
    ('Andrés Calamaro'), ('Los Rodríguez'), ('Los Auténticos Decadentes'),
    ('Bersuit Vergarabat'), ('Los Abuelos de la Nada'),
    ('Illya Kuryaki and the Valderramas'), ('Airbag'), ('Miranda!'),
    ('Conociendo Rusia'), ('Wos'), ('Trueno'), ('Nicki Nicole'),
    ('Nathy Peluso'), ('María Becerra'), ('Duki'), ('Bizarrap'), ('Lali'),
    ('Tan Biónica'), ('Los Piojos'), ('Ciro y Los Persas'), ('Las Pelotas'),
    ('Rata Blanca'), ('Hermética'), ('V8'), ('Attaque 77'), ('Massacre'),
    ('Él Mató a un Policía Motorizado'), ('Natalia Lafourcade'), ('Caifanes'),
    ('Maná'), ('Los Prisioneros'), ('Violeta Parra'), ('Mon Laferte'),
    ('Jorge Drexler'), ('Rubén Blades'), ('Juanes'), ('Shakira'), ('Calle 13'),

    -- Catalogo global (140)
    ('The Beatles'), ('Pink Floyd'), ('Fleetwood Mac'), ('Michael Jackson'),
    ('Prince'), ('Nirvana'), ('Radiohead'), ('Lauryn Hill'), ('Daft Punk'),
    ('Amy Winehouse'), ('Arctic Monkeys'), ('Kendrick Lamar'), ('David Bowie'),
    ('The Smiths'), ('The Strokes'), ('Gorillaz'), ('The Rolling Stones'),
    ('Led Zeppelin'), ('Queen'), ('Bob Dylan'), ('Joni Mitchell'),
    ('Stevie Wonder'), ('Marvin Gaye'), ('Aretha Franklin'), ('James Brown'),
    ('Elvis Presley'), ('Chuck Berry'), ('Little Richard'), ('Ray Charles'),
    ('Sam Cooke'), ('Otis Redding'), ('The Beach Boys'), ('The Doors'),
    ('The Who'), ('The Kinks'), ('The Velvet Underground'), ('Talking Heads'),
    ('The Clash'), ('Ramones'), ('Sex Pistols'), ('Joy Division'), ('New Order'),
    ('The Cure'), ('Depeche Mode'), ('R.E.M.'), ('U2'), ('Bruce Springsteen'),
    ('Patti Smith'), ('Lou Reed'), ('Iggy Pop'), ('Blondie'), ('Kate Bush'),
    ('Björk'), ('PJ Harvey'), ('Fiona Apple'), ('Tori Amos'),
    ('Sinéad O''Connor'), ('Madonna'), ('Whitney Houston'), ('Beyoncé'),
    ('Rihanna'), ('Taylor Swift'), ('Adele'), ('Billie Eilish'), ('Lana Del Rey'),
    ('Lorde'), ('Lady Gaga'), ('Britney Spears'), ('Janet Jackson'),
    ('Mariah Carey'), ('Sade'), ('Erykah Badu'), ('D''Angelo'), ('Frank Ocean'),
    ('Tyler, the Creator'), ('Kanye West'), ('Jay-Z'), ('Nas'),
    ('The Notorious B.I.G.'), ('2Pac'), ('Eminem'), ('Outkast'),
    ('A Tribe Called Quest'), ('Wu-Tang Clan'), ('Public Enemy'),
    ('Run-D.M.C.'), ('Beastie Boys'), ('Dr. Dre'), ('Snoop Dogg'),
    ('Missy Elliott'), ('J. Cole'), ('Drake'), ('The Weeknd'),
    ('Anderson .Paak'), ('Childish Gambino'), ('Solange'), ('Alicia Keys'),
    ('Metallica'), ('Black Sabbath'), ('Iron Maiden'), ('Judas Priest'),
    ('Motörhead'), ('AC/DC'), ('Guns N'' Roses'), ('Aerosmith'), ('Pearl Jam'),
    ('Soundgarden'), ('Alice in Chains'), ('The Smashing Pumpkins'),
    ('Foo Fighters'), ('Red Hot Chili Peppers'), ('Green Day'), ('Oasis'),
    ('Blur'), ('Pulp'), ('Suede'), ('Muse'), ('The Killers'),
    ('Queens of the Stone Age'), ('Tame Impala'), ('Kraftwerk'), ('Brian Eno'),
    ('Aphex Twin'), ('The Chemical Brothers'), ('Massive Attack'), ('Portishead'),
    ('Boards of Canada'), ('Moby'), ('LCD Soundsystem'), ('Justice'),
    ('Miles Davis'), ('John Coltrane'), ('Nina Simone'), ('Ella Fitzgerald'),
    ('Billie Holiday'), ('Duke Ellington'), ('Thelonious Monk'),
    ('Herbie Hancock'), ('Charles Mingus'), ('Bob Marley')
) AS seed(name)
ON CONFLICT (normalized_name) DO UPDATE SET name = EXCLUDED.name;

-- Elimina solamente el artefacto creado por el smoke de autenticacion local.
CREATE TEMP TABLE removed_smoke_images AS
SELECT p.image_id
FROM posts p
JOIN albums a ON a.id = p.album_id
JOIN artists ar ON ar.id = a.artist_id
WHERE ar.normalized_name = 'authsmokeartist'
  AND LOWER(a.title) = 'auth smoke album'
  AND p.image_id IS NOT NULL;

DELETE FROM inquiries
WHERE post_id IN (
    SELECT p.id FROM posts p
    JOIN albums a ON a.id = p.album_id
    JOIN artists ar ON ar.id = a.artist_id
    WHERE ar.normalized_name = 'authsmokeartist'
      AND LOWER(a.title) = 'auth smoke album'
);

DELETE FROM posts
WHERE album_id IN (
    SELECT a.id FROM albums a
    JOIN artists ar ON ar.id = a.artist_id
    WHERE ar.normalized_name = 'authsmokeartist'
      AND LOWER(a.title) = 'auth smoke album'
);

DELETE FROM images
WHERE id IN (SELECT image_id FROM removed_smoke_images)
  AND NOT EXISTS (SELECT 1 FROM posts WHERE posts.image_id = images.id)
  AND NOT EXISTS (SELECT 1 FROM albums WHERE albums.cover_image_id = images.id);

DELETE FROM albums
WHERE LOWER(title) = 'auth smoke album'
  AND artist_id IN (SELECT id FROM artists WHERE normalized_name = 'authsmokeartist')
  AND NOT EXISTS (SELECT 1 FROM posts WHERE posts.album_id = albums.id);

DELETE FROM artists
WHERE normalized_name = 'authsmokeartist'
  AND NOT EXISTS (SELECT 1 FROM albums WHERE albums.artist_id = artists.id);

-- El wrapper invoca esta funcion temporal una vez por fila del manifiesto. Al
-- re-ejecutar, reutiliza album/post e inserta una imagen solo si todavia falta.
CREATE OR REPLACE FUNCTION pg_temp.seed_demo_post(
    p_artist_name TEXT, p_album_title TEXT, p_release_year INTEGER,
    p_genre TEXT, p_price INTEGER, p_condition TEXT, p_pressing_year INTEGER,
    p_zone TEXT, p_description TEXT, p_content_type TEXT, p_image_data BYTEA
) RETURNS BIGINT AS $$
DECLARE
    selected_artist_id BIGINT;
    selected_album_id BIGINT;
    selected_post_id BIGINT;
    selected_image_id BIGINT;
    publisher_id BIGINT;
BEGIN
    SELECT id INTO selected_artist_id
    FROM artists
    WHERE normalized_name = REGEXP_REPLACE(
        LOWER(p_artist_name COLLATE "default"), '[^[:alnum:]]', '', 'g');

    IF selected_artist_id IS NULL THEN
        INSERT INTO artists (name, normalized_name)
        VALUES (p_artist_name, REGEXP_REPLACE(
            LOWER(p_artist_name COLLATE "default"), '[^[:alnum:]]', '', 'g'))
        RETURNING id INTO selected_artist_id;
    END IF;

    SELECT id INTO selected_album_id
    FROM albums
    WHERE artist_id = selected_artist_id
      AND LOWER(title) = LOWER(p_album_title)
      AND release_year = p_release_year;

    IF selected_album_id IS NULL THEN
        INSERT INTO albums (title, artist_id, release_year, genre)
        VALUES (p_album_title, selected_artist_id, p_release_year, p_genre)
        RETURNING id INTO selected_album_id;
    ELSE
        UPDATE albums
        SET title = p_album_title,
            genre = COALESCE(genre, p_genre)
        WHERE id = selected_album_id;
    END IF;

    SELECT id, image_id INTO selected_post_id, selected_image_id
    FROM posts
    WHERE album_id = selected_album_id AND status = 'AVAILABLE'
    ORDER BY id LIMIT 1;

    IF selected_image_id IS NULL THEN
        INSERT INTO images (content_type, data)
        VALUES (p_content_type, p_image_data)
        RETURNING id INTO selected_image_id;
    END IF;

    IF selected_post_id IS NULL THEN
        SELECT id INTO publisher_id FROM users WHERE email = 'usuario.demo@example.com';
        INSERT INTO posts (user_id, album_id, price, description, item_condition,
                           pressing_year, zone, stock, image_id, status)
        VALUES (publisher_id, selected_album_id, p_price, p_description, p_condition,
                p_pressing_year, p_zone, 1, selected_image_id, 'AVAILABLE')
        RETURNING id INTO selected_post_id;
    ELSE
        UPDATE posts
        SET price = COALESCE(price, p_price),
            description = COALESCE(description, p_description),
            item_condition = COALESCE(item_condition, p_condition),
            pressing_year = COALESCE(pressing_year, p_pressing_year),
            zone = COALESCE(zone, p_zone),
            image_id = COALESCE(image_id, selected_image_id)
        WHERE id = selected_post_id;
    END IF;

    RETURN selected_post_id;
END;
$$ LANGUAGE plpgsql;
```

## persistence/src/test/resources/populator.sql

[persistence/src/test/resources/populator.sql, lines 1–97](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/persistence/src/test/resources/populator.sql>)

```sql
INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (1, 'bpessagno', 'bpessagno@itba.edu.ar', '$2a$12$FpiCwPCeBQTF3ihFUejq2Oz4HO.SYw2n4z1fgYoZ3bpZI67EDcIFm', 'USER', TRUE, 'es');

INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (2, 'tgorganchian', 'tgorganchian@itba.edu.ar', '$2a$12$InUBNvxsWcA9mXYXqKOoAuysB1rA4gF.dteOO/IUP6YvMKzYvtvru', 'ADMIN', TRUE, 'fr');

INSERT INTO users (id, username, email, password_hash, role, enabled, preferred_locale)
VALUES (3, 'legacy', 'legacy@example.com', NULL, 'USER', FALSE, 'en');

INSERT INTO email_verification_tokens (id, user_id, token)
VALUES (1, 3, 'pending-user-verification-token');

INSERT INTO password_reset_tokens (id, user_id, token, expires_at)
VALUES (1, 1, 'live-password-reset-token', TIMESTAMP '2999-01-01 00:00:00');

INSERT INTO password_reset_tokens (id, user_id, token, expires_at)
VALUES (2, 2, 'expired-password-reset-token', TIMESTAMP '2020-01-01 00:00:00');

INSERT INTO artists (id, name, normalized_name, search_phrase)
VALUES (1, 'illya kuryaki and the valderramas', 'illyakuryakiandthevalderramas', 'illya kuryaki and the valderramas');

INSERT INTO artists (id, name, normalized_name, search_phrase)
VALUES (2, 'soda stereo', 'sodastereo', 'soda stereo');

INSERT INTO artists (id, name, normalized_name, search_phrase)
VALUES (3, 'sold only artist', 'soldonlyartist', 'sold only artist');

-- Artista con acento y sin publicaciones: sostiene los tests de sugerencias que
-- comprueban que search_phrase ignora los diacriticos. Al no tener posts no
-- aparece en las sugerencias del buscador, que solo miran publicaciones.
INSERT INTO artists (id, name, normalized_name, search_phrase)
VALUES (4, 'Café Tacvba', 'cafétacvba', 'cafe tacvba');

INSERT INTO images (id, content_type, data)
VALUES (1, 'image/png', X'89504E470D0A1A0A');

-- Foto propia de la publicacion 5, distinta de la portada del album.
INSERT INTO images (id, content_type, data)
VALUES (2, 'image/jpeg', X'FFD8FFE0');

-- Imagen que nadie referencia, para poder borrarla.
INSERT INTO images (id, content_type, data)
VALUES (3, 'image/webp', X'52494646');

INSERT INTO albums (id, title, artist_id, release_year, genre, cover_image_id, search_phrase)
VALUES (1, 'versus', 1, 1997, 'HIP_HOP', 1, 'versus');

INSERT INTO albums (id, title, artist_id, release_year, genre, cover_image_id, search_phrase)
VALUES (2, 'cancion animal', 2, 1990, 'ROCK', NULL, 'cancion animal');

INSERT INTO albums (id, title, artist_id, release_year, genre, cover_image_id, search_phrase)
VALUES (3, 'sold only album', 3, 2000, 'ROCK', NULL, 'sold only album');

-- created_at no sigue el orden de los ids a proposito: asi los tests de orden
-- distinguen "mas nuevo" (fecha) de "id mas alto".
-- Post anterior a los detalles opcionales, con precio y condicion obligatorios.
INSERT INTO posts (id, user_id, album_id, price, item_condition, created_at)
VALUES (1, 1, 1, 35000, 'USED', '2026-02-15 10:00:00');

-- Post con todos los datos comerciales cargados.
INSERT INTO posts (id, user_id, album_id, price, description, item_condition, pressing_year, zone, stock, created_at)
VALUES (2, 2, 1, 45000, 'Prensado japones, tapa con leve desgaste.', 'USED', 2015, 'Palermo', 2, '2026-01-01 10:00:00');

-- Post de otro album y otro artista, el mas reciente y el mas barato.
INSERT INTO posts (id, user_id, album_id, price, item_condition, created_at)
VALUES (3, 1, 2, 30000, 'USED', '2026-03-01 10:00:00');

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
INSERT INTO posts (id, user_id, album_id, price, item_condition, status, created_at)
VALUES (4, 3, 2, 20000, 'USED', 'SOLD', '2026-01-15 10:00:00');

INSERT INTO posts (id, user_id, album_id, price, item_condition, status, image_id, created_at)
VALUES (5, 1, 3, 25000, 'USED', 'SOLD', 2, '2026-01-16 10:00:00');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (5, 4, 1, 'Me lo llevo.', '2026-03-06 10:00:00', 'ACCEPTED');

INSERT INTO inquiries (id, post_id, buyer_id, message, created_at, status)
VALUES (6, 4, 2, NULL, '2026-03-07 10:00:00', 'REJECTED');

-- Consulta cuya publicacion fue eliminada: conserva album y vendedor para seguir mostrandose.
INSERT INTO inquiries (id, post_id, album_id, seller_id, buyer_id, message, created_at, status)
VALUES (7, NULL, 3, 1, 3, 'Sigue disponible?', '2026-03-08 10:00:00', 'REJECTED');
```

[Optional demo seed](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/tools/sql/demo-users.sql>)

[[Database schema]] · [[Development tools]] · [[Authentication flow]] · [[Testing and evidence]]
