---
title: "PostService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java"]
---

# PostService

Contrato de publicaciones: ficha, búsqueda paginada, sugerencias, listados por publicante (el privado con filtro opcional por [[PostStatus]] y sus conteos), alta, edición y borrado (estas dos reciben quién actúa), más las operaciones internas de la venta (`lockById`, `lockByIds`, `reserve`, `release`, `markSold`) que exigen una transacción abierta.

## Guía de lectura

Operaciones para localizar en la fuente: `findById`, `lockById`, `lockByIds`, `reserve`, `release`, `markSold`, `findDetail`, `findPublisherId`, `findEditableById`, `findUploadedImageIds`, `findAlbumCoverImageId`, `search`, `findSearchSuggestions`, `findByPublisherId`, `countByStatusForPublisher`, `findAvailableByPublisherId`, `publish`, `update`, `delete`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Condition]], [[FilterCounts]], [[Genre]], [[ImageUpload]], [[Post]], [[PostDetail]], [[PostPage]], [[PostSearchCriteria]], [[PostStatus]], [[PostSummary]], [[SearchResult]], [[SearchSuggestion]].

Referenciado por: [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[LandingController]], [[PostAccessHandler]], [[PostServiceImpl]], [[ProfileController]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]], [[PublishController]], [[SearchSuggestionController]], [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PostService.java>), líneas 1–85.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.Condition;
import ar.edu.itba.paw.models.FilterCounts;
import ar.edu.itba.paw.models.Genre;
import ar.edu.itba.paw.models.ImageUpload;
import ar.edu.itba.paw.models.Post;
import ar.edu.itba.paw.models.PostDetail;
import ar.edu.itba.paw.models.PostPage;
import ar.edu.itba.paw.models.PostSearchCriteria;
import ar.edu.itba.paw.models.PostStatus;
import ar.edu.itba.paw.models.PostSummary;
import ar.edu.itba.paw.models.SearchResult;
import ar.edu.itba.paw.models.SearchSuggestion;

import java.util.Collection;
import java.util.List;
import java.util.Optional;

public interface PostService {

    PostSummary findById(long postId);

    // Bloquea la fila del post dentro de la transaccion del llamador: las consultas del mismo
    // ejemplar compiten por ella y se ordenan entre si.
    PostSummary lockById(long postId);

    // lockById para varios posts a la vez, en orden de id. Omite los que no existen.
    List<PostSummary> lockByIds(Collection<Long> postIds);

    /*
     * Internas de la venta: solo InquiryService las llama, dentro de su transaccion y despues de
     * bloquear el post con lockById y de chequear quien pide la transicion. No reciben actor
     * ni validan permisos; cada una devuelve false si el post no estaba en el estado de origen.
     */
    boolean reserve(long postId);

    boolean release(long postId);

    boolean markSold(long postId);

    // La ficha publica para quien mira: viewerId es null sin sesion, y moderator lo resuelve la
    // capa web a partir del rol. La galeria incluye la portada del album solo si el post no tiene
    // fotos propias.
    PostDetail findDetail(long postId, Long viewerId, boolean moderator);

    // Para PostAccessHandler: el Publicante, sin decidir nada. Vacio si el post no existe.
    Optional<Long> findPublisherId(long postId);

    /*
     * Editar y eliminar: quien puede hacerlo (el Publicante o un moderador) lo decide
     * @postAccess en la capa web y el service con actorId. El service comprueba pertenencia
     * o rol ADMIN antes de exigir que el post siga a la venta.
     */
    PostSummary findEditableById(long postId, long actorId);

    // Imagenes propias del post, para mostrar controles de retiro durante la edicion.
    List<Long> findUploadedImageIds(long postId);

    Optional<Long> findAlbumCoverImageId(long postId);

    SearchResult search(PostSearchCriteria criteria, int pageNumber);

    List<SearchSuggestion> findSearchSuggestions(String query);

    // status null trae los Posts en cualquier estado.
    PostPage findByPublisherId(long publisherId, PostStatus status, int pageNumber);

    // Los numeros de los chips de filtro de "Mis publicaciones".
    FilterCounts<PostStatus> countByStatusForPublisher(long publisherId);

    PostPage findAvailableByPublisherId(long publisherId, int pageNumber);

    Post publish(long publisherId, String title, String artistName, int releaseYear,
                 Genre genre, int price, String description, Condition condition, Integer pressingYear,
                 String zone, List<ImageUpload> images);

    PostSummary update(long postId, long actorId, String title, String artistName, int releaseYear,
                       Genre genre, int price, String description, Condition condition, Integer pressingYear,
                       String zone, List<ImageUpload> images, List<Long> removedImageIds);

    // Devuelve cuantas consultas quedaron desenganchadas de la publicacion eliminada.
    int delete(long postId, long actorId);

}
```
