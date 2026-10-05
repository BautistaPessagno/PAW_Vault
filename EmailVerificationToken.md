---
title: "EmailVerificationToken"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java"]
---

# EmailVerificationToken

Fila de `email_verification_tokens`: id, Cuenta, token y fecha de emisión. La fecha sirve para el tope de un minuto entre reenvíos. No tiene vencimiento. Ver [[Tokens and email links]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `userId`, `token`, `createdAt`.

Operaciones para localizar en la fuente: `getId`, `getUserId`, `getToken`, `getCreatedAt`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[EmailVerificationTokenDao]], [[EmailVerificationTokenJdbcDao]], [[EmailVerificationTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailVerificationToken.java>), líneas 1–36.

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;

public final class EmailVerificationToken {

    private final long id;
    private final long userId;
    private final String token;
    private final LocalDateTime createdAt;

    public EmailVerificationToken(final long id, final long userId, final String token,
                                  final LocalDateTime createdAt) {
        this.id = id;
        this.userId = userId;
        this.token = token;
        this.createdAt = createdAt;
    }

    public long getId() {
        return id;
    }

    public long getUserId() {
        return userId;
    }

    public String getToken() {
        return token;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

}
```
