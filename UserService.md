---
title: "UserService"
categories: ["Services"]
type: "code"
module: "services-contracts"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java"]
---

# UserService

Contrato de Cuentas: registro, verificación y reenvío, nombre, avatar, cambio y recuperación de contraseña, datos de cobro y bloqueo de fila para serializar operaciones de una misma Cuenta.

## Guía de lectura

Operaciones para localizar en la fuente: `findById`, `findPublicProfileById`, `findAccountAppearanceById`, `updateAvatar`, `lockById`, `findByEmail`, `register`, `verifyEmail`, `resendVerification`, `updateUsername`, `changePassword`, `requestPasswordReset`, `resetPassword`, `updatePaymentInfo`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[ImageUpload]], [[PublicUserProfile]], [[User]].

Referenciado por: [[AddressServiceImpl]], [[AddressServiceImplTest]], [[AuthenticatedUserDetailsService]], [[AuthenticationController]], [[CartServiceImpl]], [[CartServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[ProfileController]], [[PublicProfileServiceImpl]], [[PublicProfileServiceImplTest]], [[SecurityConfig]], [[UserServiceImpl]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/UserService.java>), líneas 1–44.

```java
package ar.edu.itba.paw.services;

import ar.edu.itba.paw.models.User;
import ar.edu.itba.paw.models.PublicUserProfile;
import ar.edu.itba.paw.models.ImageUpload;

import java.util.Locale;
import java.util.Optional;

public interface UserService {
    Optional<User> findById(long id);

    Optional<PublicUserProfile> findPublicProfileById(long id);

    Optional<PublicUserProfile> findAccountAppearanceById(long id);

    // avatar null quita la foto. Devuelve el id de la foto nueva, vacio si se quito. Lanza
    // InvalidImageException si la imagen no cumple ImageRules.
    Optional<Long> updateAvatar(long userId, ImageUpload avatar);

    // Bloquea la fila de la cuenta dentro de la transaccion del llamador: serializa las
    // operaciones de una misma cuenta que controlan un tope antes de escribir.
    User lockById(long id);

    Optional<User> findByEmail(String email);

    User register(String email, String username, String rawPassword, Locale locale);

    Optional<User> verifyEmail(String token, Locale locale);

    // false si no mando nada: la cuenta ya esta verificada o el ultimo enlace es muy reciente.
    boolean resendVerification(long userId, Locale locale);

    User updateUsername(long id, String username);

    User changePassword(long id, String currentPassword, String newPassword, Locale locale);

    void requestPasswordReset(String email, Locale locale);

    Optional<User> resetPassword(String token, String newPassword, Locale locale);

    // Lanza PaymentInfoRequiredException si deja la cuenta sin datos de cobro con una venta abierta.
    User updatePaymentInfo(long id, String cbu, String alias);
}
```
