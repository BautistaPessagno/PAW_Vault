---
title: "ImageController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java"]
---

# ImageController

Sirve imágenes desde el recurso al que pertenecen (post, usuario, álbum) con caché de un año; 404 sin cuerpo si no corresponde. Ver [[Cover image flow]].

## Guía de lectura

Datos y dependencias declaradas: `CACHE_DAYS`, `imageService`.

Operaciones para localizar en la fuente: `postImage`, `userAvatar`, `albumCover`, `imageResponse`, `imageNotFound`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[Image]], [[ImageNotFoundException]], [[ImageService]].

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>), líneas 1–62.

```java
package ar.edu.itba.paw.webapp.controller;

import ar.edu.itba.paw.models.Image;
import ar.edu.itba.paw.services.ImageService;
import ar.edu.itba.paw.webapp.exceptions.ImageNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.util.concurrent.TimeUnit;

@Controller
public class ImageController {

    // Una imagen nunca cambia una vez guardada, asi que el navegador puede cachearla por id.
    private static final long CACHE_DAYS = 365;

    private final ImageService imageService;

    @Autowired
    public ImageController(final ImageService imageService) {
        this.imageService = imageService;
    }

    @RequestMapping(value = "/post/{postId:\\d+}/images/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> postImage(@PathVariable("postId") final long postId,
                                           @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findPostImage(postId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    @RequestMapping(value = "/users/{userId:\\d+}/avatar/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> userAvatar(@PathVariable("userId") final long userId,
                                            @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findUserAvatar(userId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    @RequestMapping(value = "/albums/{albumId:\\d+}/cover/{imageId:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> albumCover(@PathVariable("albumId") final long albumId,
                                            @PathVariable("imageId") final long imageId) {
        return imageResponse(imageService.findAlbumCover(albumId, imageId).orElseThrow(ImageNotFoundException::new));
    }

    private static ResponseEntity<byte[]> imageResponse(final Image image) {
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(image.getContentType()))
                .cacheControl(CacheControl.maxAge(CACHE_DAYS, TimeUnit.DAYS).cachePublic())
                .body(image.getData());
    }

    @ExceptionHandler(ImageNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public void imageNotFound() {
    }
}
```
