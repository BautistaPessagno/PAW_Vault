---
title: "PostJdbcDao"
categories: ["Persistence"]
type: "code"
module: "persistence"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java"]
---

# PostJdbcDao

Publicaciones con Spring JDBC. Arma el `WHERE` de búsqueda agregando cláusulas fijas con parámetros, comparte ese `WHERE` entre listar y contar, ordena desde un `switch` sobre [[PostSort]], escapa los comodines de `LIKE`, bloquea filas con `FOR UPDATE` (una o varias en orden de id) y cambia estado con guarda. El listado del perfil privado filtra por estado con `IN (...)` y cuenta por estado con `GROUP BY status`.

## Guía de lectura

Datos y dependencias declaradas: `ROW_MAPPER`, `SEARCH_SUGGESTION_ROW_MAPPER`, `SUGGESTION_RANK`, `FIND_SUGGESTIONS_QUERY`, `SUMMARY_SELECT`, `COUNT_SELECT`, `LIKE_ESCAPE`, `LIKE_ESCAPE_CLAUSE`, `NEWEST_FIRST`, `UPDATE_POST`, `jdbcTemplate`, `jdbcInsert`.

Operaciones para localizar en la fuente: `readNullableInt`, `readNullableLong`, `readCondition`, `search`, `countSearch`, `searchWhere`, `findSearchSuggestions`, `findByPublisherId`, `findAvailableByPublisherId`, `countAvailableByPublisherId`, `countByPublisherId`, `countByStatusForPublisher`, `placeholders`, `publisherParameters`, `orderBy`, `escapeLike`, `findById`, `findByIdForUpdate`, `findByIdsForUpdate`, `existsByUserIdAndAlbumId`, `create`, `update`, `updateWithImage`, `updateStatus`, `findOwnImageId`, `findAlbumCoverImageId`, `delete`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AlbumJdbcDao]], [[Condition]], [[DuplicatePostKeyException]], [[Post]], [[PostDao]], [[PostSearchCriteria]], [[PostSort]], [[PostStatus]], [[PostSummary]], [[SearchSuggestion]], [[SearchSuggestionType]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>), líneas 1–400.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSort;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.SearchSuggestion;
import ar.edu.itba.paw.models.SearchSuggestionType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;
import org.springframework.stereotype.Repository;

import javax.sql.DataSource;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Repository
public class PostJdbcDao implements PostDao {

    private static final RowMapper<PostSummary> ROW_MAPPER = (resultSet, rowNum) -> new PostSummary(
            resultSet.getLong("post_id"),
            resultSet.getLong("user_id"),
            resultSet.getString("publisher_email"),
            resultSet.getString("publisher_locale"),
            resultSet.getLong("album_id"),
            resultSet.getString("album_title"),
            resultSet.getString("artist_name"),
            resultSet.getInt("album_release_year"),
            AlbumJdbcDao.readGenre(resultSet),
            readNullableLong(resultSet, "post_image_id"),
            resultSet.getInt("post_price"),
            resultSet.getString("post_description"),
            readCondition(resultSet),
            readNullableInt(resultSet, "post_pressing_year"),
            resultSet.getString("post_zone"),
            PostStatus.valueOf(resultSet.getString("post_status"))
    );

    private static final RowMapper<SearchSuggestion> SEARCH_SUGGESTION_ROW_MAPPER = (resultSet, rowNum) ->
            new SearchSuggestion(
                    SearchSuggestionType.valueOf(resultSet.getString("suggestion_type").trim()),
                    resultSet.getString("suggestion_value"),
                    resultSet.getString("artist_name")
            );

    // Reproduce en SQL el ranking que antes se calculaba en memoria sobre la tabla
    // entera: coincidencia exacta, prefijo del texto completo, prefijo de alguna
    // palabra y, por ultimo, aparicion en cualquier posicion.
    private static final String SUGGESTION_RANK =
            "CASE WHEN REPLACE(search_phrase, ' ', '') = ? THEN 0 "
                    + "WHEN REPLACE(search_phrase, ' ', '') LIKE ? THEN 1 "
                    + "WHEN ' ' || search_phrase LIKE ? THEN 2 ELSE 3 END";

