---
title: "ImageController"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-09-09"
commit: "ff96f275ae009bad4534751b7a4857cf45aea7ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java"]
---

# ImageController

GET /covers/{id} accepts decimal digits, loads [[Image]] through [[ImageService]] and returns its byte array with stored Content-Type and public max-age of 365 days. A missing image raises [[ImageNotFoundException]] and the local handler returns 404. There is no authentication, replacement route or ETag logic in this controller. See [[Cover image flow]].

## Connections

Project types referenced: [[Image]], [[ImageNotFoundException]], [[ImageService]].

Referenced by: no direct project type reference; implementations may be injected through interfaces.

## Exact source

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
