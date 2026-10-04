---
title: "SameSiteRedirects"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java"]
---

# SameSiteRedirects

Convierte el header `Referer` en una ruta de regreso segura: mismo host, dentro del context path y sin `//` ni barra invertida. Evita una redirección abierta.

## Guía de lectura

Datos y dependencias declaradas: `HOME`.

Operaciones para localizar en la fuente: `pathOf`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[AuthenticationController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/SameSiteRedirects.java>), líneas 1–44.

```java
package ar.edu.itba.paw.webapp.security;

import javax.servlet.http.HttpServletRequest;
import java.net.URI;

/*
 * Volver a la pagina desde la que se envio un formulario. El Referer lo manda el navegador,
 * asi que solo se acepta si apunta a esta misma aplicacion: redirigir a cualquier otro sitio
 * abriria un open redirect. Cualquier otro caso vuelve al inicio.
 */
public final class SameSiteRedirects {

    private static final String HOME = "/";

    private SameSiteRedirects() {
    }

    // La ruta sin el context path, lista para "redirect:".
    public static String pathOf(final String referer, final HttpServletRequest request) {
        if (referer == null) {
            return HOME;
        }
        final URI uri;
        try {
            uri = URI.create(referer);
        } catch (final IllegalArgumentException e) {
            return HOME;
        }
        final String contextPath = request.getContextPath();
        final String path = uri.getRawPath();
        if (!request.getServerName().equalsIgnoreCase(uri.getHost()) || path == null
                || !path.startsWith(contextPath + "/")) {
            return HOME;
        }
        final String relativePath = path.substring(contextPath.length());
        // "//otro-sitio/x" y las variantes con "\" son relativas al protocolo: el navegador
        // las resolveria contra otro host aunque el Referer sea de este.
        if (relativePath.startsWith("//") || relativePath.contains("\\")) {
            return HOME;
        }
        final String query = uri.getRawQuery();
        return relativePath + (query == null ? "" : "?" + query);
    }
}
```
