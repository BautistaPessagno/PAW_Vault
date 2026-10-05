---
title: "PostDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java"]
---

# PostDao

Contrato de publicaciones: búsqueda y conteo con filtros, sugerencias, listados por publicante (el privado filtrado por un conjunto de estados, con conteo por estado para los chips), lectura con bloqueo de una o varias filas, alta, edición, cambio de estado con guarda y borrado.

## Guía de lectura

Operaciones para localizar en la fuente: `search`, `countSearch`, `findSearchSuggestions`, `findByPublisherId`, `findAvailableByPublisherId`, `countAvailableByPublisherId`, `countByPublisherId`, `countByStatusForPublisher`, `findById`, `findByIdForUpdate`, `findByIdsForUpdate`, `existsByUserIdAndAlbumId`, `create`, `update`, `updateWithImage`, `updateStatus`, `findOwnImageId`, `findAlbumCoverImageId`, `delete`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[Post]], [[PostSearchCriteria]], [[PostStatus]], [[PostSummary]], [[SearchSuggestion]].

Referenciado por: [[PostJdbcDao]], [[PostJdbcDaoTest]], [[PostServiceImpl]], [[PostServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PostDao.java>), líneas 1–65.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchSuggestion;

import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public interface PostDao {
    List<PostSummary> search(PostSearchCriteria criteria, int limit, int offset);

    int countSearch(PostSearchCriteria criteria);

    // normalizedQuery llega ya pasada por SearchText.compact: el ranking se
    // resuelve contra la columna search_phrase, sin traer la tabla entera.
    List<SearchSuggestion> findSearchSuggestions(String normalizedQuery, int limit);

    // Solo los Posts en statuses: "todas" es la lista completa.
    List<PostSummary> findByPublisherId(long publisherId, Collection<PostStatus> statuses, int limit, int offset);

    List<PostSummary> findAvailableByPublisherId(long publisherId, int limit, int offset);

    int countAvailableByPublisherId(long publisherId);

    // Total de publicaciones de un publicante en statuses, para numerar las paginas del perfil.
    int countByPublisherId(long publisherId, Collection<PostStatus> statuses);

    // Para los filtros de "Mis publicaciones". Los estados sin Posts no estan en el mapa.
    Map<PostStatus, Integer> countByStatusForPublisher(long publisherId);

    Optional<PostSummary> findById(long id);

    Optional<PostSummary> findByIdForUpdate(long id);

    // Bloquea las filas en orden de id, asi dos transacciones que comparten posts no se
    // traban entre si, y devuelve los summaries de los que existen.
    List<PostSummary> findByIdsForUpdate(Collection<Long> ids);

    boolean existsByUserIdAndAlbumId(long userId, long albumId);

    Post create(long userId, long albumId, int price, String description, Condition condition,
                Integer pressingYear, String zone, Long imageId);

    boolean update(long id, long albumId, int price, String description, Condition condition,
                   Integer pressingYear, String zone);

    boolean updateWithImage(long id, long albumId, int price, String description, Condition condition,
                            Integer pressingYear, String zone, Long imageId);

    // Guarda de estado: solo actualiza si el post esta en el estado "from" esperado.
    boolean updateStatus(long id, PostStatus from, PostStatus to);

    // Imagen propia de la publicacion, sin caer en la portada del album.
    Optional<Long> findOwnImageId(long id);

    Optional<Long> findAlbumCoverImageId(long id);

    boolean delete(long id);
}
```
