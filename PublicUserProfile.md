---
title: "PublicUserProfile"
categories: ["Domain"]
type: "code"
module: "models"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java"]
---

# PublicUserProfile

Lo único de una Cuenta que se muestra a otros: id, nombre y foto. Sin correo, hash ni datos de cobro.

## Guía de lectura

Datos y dependencias declaradas: `id`, `username`, `avatarImageId`.

Operaciones para localizar en la fuente: `getId`, `getUsername`, `getAvatarImageId`.

## Conexiones

Referencias estáticas a tipos del proyecto: ninguna.

Referenciado por: [[PostDetail]], [[PostServiceImpl]], [[PostServiceImplTest]], [[PublicProfile]], [[PublicProfileServiceImpl]], [[UserDao]], [[UserJdbcDao]], [[UserJdbcDaoTest]], [[UserService]], [[UserServiceImpl]], [[UserServiceImplTest]].

Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.

## Fuente completa

Fuente exacta en `8929aea`: [models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java>), líneas 1–21.

```java
package ar.edu.itba.paw.models;

/*
 * Id, nombre y foto de una Cuenta: lo unico de ella que se muestra a otros. El perfil publico
 * solo la devuelve verificada; la propia Cuenta la ve tambien sin verificar, en su perfil.
 */
public final class PublicUserProfile {
    private final long id;
    private final String username;
    private final Long avatarImageId;

    public PublicUserProfile(final long id, final String username, final Long avatarImageId) {
        this.id = id;
        this.username = username;
        this.avatarImageId = avatarImageId;
    }

    public long getId() { return id; }
    public String getUsername() { return username; }
    public Long getAvatarImageId() { return avatarImageId; }
}
```
