---
title: "Edit and delete flow"
categories: ["Flows", "Web", "Services", "Persistence"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java", "services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java", "models/src/main/java/ar/edu/itba/paw/models/PostDetail.java", "webapp/src/main/webapp/js/confirm-action.js"]
---

# Edit and delete flow

> [!summary] En una frase
> El publicante, o un administrador, edita o elimina una publicación mientras siga disponible; eliminar no borra las consultas: las desengancha del post y rechaza las pendientes.

## Qué resuelve

`GET` y `POST /post/{id}/edit` y `POST /post/{id}/delete`. Con el PR #46 un administrador también modera publicaciones ajenas, en reemplazo del panel `/admin` eliminado.

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| `@PreAuthorize` con `hasRole('ADMIN') or @postAccess.isPublisher(...)` | Quién puede editar o eliminar |
| `SELECT ... FOR UPDATE` | Que la edición o el borrado no se crucen con una consulta o una venta |
| `ON DELETE CASCADE` en `post_images` | Las filas de la galería se van con el post |
| `UPDATE` de desenganche | Conservar las consultas de un post eliminado |
| `confirm-action.js` + `ui:confirm-dialog` | Confirmación antes de eliminar |
| Mismo formulario y validador que publicar | [[PublishForm]], [[PublishFormValidator]] |

## Recorrido paso a paso

### Editar

1. `GET /post/{id}/edit`: `VERIFIED` por URL y `CAN_MODERATE_POST` por recurso. `findEditableById` exige `AVAILABLE`; si no, 409. El formulario se precarga con los datos actuales; la vista recibe las fotos propias y la portada de respaldo del álbum.
2. `POST /post/{id}/edit` → `PostServiceImpl.update`:
   - Reglas numéricas.
   - `findByIdForUpdate` bloquea el post y exige `AVAILABLE`.
   - Las fotos a quitar (`removedImageIds`) tienen que ser fotos propias de ese post; si no, `InvalidImageException`.
   - El tope de 5 cuenta las que se conservan más las nuevas. El validador del formulario no puede saberlo; por eso lo informa el service y el controller lo muestra en el campo.
   - `resolveForEdit` de artista y álbum: busca o crea por identidad y, si el nombre visible o el género difieren, **actualiza el registro compartido**.
   - Crea las fotos nuevas, actualiza el post (con `image_id` si cambió la galería), reemplaza `post_images` y borra las imágenes retiradas.
3. Éxito: aviso `postUpdated` y redirección a la ficha.

### Eliminar

`POST /post/{id}/delete` → `PostServiceImpl.delete`:

1. Bloquea el post y exige `AVAILABLE`.
2. Lee los ids de sus fotos propias.
3. `inquiryDao.detachFromPost`: en un `UPDATE`, cada consulta copia `album_id` y `seller_id` del post, pone `post_id = NULL` y, si estaba `PENDING`, pasa a `REJECTED`.
4. Borra el post. Las filas de `post_images` se van por `ON DELETE CASCADE`.
5. Borra las imágenes (cada borrado solo procede si nada más la referencia).
6. Loguea cuántas consultas desenganchó y cuántas imágenes borró.

El controller redirige a `/profile#posts`, o a `/` si quien eliminó es administrador.

## Decisiones y por qué

| Decisión | Alternativa | Motivo | Fuente |
|---|---|---|---|
| Solo se edita o elimina lo `AVAILABLE` | Permitirlo siempre | "Un ejemplar vendido es el registro de la compra"; uno reservado tiene una venta en curso | Comentario en [[PostServiceImpl]] |
| Las consultas sobreviven desenganchadas | Borrarlas en cascada | El comprador sigue viendo qué preguntó y que la publicación ya no existe | Comentario en [[PostServiceImpl]]; migración V1 |
| Desenganchar antes de borrar | Borrar primero | Hay FK de `inquiries.post_id` a `posts` | Orden en `delete` |
| Borrar imágenes después del post | Antes | Las referencias tienen que desaparecer primero | Comentario en [[PostServiceImpl]] |
| La portada del álbum no se borra | Borrarla con el post | "Es del álbum y queda" | Comentario en [[PostServiceImpl]] |
| Pertenencia en `@PreAuthorize`, estado en el service | Las dos cosas en el service | Regla por capa del PR #43 y #46 | Comentario en [[PostService]] |
| El administrador modera desde la ficha | Panel `/admin` | El panel estaba vacío; se quitó | Commits `60480b55`, `e462c468` |
| Un post inexistente pasa el handler | Devolver `false` | Que el service responda 404 y no un 403 engañoso | Comentario en [[PostAccessHandler]] |

## Concurrencia y casos borde

- Editar mientras alguien consulta: los dos bloquean el post y se ordenan.
- Eliminar mientras el publicante acepta una consulta desde otra pestaña: quien llegue segundo ve el post reservado (409) o inexistente (404 o 409).
- Quitar todas las fotos: el post queda sin imagen propia y se muestra la portada heredada o el placeholder.
- `removedImageIds` con un id que no es una foto propia del post: `InvalidImageException`, que el controller muestra como error del campo de fotos.

## Límites conocidos

- **Editar reescribe datos compartidos.** `resolveForEdit` cambia el nombre visible del artista y el título o género del álbum, que también usan publicaciones de otras Cuentas.
- **La pertenencia no se vuelve a chequear en el service** (ver [[Security and authorization]]).
- Eliminar rechaza las consultas pendientes **sin correo** a esos compradores.
- No hay historial de cambios de una publicación.

## Preguntas de defensa

**¿Qué pasa con las consultas si borro la publicación?**
Quedan en la bandeja del comprador con el álbum y el vendedor copiados; las pendientes pasan a rechazadas.

**¿Por qué no puedo editar una publicación reservada?**
Porque hay una venta en curso con un precio y un ejemplar pactados. Solo se toca lo que sigue disponible.

**¿Cómo modera un administrador?**
La misma expresión de `@PreAuthorize` lo deja pasar por rol; la ficha le muestra los botones (`PostDetail.isEditable`).

**¿Qué diferencia hay entre 403, 404 y 409 acá?**
403 si no es tuya ni sos administrador; 404 si no existe; 409 si existe y es tuya pero ya no está disponible.

## Evidencia de código

Expresión de moderación y endpoint de borrado:

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>), líneas 38–40.

