---
title: "User"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-05"
commit: "c3e2a4cd23337bd35175d14ef551ba12a758a59d"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/User.java"]
---

# User

La Cuenta: nombre visible, correo, hash de la contraseña, [[UserRole]], si está verificada, idioma preferido y [[PaymentInfo]]. Inmutable. `verified` no impide iniciar sesión; habilita la authority `VERIFIED`. Ver [[Authentication flow]].

## Guía de lectura

Datos y dependencias declaradas: `id`, `username`, `email`, `passwordHash`, `role`, `verified`, `preferredLocale`, `paymentInfo`.

Operaciones para localizar en la fuente: `getId`, `getUsername`, `getEmail`, `getPasswordHash`, `getRole`, `isVerified`, `getPreferredLocale`, `getPaymentInfo`, `hasPaymentInfo`.

## Conexiones

Referencias estáticas a tipos del proyecto: [[PaymentInfo]], [[UserRole]].

Referenciado por: [[AuthenticatedUser]], [[AuthenticatedUserDetailsService]], [[AuthenticationController]], [[AuthenticationSessions]], [[EmailService]], [[EmailServiceImpl]], [[EmailServiceImplTest]], [[InquiryServiceImpl]], [[InquiryServiceImplTest]], [[PostServiceImpl]], [[PostServiceImplTest]], [[ProfileController]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserService]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `c3e2a4c`: [models/src/main/java/ar/edu/itba/paw/models/User.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/User.java>), líneas 1–69.

```java
package ar.edu.itba.paw.models;

public class User {
    private final long id;
    private final String username;
    private final String email;
    private final String passwordHash;
    private final UserRole role;
    private final boolean verified;
    private final String preferredLocale;
    private final PaymentInfo paymentInfo;

    // Las cuentas que todavia no cargaron datos de cobro.
    public User(final long id, final String username, final String email,
                final String passwordHash, final UserRole role, final boolean verified,
                final String preferredLocale) {
        this(id, username, email, passwordHash, role, verified, preferredLocale, PaymentInfo.NONE);
    }

    public User(final long id, final String username, final String email,
                final String passwordHash, final UserRole role, final boolean verified,
                final String preferredLocale, final PaymentInfo paymentInfo) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
        this.role = role;
        this.verified = verified;
        this.preferredLocale = preferredLocale;
        this.paymentInfo = paymentInfo;
    }

    public long getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public UserRole getRole() {
        return role;
    }

    public boolean isVerified() {
        return verified;
    }

    public String getPreferredLocale() {
        return preferredLocale;
    }

    // Nunca null: sin datos de cobro es PaymentInfo.NONE.
    public PaymentInfo getPaymentInfo() {
        return paymentInfo;
    }

    public boolean hasPaymentInfo() {
        return paymentInfo.isPresent();
    }
}
```
