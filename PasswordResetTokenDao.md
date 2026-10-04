---
title: "PasswordResetTokenDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java"]
---

# PasswordResetTokenDao

Contrato de los tokens de recuperación: crear con vencimiento, buscar, borrar por token, borrar por Cuenta y purgar vencidos. Ver [[Tokens and email links]].

## Guía de lectura

Operaciones para localizar en la fuente: `create`, `findByToken`, `deleteByToken`, `deleteByUserId`, `deleteExpired`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PasswordResetToken]].

Referenciado por: [[PasswordResetTokenJdbcDao]], [[PasswordResetTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/PasswordResetTokenDao.java>), líneas 1–20.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PasswordResetToken;

import java.time.LocalDateTime;
import java.util.Optional;

public interface PasswordResetTokenDao {

    PasswordResetToken create(long userId, String token, LocalDateTime expiresAt);

    Optional<PasswordResetToken> findByToken(String token);

    int deleteByToken(String token);

    int deleteByUserId(long userId);

    int deleteExpired(LocalDateTime now);

}
```
