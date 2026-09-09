---
title: "Cover image flow"
categories: ["Flows", "Web"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java", "services/src/main/java/ar/edu/itba/paw/services/ImageServiceImpl.java", "services/src/main/java/ar/edu/itba/paw/services/AlbumServiceImpl.java"]
---

# Cover image flow

An optional cover belongs to an Album, not an individual Post. [[PublishForm]] receives MultipartFile through a lazy CommonsMultipartResolver. [[PublishController]] passes the declared MIME type and bytes to [[PostServiceImpl]], then [[AlbumServiceImpl]].

## Storage decisions

1. Existing artist/title/year identity returns the stored Album and ignores the submitted cover, even if the existing cover is null.
2. A new album with no bytes stores a null image reference.
3. A new album with bytes invokes [[ImageServiceImpl]]. It permits normalized image/png, image/jpeg and image/webp with 1–5,242,880 bytes.
4. [[ImageJdbcDao]] inserts content_type and BYTEA data and returns the generated ID. Album and Post writes join the same publish transaction.

Only the supplied MIME label and byte length are checked. There is no image decoder, signature validation, resizing or content deduplication. The HTML accept list is a file-picker hint. The whole multipart request limit is 6,291,456 bytes; excessive requests return an empty PublishForm with coverTooLarge.

## Retrieval

ui:vinyl-card renders /images/covers/placeholder.svg when coverImageId is null. Otherwise it renders /covers/{id}. [[ImageController]] loads the Image through a read-only service call and returns bytes with stored Content-Type and Cache-Control public, max-age=31536000. Missing IDs return 404. There is no replace/delete route, authentication or conditional ETag response in this controller.

An old album whose cover_path was removed by the startup script now displays the placeholder. A non-null dangling image ID instead requests a missing resource and gets 404; the JSP has no automatic fallback for that case. The startup schema does not enforce the image foreign key.

## Image response source

[webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java, lines 1–46](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>)

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

    @RequestMapping(value = "/covers/{id:\\d+}", method = RequestMethod.GET)
    public ResponseEntity<byte[]> cover(@PathVariable("id") final long id) {
        final Image image = imageService.findById(id).orElseThrow(ImageNotFoundException::new);
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

[[Database schema]] · [[UI components]] · [[ImageJdbcDaoTest]] · [[ImageServiceImplTest]]
