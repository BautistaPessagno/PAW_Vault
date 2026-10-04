---
title: "TransactionCallbacks"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java"]
---

# TransactionCallbacks

Difiere una acción hasta después del commit de la transacción en curso; sin transacción la ejecuta en el momento. Lo usan todos los envíos de correo. Ver [[Mail delivery]].

## Guía de lectura

Operaciones para localizar en la fuente: `afterCommit`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[InquiryServiceImpl]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>), líneas 1–24.

```java
package ar.edu.itba.paw.services;

import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;

final class TransactionCallbacks {

    private TransactionCallbacks() {
        throw new AssertionError("No instances");
    }

    static void afterCommit(final Runnable action) {
        if (!TransactionSynchronizationManager.isSynchronizationActive()) {
            action.run();
            return;
        }
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
            @Override
            public void afterCommit() {
                action.run();
            }
        });
    }
}
```
