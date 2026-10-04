@title: Public profile flow
@categories: Flows, Web, Services
@files: webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java, services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java, services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java, models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java, models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java, models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java, persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java, persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java, webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java, webapp/src/main/webapp/WEB-INF/views/profile/public.jsp, webapp/src/main/webapp/WEB-INF/tags/avatar.tag

> [!summary] En una frase
> `/users/{id}` muestra, sin pedir sesión, el nombre y la foto de una Cuenta verificada, sus publicaciones a la venta y su reputación.

## Qué resuelve

Saber a quién le estás comprando (PR #46). Se llega desde la ficha de una publicación, desde la página de una venta y desde el autor de una reseña.

## Herramientas

| Herramienta | Para qué se usa acá |
|---|---|
| Un service de composición | [[PublicProfileServiceImpl]] junta lo de tres dominios |
| Proyección [[PublicUserProfile]] | Solo id, nombre y foto: nunca correo, hash ni datos de cobro |
| `WHERE verified = TRUE` | El perfil público existe solo para Cuentas verificadas |
| `Pagination` | Publicaciones de a 15 |
| [[ImageController]] | La foto se pide con el id de la Cuenta en la URL |

## Recorrido paso a paso

1. `GET /users/{id}?page=N`, ruta pública (`permitAll`).
2. `PublicProfileServiceImpl.findByUserId`, en una transacción de solo lectura:
   - `userService.findPublicProfileById`: `SELECT id, username, avatar_image_id FROM users WHERE id = ? AND verified = TRUE`. Si no hay fila, `UserNotFoundException` → 404.
   - `postService.findAvailableByPublisherId`: solo publicaciones `AVAILABLE`, más nuevas primero.
   - `reviewService.statsForUser`: cantidad y promedio de reseñas activas.
   - `reviewService.findRecentForUser`: las 10 más recientes.
3. La vista recibe `postOrigin = PUBLIC_PROFILE`. Cada tarjeta lo pasa a la ficha, que así sabe ofrecer "volver al perfil" con la página correcta ([[Post detail flow]]).
4. La foto se pide a `/users/{id}/avatar/{imageId}`. El SQL exige que la imagen sea el avatar vigente de esa Cuenta y que la Cuenta esté verificada.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Un service aparte para el perfil público | `PostService` ya depende de `UserService`; componer en uno de los dos crearía un ciclo | Comentario en [[PublicProfileServiceImpl]] |
| Una proyección mínima y no `User` | Que un dato privado no llegue a una vista pública por descuido | Estructura de [[PublicUserProfile]] |
| Solo Cuentas verificadas | Una Cuenta sin verificar puede ser un correo ajeno | Consulta de [[UserJdbcDao]] |
| Solo publicaciones disponibles | Es una vidriera; el historial queda en el perfil privado | Método `findAvailableByPublisherId` |
| Dos lecturas de apariencia: la del perfil privado no filtra por verificación, la pública sí | El perfil privado lee la Cuenta propia; la vista pública no muestra Cuentas sin verificar | Commit `e4babb17`; `findAccountAppearanceById` frente a `findPublicProfileById` en [[UserJdbcDao]] |
| Volver solo a un perfil conocido | La ficha construye la ruta de regreso a partir de un enum, no de un texto libre | Comentario en [[PostController]] |

## Límites conocidos

- Las reseñas no se paginan (10 fijas).
- Las cuatro lecturas son consultas separadas dentro de una transacción de solo lectura; no hay caché.
- Un solo test de service ([[PublicProfileServiceImplTest]]).

## Preguntas de defensa

**¿Qué datos de una Cuenta son públicos?**
Nombre, foto, publicaciones a la venta y reseñas recibidas. Nada más.

**¿Qué pasa si pido el perfil de una Cuenta sin verificar?**
404, igual que si no existiera.

**¿Por qué existe `PublicProfileService`?**
Para componer Cuenta, publicaciones y reseñas sin que un service de dominio dependa de los otros dos.

## Evidencia de código

{{code:services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java:9-36}}

{{code:webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java:13-31}}

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java:64-81}}

{{code:persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java:56-61}}
