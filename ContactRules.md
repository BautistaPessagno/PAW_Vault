---
title: "ContactRules"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/ContactRules.java"]
---

# ContactRules

La única definición de "se puede consultar": disponible, ajeno y sin una Consulta abierta del comprador. La leen el contacto, el carrito y la ficha, y el carrito le pasa sus constantes al DAO para filtrar en SQL.

## Guía de lectura

Datos y dependencias declaradas: `CONTACTABLE_POST_STATUS`, `BLOCKING_INQUIRY_STATUSES`.

Operaciones para localizar en la fuente: `stateOf`, `stateForAnonymous`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ContactState]], [[InquiryStatus]], [[PostStatus]].

Referenciado por: [[CartServiceImpl]], [[ContactRulesTest]], [[InquiryServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services/src/main/java/ar/edu/itba/paw/services/ContactRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/ContactRules.java>), líneas 1–44.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.ContactState;
import ar.edu.itba.paw.models.InquiryStatus;
import ar.edu.itba.paw.models.PostStatus;

import java.util.List;

/*
 * La unica definicion de "se puede consultar": disponible, ajeno y sin una Consulta abierta
 * del comprador. El contacto, el carrito y la ficha la leen de aca; el carrito le pasa a su DAO
 * estas mismas constantes para filtrar en la base. Lo ajeno no hace falta filtrarlo ahi: add()
 * nunca deja entrar un Post propio.
 */
final class ContactRules {

    static final PostStatus CONTACTABLE_POST_STATUS = PostStatus.AVAILABLE;

    static final List<InquiryStatus> BLOCKING_INQUIRY_STATUSES = InquiryStatus.OPEN_STATUSES;

    private ContactRules() {
    }

    // Una Consulta abierta gana: el comprador tiene que llegar a su Conversacion aunque el
    // post ya este reservado para el.
    static ContactState stateOf(final PostStatus postStatus, final long sellerId, final long buyerId,
                                final boolean hasOpenInquiry) {
        if (hasOpenInquiry) {
            return ContactState.OPEN_INQUIRY;
        }
        if (stateForAnonymous(postStatus) == ContactState.UNAVAILABLE) {
            return ContactState.UNAVAILABLE;
        }
        if (sellerId == buyerId) {
            return ContactState.OWN_POST;
        }
        return ContactState.CONTACTABLE;
    }

    // Sin sesion no hay Consulta abierta ni post propio: solo cuenta el estado del post.
    static ContactState stateForAnonymous(final PostStatus postStatus) {
        return postStatus == CONTACTABLE_POST_STATUS ? ContactState.CONTACTABLE : ContactState.UNAVAILABLE;
    }
}
```
