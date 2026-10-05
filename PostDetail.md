---
title: "PostDetail"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PostDetail.java"]
---

# PostDetail

La ficha de una publicación para quien la mira: resumen, perfil público del vendedor (nulo si no está verificado), fotos y si puede editarla (`isEditable`: disponible y propia o moderador). Si puede consultarla lo decide [[PostContactOptions]].

## Guía de lectura

Datos y dependencias declaradas: `post`, `seller`, `galleryImageIds`, `ownedByViewer`, `moderator`.

Operaciones para localizar en la fuente: `getPost`, `getSeller`, `getGalleryImageIds`, `isOwnedByViewer`, `isEditable`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PostStatus]], [[PostSummary]], [[PublicUserProfile]].

Referenciado por: [[CartServiceImpl]], [[CartServiceImplTest]], [[PostController]], [[PostService]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PostView]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/PostDetail.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PostDetail.java>), líneas 1–41.

```java
package ar.edu.itba.paw.models;

import java.util.List;

/*
 * La ficha de una publicacion vista por alguien, con o sin sesion. Decide si quien mira puede
 * editarla: PostService usa la misma regla de estado antes de editar o eliminar, y el rol de
 * moderador lo resuelve la capa web. Si puede consultarla lo decide CartService (PostView).
 */
public final class PostDetail {

    private final PostSummary post;
    private final PublicUserProfile seller;
    private final List<Long> galleryImageIds;
    private final boolean ownedByViewer;
    private final boolean moderator;

    // seller es null si el Publicante ya no tiene perfil publico.
    public PostDetail(final PostSummary post, final PublicUserProfile seller, final List<Long> galleryImageIds,
                      final boolean ownedByViewer, final boolean moderator) {
        this.post = post;
        this.seller = seller;
        this.galleryImageIds = List.copyOf(galleryImageIds);
        this.ownedByViewer = ownedByViewer;
        this.moderator = moderator;
    }

    public PostSummary getPost() { return post; }

    public PublicUserProfile getSeller() { return seller; }

    // La portada primero y despues las fotos adicionales, en orden.
    public List<Long> getGalleryImageIds() { return galleryImageIds; }

    public boolean isOwnedByViewer() { return ownedByViewer; }

    // Solo se edita o elimina lo que sigue a la venta, y solo su Publicante o un moderador.
    public boolean isEditable() {
        return post.getStatus() == PostStatus.AVAILABLE && (ownedByViewer || moderator);
    }
}
```
