---
title: "TransactionCallbacks"
categories: ["Services"]
type: "code"
module: "services"
project: "quieroVinilos"
snapshot: "2026-09-22"
commit: "f12af080cf6a27101160f005102a20f436574cf7"
status: "documented"
sources: ["services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java"]
---

# TransactionCallbacks

Package-private helper that defers an action until the surrounding Spring transaction commits, or runs it immediately when no synchronization is active. Services use it to log and send mail only after commit, so a rolled-back write no longer triggers a notification.

## Connections

Project types referenced: none.

Referenced by: [[InquiryServiceImpl]], [[UserServiceImpl]].

## Exact source

[services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java, lines 1–24](<file:///Users/bautistapessagno/Desktop/ITBA/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/TransactionCallbacks.java>)

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

## Context

[[Architecture]] · [[Source inventory]] · [[Testing and evidence]]
