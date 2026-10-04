---
title: "UserDao"
categories: ["Persistence"]
type: "code"
module: "persistence-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java"]
---

# UserDao

Contrato de Cuentas: buscar por id o correo, lectura con bloqueo, proyección pública, alta, y actualizaciones condicionales (`completePending`, `markVerified`, `updatePasswordIfMatches`) que resuelven carreras en la base.

## Guía de lectura

Operaciones para localizar en la fuente: `findById`, `findPublicProfileById`, `findAccountAppearanceById`, `findAccountAppearanceByIdForUpdate`, `updateAvatarImageId`, `findByIdForUpdate`, `findByEmail`, `create`, `completePending`, `markVerified`, `updateUsername`, `updatePasswordIfMatches`, `updatePassword`, `updatePaymentInfo`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PaymentInfo]], [[PublicUserProfile]], [[User]], [[UserRole]].

Referenciado por: [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence-contracts/src/main/java/ar/edu/itba/paw/persistence/UserDao.java>), líneas 1–40.

```java
package ar.edu.itba.paw.persistence;

import ar.edu.itba.paw.models.PaymentInfo;
import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.UserRole;

import java.util.Optional;

public interface UserDao {
    Optional<User> findById(long id);

    Optional<PublicUserProfile> findPublicProfileById(long id);

    Optional<PublicUserProfile> findAccountAppearanceById(long id);

    // Igual que findAccountAppearanceById, bloqueando la fila hasta el fin de la transaccion.
    Optional<PublicUserProfile> findAccountAppearanceByIdForUpdate(long id);

    boolean updateAvatarImageId(long id, Long imageId);

    // Bloquea la fila hasta el fin de la transaccion.
    Optional<User> findByIdForUpdate(long id);

    Optional<User> findByEmail(String email);

    User create(String username, String email, String passwordHash, UserRole role, String preferredLocale);

    boolean completePending(long id, String username, String passwordHash);

    boolean markVerified(long id);

    Optional<User> updateUsername(long id, String username);

    Optional<User> updatePasswordIfMatches(long id, String expectedPasswordHash, String newPasswordHash);

    Optional<User> updatePassword(long id, String newPasswordHash);

    Optional<User> updatePaymentInfo(long id, PaymentInfo paymentInfo);
}
```