```java
    // Editar y eliminar: el Publicante o un administrador. Que el post siga a la venta lo exige el service.
    private static final String CAN_MODERATE_POST =
            "hasRole('ADMIN') or @postAccess.isPublisher(authentication, #postId)";
```

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>), líneas 115–154.

```java
    /*
     * El validador revisa las fotos nuevas una por una; el tope de la galeria cuenta tambien las
     * que se conservan, y eso lo sabe recien PostService: lo informa con InvalidImageException.
     */
    @PreAuthorize(CAN_MODERATE_POST)
    @RequestMapping(value = "/post/{postId:[0-9]+}/edit", method = RequestMethod.POST)
    public ModelAndView edit(@PathVariable("postId") final long postId,
                             @Valid @ModelAttribute("publishForm") final PublishForm form,
                             final BindingResult bindingResult,
                             final RedirectAttributes redirectAttributes) throws IOException {
        if (bindingResult.hasErrors()) {
            return editView(postId);
        }

        try {
            postService.update(postId, form.getTitle(), form.getArtistName(),
                    form.getReleaseYear(), form.getGenre(), form.getPrice(), form.getDescription(),
                    form.getCondition(), form.getPressingYear(), form.getZone(),
                    form.toImageUploads(), form.getRemovedImageIds());
            redirectAttributes.addFlashAttribute("postUpdated", true);
            return new ModelAndView("redirect:/post/" + postId);
        } catch (final InvalidImageException e) {
            bindingResult.rejectValue("covers", "publish.cover.invalid");
        } catch (final DuplicatePostException e) {
            bindingResult.reject("publish.duplicate");
        } catch (final ConcurrentPublishException e) {
            bindingResult.reject("publish.concurrent");
        }
        return editView(postId);
    }

    @PreAuthorize(CAN_MODERATE_POST)
    @RequestMapping(value = "/post/{postId:[0-9]+}/delete", method = RequestMethod.POST)
    public ModelAndView delete(@PathVariable("postId") final long postId,
                               @AuthenticationPrincipal final AuthenticatedUser currentUser,
                               final RedirectAttributes redirectAttributes) {
        postService.delete(postId);
        redirectAttributes.addFlashAttribute("postDeleted", true);
        return new ModelAndView(currentUser.isAdmin() ? "redirect:/" : "redirect:/profile#posts");
    }
```

Edición:

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 270–316.

```java
    @Override
    @Transactional
    public PostSummary update(final long postId, final String title,
                              final String artistName, final int releaseYear, final Genre genre, final int price,
                              final String description, final Condition condition, final Integer pressingYear,
                              final String zone, final List<ImageUpload> images,
                              final List<Long> removedImageIds) {
        requireValidPostData(releaseYear, price, pressingYear);
        requireAvailable(postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new));
        final List<Long> oldImageIds = findUploadedImageIds(postId);
        final Set<Long> removed = removedImageIds == null ? Set.of() : new HashSet<>(removedImageIds);
        if (!oldImageIds.containsAll(removed)) {
            throw new InvalidImageException();
        }
        final List<Long> imageIds = new ArrayList<>();
        for (final Long imageId : oldImageIds) {
            if (!removed.contains(imageId)) {
                imageIds.add(imageId);
            }
        }
        requireGallerySize(imageIds.size() + (images == null ? 0 : images.size()));
        try {
            final Artist artist = artistService.resolveForEdit(artistName);
            final Album album = albumService.resolveForEdit(title, artist.getId(), releaseYear, genre);
            imageIds.addAll(createImages(images));
            final boolean galleryChanged = !removed.isEmpty() || images != null && !images.isEmpty();
            final boolean updated = galleryChanged
                    ? postDao.updateWithImage(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone), imageIds.isEmpty() ? null : imageIds.get(0))
                    : postDao.update(postId, album.getId(), price, blankToNull(description), condition,
                            pressingYear, blankToNull(zone));
            if (!updated) {
                throw new PostNotFoundException();
            }
            if (galleryChanged) {
                imageService.replaceGallery(postId, extrasOf(imageIds));
                for (final Long removedId : removed) {
                    imageService.delete(removedId);
                }
            }
            return postDao.findById(postId).orElseThrow(PostNotFoundException::new);
        } catch (final DuplicatePostKeyException e) {
            throw new DuplicatePostException();
        } catch (final DataIntegrityViolationException e) {
            throw new ConcurrentPublishException();
        }
    }
```

