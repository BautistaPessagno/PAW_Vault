---
title: "EmailRules"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/EmailRules.java"]
---

# EmailRules

Una sola regla para guardar y buscar un correo: sin espacios y en minúsculas. La comparten [[UserServiceImpl]] y [[UserJdbcDao]], así el mismo correo escrito distinto es la misma Cuenta.

## Guía de lectura

Operaciones para localizar en la fuente: `normalize`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[UserJdbcDao]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/EmailRules.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/EmailRules.java>), líneas 1–15.

```java
package ar.edu.itba.paw.models;

import java.util.Locale;

// Como se guarda y se busca un correo, compartido por UserService y por UserDao.
public final class EmailRules {

    private EmailRules() {
    }

    // Sin espacios y en minusculas: el mismo correo escrito distinto es la misma Cuenta.
    public static String normalize(final String email) {
        return email.trim().toLowerCase(Locale.ROOT);
    }
}
```
