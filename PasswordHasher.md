---
title: "PasswordHasher"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java"]
---

# PasswordHasher

Hashear y comparar contraseñas sin que `services` dependa de Spring Security. El adaptador sobre BCrypt está en [[SecurityConfig]].

## Guía de lectura

Operaciones para localizar en la fuente: `hash`, `matches`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[SecurityConfig]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PasswordHasher.java>), líneas 1–7.

```java
package ar.edu.itba.paw.services;

public interface PasswordHasher {
    String hash(String rawPassword);

    boolean matches(String rawPassword, String passwordHash);
}
```