Borrado:

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>), líneas 318–338.

```java
    // Solo se elimina lo que todavia esta a la venta: un ejemplar vendido es el registro de
    // la compra. Las consultas sobreviven desenganchadas del post para que el comprador
    // siga viendo que pregunto y que la publicacion ya no existe. La foto propia de la
    // publicacion se va con ella; la portada del album es del album y queda.
    @Override
    @Transactional
    public int delete(final long postId) {
        requireAvailable(postDao.findByIdForUpdate(postId).orElseThrow(PostNotFoundException::new));
        final List<Long> uploadedImageIds = findUploadedImageIds(postId);
        final int detached = inquiryDao.detachFromPost(postId);
        if (!postDao.delete(postId)) {
            throw new PostNotFoundException();
        }
        // Las filas de la galeria se van con el post (ON DELETE CASCADE): recien ahi se pueden borrar las fotos.
        for (final Long imageId : uploadedImageIds) {
            imageService.delete(imageId);
        }
        LOGGER.info("Deleted post postId={} detachedInquiries={} deletedImages={}",
                postId, detached, uploadedImageIds.size());
        return detached;
    }
```

Desenganche de consultas:

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>), líneas 362–372.

```java
    // Antes de borrar la publicacion, cada consulta se queda con su album y su vendedor y
    // deja de apuntar al post. Las pendientes se cierran: ya no hay nada que aceptar.
    @Override
    public int detachFromPost(final long postId) {
        return jdbcTemplate.update("UPDATE inquiries SET "
                        + "album_id = (SELECT album_id FROM posts WHERE id = inquiries.post_id), "
                        + "seller_id = (SELECT user_id FROM posts WHERE id = inquiries.post_id), "
                        + "post_id = NULL, status = CASE WHEN status = ? THEN ? ELSE status END "
                        + "WHERE post_id = ?",
                InquiryStatus.PENDING.name(), InquiryStatus.REJECTED.name(), postId);
    }
```

Handler de pertenencia:

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java>), líneas 6–23.

```java
// Regla de @PreAuthorize para editar y eliminar una publicacion; el administrador entra por su rol
// en la misma expresion. Un post inexistente pasa: el service responde 404 en vez de un 403 enganioso.
public final class PostAccessHandler {

    private final PostService postService;

    public PostAccessHandler(final PostService postService) {
        this.postService = postService;
    }

    public boolean isPublisher(final Authentication authentication, final long postId) {
        return AuthenticatedUser.idOf(authentication)
                .map(userId -> postService.findPublisherId(postId)
                        .map(userId::equals)
                        .orElse(true))
                .orElse(false);
    }
}
```

Reescritura de datos compartidos:

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>), líneas 31–42.

```java
    @Override
    @Transactional
    public Album resolveForEdit(final String title, final long artistId, final int releaseYear,
                                final Genre genre) {
        final String trimmedTitle = title.trim();
        final Album album = albumDao.findByArtistTitleYear(trimmedTitle, artistId, releaseYear)
                .orElseGet(() -> albumDao.create(trimmedTitle, artistId, releaseYear, genre));
        if (album.getTitle().equals(trimmedTitle) && album.getGenre() == genre) {
            return album;
        }
        return albumDao.updateMetadata(album.getId(), trimmedTitle, genre);
    }
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublishController.java>) · [[PublishController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/PostAccessHandler.java>) · [[PostAccessHandler]]
- [services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PostServiceImpl.java>) · [[PostServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ArtistServiceImpl.java>) · [[ArtistServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java>) · [[AlbumServiceImpl]]
- [services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java>) · [[ImageServiceImpl]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/PostJdbcDao.java>) · [[PostJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/InquiryJdbcDao.java>) · [[InquiryJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>) · [[ImageJdbcDao]]
- [models/src/main/java/ar/edu/itba/paw/models/PostDetail.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostDetail.java>) · [[PostDetail]]
- [webapp/src/main/webapp/js/confirm-action.js](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/js/confirm-action.js>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