    // El WHERE de afuera es el caso mas amplio de los cuatro, asi que no descarta
    // ninguna fila que el ranking pudiera puntuar.
    private static final String FIND_SUGGESTIONS_QUERY =
            "SELECT suggestion_type, suggestion_value, artist_name FROM ("
                    + "SELECT DISTINCT 'ARTIST' AS suggestion_type, ar.name AS suggestion_value, "
                    + "CAST(NULL AS VARCHAR(255)) AS artist_name, ar.search_phrase AS search_phrase "
                    + "FROM posts p JOIN albums a ON a.id = p.album_id "
                    + "JOIN artists ar ON ar.id = a.artist_id WHERE p.status = ? "
                    + "UNION "
                    + "SELECT DISTINCT 'ALBUM' AS suggestion_type, a.title AS suggestion_value, "
                    + "ar.name AS artist_name, a.search_phrase AS search_phrase "
                    + "FROM posts p JOIN albums a ON a.id = p.album_id "
                    + "JOIN artists ar ON ar.id = a.artist_id WHERE p.status = ?"
                    + ") suggestions WHERE REPLACE(search_phrase, ' ', '') LIKE ? "
                    + "ORDER BY " + SUGGESTION_RANK
                    + ", search_phrase, LOWER(suggestion_value), suggestion_type, LOWER(artist_name) "
                    + "LIMIT ?";

    private static final String SUMMARY_SELECT =
            "SELECT p.id AS post_id, u.id AS user_id, u.email AS publisher_email, " +
                    "u.preferred_locale AS publisher_locale, " +
                    "a.id AS album_id, a.title AS album_title, ar.name AS artist_name, " +
                    "a.release_year AS album_release_year, a.genre AS album_genre, " +
                    "COALESCE(p.image_id, a.cover_image_id) AS post_image_id, " +
                    "p.price AS post_price, p.description AS post_description, " +
                    "p.item_condition AS post_condition, p.pressing_year AS post_pressing_year, " +
                    "p.zone AS post_zone, p.status AS post_status " +
                    "FROM posts p JOIN users u ON u.id = p.user_id " +
                    "JOIN albums a ON a.id = p.album_id JOIN artists ar ON ar.id = a.artist_id ";

    private static final String COUNT_SELECT =
            "SELECT COUNT(*) FROM posts p JOIN albums a ON a.id = p.album_id "
                    + "JOIN artists ar ON ar.id = a.artist_id ";

    private static final String LIKE_ESCAPE = "\\";
    // El SQL y escapeLike() salen del mismo caracter: si cambia uno, cambia el otro.
    private static final String LIKE_ESCAPE_CLAUSE = "ESCAPE '" + LIKE_ESCAPE + "'";
    // Desempate de todo orden: lo publicado mas recientemente primero. Los posts
    // anteriores a created_at comparten fecha y se desempatan por id.
    private static final String NEWEST_FIRST = "p.created_at DESC, p.id DESC";
    private static final String UPDATE_POST =
            "UPDATE posts SET album_id = ?, price = ?, description = ?, item_condition = ?, "
                    + "pressing_year = ?, zone = ?";

    private final JdbcTemplate jdbcTemplate;
    private final SimpleJdbcInsert jdbcInsert;

    private static Integer readNullableInt(final ResultSet resultSet, final String column) throws SQLException {
        final int value = resultSet.getInt(column);
        return resultSet.wasNull() ? null : value;
    }

    private static Long readNullableLong(final ResultSet resultSet, final String column) throws SQLException {
        final long value = resultSet.getLong(column);
        return resultSet.wasNull() ? null : value;
    }

    private static Condition readCondition(final ResultSet resultSet) throws SQLException {
        return Condition.valueOf(resultSet.getString("post_condition"));
    }

