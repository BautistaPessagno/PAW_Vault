---
title: "VerificationAccessDeniedHandler"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java"]
---

# VerificationAccessDeniedHandler

Una Cuenta sin verificar que entra a una ruta de Cuenta verificada va a `/verify/required`; cualquier otra denegación sigue siendo 403.

## Guía de lectura

Datos y dependencias declaradas: `VERIFICATION_REQUIRED_PATH`, `verifiedPaths`, `forbiddenHandler`.

Operaciones para localizar en la fuente: `handle`, `isVerified`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]].

Referenciado por: [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/VerificationAccessDeniedHandler.java>), líneas 1–47.

```java
package ar.edu.itba.paw.webapp.security;

import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.security.web.access.AccessDeniedHandlerImpl;
import org.springframework.security.web.util.matcher.RequestMatcher;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/*
 * Una cuenta sin verificar que entra a una ruta de cuenta verificada llega a la pagina que
 * le explica que le falta y le deja reenviar el enlace. Cualquier otra denegacion, como la
 * administracion, sigue siendo el 403 de siempre: verificar no le daria acceso.
 */
public final class VerificationAccessDeniedHandler implements AccessDeniedHandler {

    private static final String VERIFICATION_REQUIRED_PATH = "/verify/required";

    private final RequestMatcher verifiedPaths;
    private final AccessDeniedHandlerImpl forbiddenHandler = new AccessDeniedHandlerImpl();

    public VerificationAccessDeniedHandler(final RequestMatcher verifiedPaths, final String forbiddenPage) {
        this.verifiedPaths = verifiedPaths;
        this.forbiddenHandler.setErrorPage(forbiddenPage);
    }

    @Override
    public void handle(final HttpServletRequest request, final HttpServletResponse response,
                       final AccessDeniedException exception) throws IOException, ServletException {
        if (verifiedPaths.matches(request) && !isVerified()) {
            response.sendRedirect(request.getContextPath() + VERIFICATION_REQUIRED_PATH);
            return;
        }
        forbiddenHandler.handle(request, response, exception);
    }

    private static boolean isVerified() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return authentication != null && authentication.getAuthorities().stream()
                .anyMatch(authority -> AuthenticatedUser.VERIFIED.equals(authority.getAuthority()));
    }
}
```
