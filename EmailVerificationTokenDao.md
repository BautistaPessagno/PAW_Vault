---
title: "EmailVerificationTokenDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java"]
---

# EmailVerificationTokenDao

Contrato de los tokens de verificación: crear con fecha, buscar por token, buscar el último de una Cuenta y borrar los de una Cuenta. Ver [[Tokens and email links]].

## Guía de lectura

Operaciones para localizar en la fuente: `create`, `findByToken`, `findLatestByUserId`, `deleteByUserId`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[EmailVerificationToken]].

Referenciado por: [[EmailVerificationTokenJdbcDao]], [[EmailVerificationTokenJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/EmailVerificationTokenDao.java>), líneas 1–18.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.EmailVerificationToken;

import java.time.LocalDateTime;
import java.util.Optional;

public interface EmailVerificationTokenDao {

    EmailVerificationToken create(long userId, String token, LocalDateTime createdAt);

    Optional<EmailVerificationToken> findByToken(String token);

    Optional<EmailVerificationToken> findLatestByUserId(long userId);

    int deleteByUserId(long userId);

}
```