    @Autowired
    public PostJdbcDao(final DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("posts")
                // No incluimos created_at: el DEFAULT de la base es el único reloj de publicación.
                .usingColumns("user_id", "album_id", "price", "description", "item_condition", "pressing_year",
                        "zone", "stock", "image_id", "status")
                .usingGeneratedKeyColumns("id");
    }

    @Override
    public List<PostSummary> search(final PostSearchCriteria criteria, final int limit, final int offset) {
        final List<Object> parameters = new ArrayList<>();
        final String where = searchWhere(criteria, parameters);
        parameters.add(limit);
        parameters.add(offset);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + where + "ORDER BY "
                + orderBy(criteria.getSort()) + " LIMIT ? OFFSET ?", ROW_MAPPER, parameters.toArray()));
    }

    @Override
    public int countSearch(final PostSearchCriteria criteria) {
        final List<Object> parameters = new ArrayList<>();
        final String where = searchWhere(criteria, parameters);
        return jdbcTemplate.queryForObject(COUNT_SELECT + where, Integer.class, parameters.toArray());
    }

    // Un solo WHERE para listar y contar: si divergen, la paginacion promete paginas que no existen.
    private static String searchWhere(final PostSearchCriteria criteria, final List<Object> parameters) {
        final List<String> clauses = new ArrayList<>();
        // Los vendidos no se ofrecen: la landing solo lista lo que todavia se puede comprar.
        clauses.add("p.status = ?");
        parameters.add(PostStatus.AVAILABLE.name());
        // La query llega normalizada con SearchText.compact, igual que en las sugerencias:
        // compara contra la misma columna para que las dos encuentren los mismos discos.
        if (criteria.getQuery() != null) {
            final String pattern = "%" + escapeLike(criteria.getQuery()) + "%";
            clauses.add("(REPLACE(a.search_phrase, ' ', '') LIKE ? " + LIKE_ESCAPE_CLAUSE
                    + " OR REPLACE(ar.search_phrase, ' ', '') LIKE ? " + LIKE_ESCAPE_CLAUSE + ")");
            parameters.add(pattern);
            parameters.add(pattern);
        }
        if (criteria.getGenre() != null) {
            clauses.add("a.genre = ?");
            parameters.add(criteria.getGenre().name());
        }
        if (criteria.getCondition() != null) {
            clauses.add("p.item_condition = ?");
            parameters.add(criteria.getCondition().name());
        }
        if (criteria.getArtistId() != null) {
            clauses.add("a.artist_id = ?");
            parameters.add(criteria.getArtistId());
        }
        if (criteria.getReleaseYear() != null) {
            clauses.add("a.release_year = ?");
            parameters.add(criteria.getReleaseYear());
        }
        if (criteria.getMinPrice() != null) {
            clauses.add("p.price >= ?");
            parameters.add(criteria.getMinPrice());
        }
        if (criteria.getMaxPrice() != null) {
            clauses.add("p.price <= ?");
            parameters.add(criteria.getMaxPrice());
        }
        return "WHERE " + String.join(" AND ", clauses) + " ";
    }

    @Override
    public List<SearchSuggestion> findSearchSuggestions(final String normalizedQuery, final int limit) {
        return List.copyOf(jdbcTemplate.query(FIND_SUGGESTIONS_QUERY, SEARCH_SUGGESTION_ROW_MAPPER,
                PostStatus.AVAILABLE.name(), PostStatus.AVAILABLE.name(),
                "%" + normalizedQuery + "%", normalizedQuery, normalizedQuery + "%",
                "% " + normalizedQuery + "%", limit));
    }

    @Override
    public List<PostSummary> findByPublisherId(final long publisherId, final Collection<PostStatus> statuses,
                                               final int limit, final int offset) {
        final List<Object> parameters = publisherParameters(publisherId, statuses);
        parameters.add(limit);
        parameters.add(offset);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.user_id = ? AND p.status IN ("
                        + placeholders(statuses.size()) + ") ORDER BY " + NEWEST_FIRST + " LIMIT ? OFFSET ?",
                ROW_MAPPER, parameters.toArray()));
    }

    @Override
    public List<PostSummary> findAvailableByPublisherId(final long publisherId, final int limit, final int offset) {
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT
                        + "WHERE p.user_id = ? AND p.status = ? ORDER BY " + NEWEST_FIRST + " LIMIT ? OFFSET ?",
                ROW_MAPPER, publisherId, PostStatus.AVAILABLE.name(), limit, offset));
    }

    @Override
    public int countAvailableByPublisherId(final long publisherId) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) FROM posts WHERE user_id = ? AND status = ?",
                Integer.class, publisherId, PostStatus.AVAILABLE.name());
    }

    @Override
    public int countByPublisherId(final long publisherId, final Collection<PostStatus> statuses) {
        return jdbcTemplate.queryForObject("SELECT COUNT(*) FROM posts WHERE user_id = ? AND status IN ("
                + placeholders(statuses.size()) + ")", Integer.class, publisherParameters(publisherId, statuses).toArray());
    }

    @Override
    public Map<PostStatus, Integer> countByStatusForPublisher(final long publisherId) {
        final Map<PostStatus, Integer> counts = new EnumMap<>(PostStatus.class);
        jdbcTemplate.query("SELECT status, COUNT(*) AS total FROM posts WHERE user_id = ? GROUP BY status",
                (RowCallbackHandler) resultSet -> counts.put(PostStatus.valueOf(resultSet.getString("status")),
                        resultSet.getInt("total")),
                publisherId);
        return Collections.unmodifiableMap(counts);
    }

    private static String placeholders(final int count) {
        return String.join(", ", Collections.nCopies(count, "?"));
    }

    private static List<Object> publisherParameters(final long publisherId, final Collection<PostStatus> statuses) {
        final List<Object> parameters = new ArrayList<>();
        parameters.add(publisherId);
        statuses.forEach(status -> parameters.add(status.name()));
        return parameters;
    }

    // Cada criterio mapea a un ORDER BY fijo: al SQL nunca entra texto del usuario.
    private static String orderBy(final PostSort sort) {
        switch (sort) {
            case OLDEST:
                return "p.created_at ASC, p.id ASC";
            case PRICE_ASC:
                return "p.price ASC, " + NEWEST_FIRST;
            case PRICE_DESC:
                return "p.price DESC, " + NEWEST_FIRST;
            case TITLE_ASC:
                return "LOWER(a.title) ASC, " + NEWEST_FIRST;
            case TITLE_DESC:
                return "LOWER(a.title) DESC, " + NEWEST_FIRST;
            case ARTIST_ASC:
                return "LOWER(ar.name) ASC, " + NEWEST_FIRST;
            case ARTIST_DESC:
                return "LOWER(ar.name) DESC, " + NEWEST_FIRST;
            case RELEASE_YEAR_ASC:
                return "a.release_year ASC, " + NEWEST_FIRST;
            case RELEASE_YEAR_DESC:
                return "a.release_year DESC, " + NEWEST_FIRST;
            case NEWEST:
            default:
                return NEWEST_FIRST;
        }
    }

    // Los comodines de LIKE que escriba el usuario se buscan literalmente: "%" no puede traer todo el catalogo.
    private static String escapeLike(final String value) {
        return value.replace(LIKE_ESCAPE, LIKE_ESCAPE + LIKE_ESCAPE)
                .replace("%", LIKE_ESCAPE + "%")
                .replace("_", LIKE_ESCAPE + "_");
    }

    @Override
    public Optional<PostSummary> findById(final long id) {
        return jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.id = ?", ROW_MAPPER, id).stream().findFirst();
    }

    @Override
    public Optional<PostSummary> findByIdForUpdate(final long id) {
        if (jdbcTemplate.queryForList("SELECT id FROM posts WHERE id = ? FOR UPDATE", Long.class, id).isEmpty()) {
            return Optional.empty();
        }
        return findById(id);
    }

    // Dos sentencias fijas para cualquier cantidad de posts: el bloqueo en orden de id y
    // despues los summaries, sin un findById por post.
    @Override
    public List<PostSummary> findByIdsForUpdate(final Collection<Long> ids) {
        if (ids.isEmpty()) {
            return List.of();
        }
        final String placeholders = String.join(", ", Collections.nCopies(ids.size(), "?"));
        final Object[] parameters = ids.toArray();
        jdbcTemplate.queryForList("SELECT id FROM posts WHERE id IN (" + placeholders + ") ORDER BY id FOR UPDATE",
                Long.class, parameters);
        return List.copyOf(jdbcTemplate.query(SUMMARY_SELECT + "WHERE p.id IN (" + placeholders + ") ORDER BY p.id",
                ROW_MAPPER, parameters));
    }

    @Override
    public boolean existsByUserIdAndAlbumId(final long userId, final long albumId) {
        return Boolean.TRUE.equals(jdbcTemplate.queryForObject(
                "SELECT COUNT(*) > 0 AS post_exists FROM posts WHERE user_id = ? AND album_id = ?",
                Boolean.class, userId, albumId));
    }

    @Override
    public Post create(final long userId, final long albumId, final int price, final String description,
                       final Condition condition, final Integer pressingYear, final String zone, final Long imageId) {
        final Map<String, Object> parameters = new HashMap<>();
        parameters.put("user_id", userId);
        parameters.put("album_id", albumId);
        parameters.put("price", price);
        parameters.put("description", description);
        parameters.put("item_condition", condition == null ? null : condition.name());
        parameters.put("pressing_year", pressingYear);
        parameters.put("zone", zone);
        parameters.put("stock", 1);
        parameters.put("image_id", imageId);
        parameters.put("status", PostStatus.AVAILABLE.name());
        try {
            final Number id = jdbcInsert.executeAndReturnKey(parameters);
            return new Post(id.longValue(), userId, albumId, price, description, condition, pressingYear, zone,
                    imageId, PostStatus.AVAILABLE);
        } catch (final DuplicateKeyException e) {
            throw new DuplicatePostKeyException();
        }
    }

    @Override
    public boolean update(final long id, final long albumId, final int price, final String description,
                          final Condition condition, final Integer pressingYear, final String zone) {
        try {
            return jdbcTemplate.update(UPDATE_POST + " WHERE id = ?", albumId, price, description,
                    condition == null ? null : condition.name(), pressingYear, zone, id) == 1;
        } catch (final DuplicateKeyException e) {
            throw new DuplicatePostKeyException();
        }
    }

    @Override
    public boolean updateWithImage(final long id, final long albumId, final int price, final String description,
                                   final Condition condition, final Integer pressingYear, final String zone,
                                   final Long imageId) {
        try {
            return jdbcTemplate.update(UPDATE_POST + ", image_id = ? WHERE id = ?", albumId, price, description,
                    condition == null ? null : condition.name(), pressingYear, zone, imageId, id) == 1;
        } catch (final DuplicateKeyException e) {
            throw new DuplicatePostKeyException();
        }
    }

    // Guarda de estado en el WHERE: si otra transaccion ya movio el post, no actualiza nada.
    @Override
    public boolean updateStatus(final long id, final PostStatus from, final PostStatus to) {
        return jdbcTemplate.update("UPDATE posts SET status = ? WHERE id = ? AND status = ?",
                to.name(), id, from.name()) == 1;
    }

    @Override
    public Optional<Long> findOwnImageId(final long id) {
        return jdbcTemplate.queryForList("SELECT image_id FROM posts WHERE id = ? AND image_id IS NOT NULL",
                        Long.class, id)
                .stream()
                .findFirst();
    }

    @Override
    public Optional<Long> findAlbumCoverImageId(final long id) {
        return jdbcTemplate.queryForList("SELECT a.cover_image_id FROM posts p JOIN albums a ON a.id = p.album_id " +
                        "WHERE p.id = ? AND a.cover_image_id IS NOT NULL", Long.class, id)
                .stream()
                .findFirst();
    }

    @Override
    public boolean delete(final long id) {
        return jdbcTemplate.update("DELETE FROM posts WHERE id = ?", id) == 1;
    }
}
```
