---
title: "PasswordResetToken"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java"]
---

# PasswordResetToken

Fila de `password_reset_tokens`: id, Cuenta, token y vencimiento. Un solo enlace vivo por Cuenta. Ver [[Tokens and email links]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `userId`, `token`, `expiresAt`.

Operaciones para localizar en la fuente: `getId`, `getUserId`, `getToken`, `getExpiresAt`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PasswordResetTokenDao]], [[PasswordResetTokenJdbcDao]], [[PasswordResetTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PasswordResetToken.java>), líneas 1–36.

```java
package ar.edu.itba.paw.models;

import java.time.LocalDateTime;

public final class PasswordResetToken {

    private final long id;
    private final long userId;
    private final String token;
    private final LocalDateTime expiresAt;

    public PasswordResetToken(final long id, final long userId, final String token,
                              final LocalDateTime expiresAt) {
        this.id = id;
        this.userId = userId;
        this.token = token;
        this.expiresAt = expiresAt;
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

    public LocalDateTime getExpiresAt() {
        return expiresAt;
    }

}
```
