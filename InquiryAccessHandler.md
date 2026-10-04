---
title: "InquiryAccessHandler"
categories: ["Web"]
type: "code"
module: "webapp"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java"]
---

# InquiryAccessHandler

Bean `inquiryAccess` de `@PreAuthorize`: comprador, publicante o cualquiera de las dos partes de una consulta. Una consulta inexistente pasa, para que el service responda 404.

## Guía de lectura

Datos y dependencias declaradas: `inquiryService`.

Operaciones para localizar en la fuente: `isBuyer`, `isSeller`, `isParty`, `allows`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[AuthenticatedUser]], [[InquiryParties]], [[InquiryService]].

Referenciado por: [[SecurityConfig]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/security/InquiryAccessHandler.java>), líneas 1–40.

```java
package ar.edu.itba.paw.webapp.security;

import ar.edu.itba.paw.models.InquiryParties;
import ar.edu.itba.paw.services.InquiryService;
import org.springframework.security.core.Authentication;

import java.util.function.BiPredicate;

// Reglas de @PreAuthorize para la Consulta y su Venta: ver, conversar y cancelar es de las dos
// partes, subir el comprobante es del comprador y revisarlo es del Publicante. Una consulta inexistente pasa:
// el handler llega al service, que responde 404 en vez de un 403 enganioso.
public final class InquiryAccessHandler {

    private final InquiryService inquiryService;

    public InquiryAccessHandler(final InquiryService inquiryService) {
        this.inquiryService = inquiryService;
    }

    public boolean isBuyer(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isBuyer);
    }

    public boolean isSeller(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isSeller);
    }

    public boolean isParty(final Authentication authentication, final long inquiryId) {
        return allows(authentication, inquiryId, InquiryParties::isParty);
    }

    private boolean allows(final Authentication authentication, final long inquiryId,
                           final BiPredicate<InquiryParties, Long> rule) {
        return AuthenticatedUser.idOf(authentication)
                .map(userId -> inquiryService.findParties(inquiryId)
                        .map(parties -> rule.test(parties, userId))
                        .orElse(true))
                .orElse(false);
    }
}
```
