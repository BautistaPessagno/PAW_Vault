---
title: "AuthenticationSessions"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java"]
---

# AuthenticationSessions

Tres operaciones sobre la sesión: iniciar sesión sin pasar por el login (registro), refrescar el principal (verificación, cambio de nombre) y cerrar todas las sesiones de una Cuenta (cambio o recuperación de clave).

## Guía de lectura

Datos y dependencias declaradas: `CONTEXT_REPOSITORY`, `LOGOUT_HANDLER`.

Operaciones para localizar en la fuente: `login`, `logoutEverywhere`, `refreshIfCurrent`, `currentUser`, `authenticationFor`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[User]].

Referenciado por: [[AuthenticationController]], [[ProfileController]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/AuthenticationSessions.java>), líneas 1–91.

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.models.User;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.session.SessionInformation;
import org.springframework.security.core.session.SessionRegistry;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.security.web.context.SecurityContextRepository;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.util.Optional;

/*
 * Reemplaza el principal de la sesion cuando cambia algo de la cuenta que la cabecera o
 * SecurityConfig necesitan ver en el mismo request: el registro, la verificacion o el
 * nombre de usuario. Tambien cierra las sesiones de la cuenta cuando cambia la clave.
 */
public final class AuthenticationSessions {

    private static final SecurityContextRepository CONTEXT_REPOSITORY = new HttpSessionSecurityContextRepository();
    private static final SecurityContextLogoutHandler LOGOUT_HANDLER = new SecurityContextLogoutHandler();

    private AuthenticationSessions() {
    }

    // Inicia sesion sin pedir la clave, recien elegida en el mismo formulario.
    public static void login(final User user, final HttpServletRequest request, final HttpServletResponse response,
                             final SessionRegistry sessionRegistry) {
        // Un id de sesion nuevo al autenticarse evita que alguien que fijo la cookie antes
        // quede adentro de la cuenta.
        if (request.getSession(false) != null) {
            request.changeSessionId();
        }
        final SecurityContext context = SecurityContextHolder.createEmptyContext();
        final Authentication authentication = authenticationFor(user, null);
        context.setAuthentication(authentication);
        SecurityContextHolder.setContext(context);
        CONTEXT_REPOSITORY.saveContext(context, request, response);
        // El form login registra la sesion solo; esta no pasa por el, asi que se registra aca
        // para poder expirarla si despues cambia la clave.
        sessionRegistry.registerNewSession(request.getSession().getId(), authentication.getPrincipal());
    }

    /*
     * Despues de cambiar o restablecer la clave: expira las otras sesiones de la cuenta y, si
     * este navegador tenia una, la cierra. Sin esto, una sesion iniciada por quien registro el
     * correo antes que su dueno seguiria adentro despues de que el dueno recupere la cuenta.
     */
    public static void logoutEverywhere(final User user, final HttpServletRequest request,
                                        final HttpServletResponse response, final SessionRegistry sessionRegistry) {
        final HttpSession currentSession = request.getSession(false);
        final String currentSessionId = currentSession == null ? null : currentSession.getId();
        sessionRegistry.getAllSessions(new AuthenticatedUser(user), false).stream()
                .filter(session -> !session.getSessionId().equals(currentSessionId))
                .forEach(SessionInformation::expireNow);
        if (currentUser().filter(current -> current.getId() == user.getId()).isPresent()) {
            LOGOUT_HANDLER.logout(request, response, SecurityContextHolder.getContext().getAuthentication());
        }
    }

    // Solo si la sesion ya es de esa cuenta: un enlace abierto en otro navegador no inicia sesion.
    public static void refreshIfCurrent(final User user) {
        currentUser().filter(current -> current.getId() == user.getId()).ifPresent(current -> {
            final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            SecurityContextHolder.getContext().setAuthentication(
                    authenticationFor(user, authentication.getDetails()));
        });
    }

    private static Optional<AuthenticatedUser> currentUser() {
        final Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null && authentication.getPrincipal() instanceof AuthenticatedUser) {
            return Optional.of((AuthenticatedUser) authentication.getPrincipal());
        }
        return Optional.empty();
    }

    private static Authentication authenticationFor(final User user, final Object details) {
        final AuthenticatedUser principal = new AuthenticatedUser(user);
        final UsernamePasswordAuthenticationToken authentication = new UsernamePasswordAuthenticationToken(
                principal, null, principal.getAuthorities());
        authentication.setDetails(details);
        return authentication;
    }
}
```
