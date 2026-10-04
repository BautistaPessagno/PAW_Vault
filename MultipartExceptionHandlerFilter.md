---
title: "MultipartExceptionHandlerFilter"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java"]
---

# MultipartExceptionHandlerFilter

Filtro que envuelve al multipart: si el request excede el tamaño máximo, redirige al formulario de origen con un aviso en lugar de un error 500.

## Guía de lectura

Datos y dependencias declaradas: `LOGGER`.

Operaciones para localizar en la fuente: `doFilterInternal`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: sin referencias léxicas desde otros archivos Java.

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/MultipartExceptionHandlerFilter.java>), líneas 1–50.

```java
package ar.edu.itba.paw.webapp.security;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.filter.OncePerRequestFilter;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public final class MultipartExceptionHandlerFilter extends OncePerRequestFilter {

    private static final Logger LOGGER = LoggerFactory.getLogger(MultipartExceptionHandlerFilter.class);

    @Override
    protected void doFilterInternal(final HttpServletRequest request, final HttpServletResponse response,
                                    final FilterChain filterChain) throws ServletException, IOException {
        try {
            filterChain.doFilter(request, response);
        } catch (final ServletException | RuntimeException exception) {
            /*
             * El resolver multipart parsea de forma lazy, asi que el limite excedido puede
             * saltar dentro del DispatcherServlet y llegar aca envuelto en una
             * NestedServletException. Por eso tambien se mira la causa directa.
             */
            if (!(exception instanceof MaxUploadSizeExceededException)
                    && !(exception.getCause() instanceof MaxUploadSizeExceededException)) {
                throw exception;
            }
            LOGGER.warn("Rejected a multipart request over the size limit uri={}", request.getRequestURI());
            final String servletPath = request.getServletPath();
            // El comprobante vuelve a la pagina de la Venta, que muestra el aviso.
            if (servletPath.matches("/inquiries/[0-9]+/receipt")) {
                final String salePath = servletPath.substring(0, servletPath.length() - "/receipt".length());
                response.sendRedirect(request.getContextPath() + salePath + "?receiptTooLarge");
                return;
            }
            // La foto de perfil vuelve al perfil, que reabre el dialogo con el aviso.
            if ("/profile/avatar".equals(servletPath)) {
                response.sendRedirect(request.getContextPath() + "/profile?avatarTooLarge#avatar");
                return;
            }
            final String target = servletPath.matches("/post/[0-9]+/edit") ? servletPath : "/publish";
            response.sendRedirect(request.getContextPath() + target + "?coverTooLarge");
        }
    }
}
```
