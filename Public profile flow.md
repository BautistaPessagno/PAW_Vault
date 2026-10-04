---
title: "Public profile flow"
categories: ["Flows", "Web", "Services"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java", "services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java", "services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java", "models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java", "models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java", "models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java", "persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java", "webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java", "webapp/src/main/webapp/WEB-INF/views/profile/public.jsp", "webapp/src/main/webapp/WEB-INF/tags/avatar.tag", "persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java"]
---

# Public profile flow

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

Fuente exacta en `8929aea`: [services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java>), líneas 9–36.

```java
/*
 * Arma el perfil publico con lo de cada dominio: la Cuenta, sus publicaciones a la venta y sus
 * Resenas. Vive aparte porque PostService ya depende de UserService.
 */
@Service
public class PublicProfileServiceImpl implements PublicProfileService {

    private final UserService userService;
    private final PostService postService;
    private final ReviewService reviewService;

    @Autowired
    public PublicProfileServiceImpl(final UserService userService, final PostService postService,
                                    final ReviewService reviewService) {
        this.userService = userService;
        this.postService = postService;
        this.reviewService = reviewService;
    }

    @Override
    @Transactional(readOnly = true)
    public PublicProfile findByUserId(final long userId, final int pageNumber) {
        final PublicUserProfile user = userService.findPublicProfileById(userId)
                .orElseThrow(UserNotFoundException::new);
        return new PublicProfile(user, postService.findAvailableByPublisherId(userId, pageNumber),
                reviewService.statsForUser(userId), reviewService.findRecentForUser(userId));
    }
}
```

Fuente exacta en `8929aea`: [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java>), líneas 13–31.

```java
@Controller
public class PublicProfileController {
    private final PublicProfileService publicProfileService;

    @Autowired
    public PublicProfileController(final PublicProfileService publicProfileService) {
        this.publicProfileService = publicProfileService;
    }

    @RequestMapping(value = "/users/{id:[0-9]+}", method = RequestMethod.GET)
    public ModelAndView show(@PathVariable("id") final long id,
                             @RequestParam(name = "page", defaultValue = "1") final int pageNumber) {
        final ModelAndView view = new ModelAndView("profile/public");
        view.addObject("profile", publicProfileService.findByUserId(id, pageNumber));
        view.addObject("postOrigin", PostOrigin.PUBLIC_PROFILE);
        view.addObject("maxRating", ReviewRules.MAX_RATING);
        return view;
    }
}
```

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>), líneas 64–81.

```java
    @Override
    public Optional<PublicUserProfile> findPublicProfileById(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ? AND verified = TRUE",
                        PUBLIC_PROFILE_MAPPER, id)
                .stream().findAny();
    }

    @Override
    public Optional<PublicUserProfile> findAccountAppearanceById(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ?",
                PUBLIC_PROFILE_MAPPER, id).stream().findAny();
    }

    @Override
    public Optional<PublicUserProfile> findAccountAppearanceByIdForUpdate(final long id) {
        return jdbcTemplate.query(PUBLIC_PROFILE_SELECT + "WHERE id = ? FOR UPDATE",
                PUBLIC_PROFILE_MAPPER, id).stream().findAny();
    }
```

Fuente exacta en `8929aea`: [persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ImageJdbcDao.java>), líneas 56–61.

```java
    @Override
    public Optional<Image> findUserAvatar(final long userId, final long imageId) {
        return jdbcTemplate.query(IMAGE_SELECT + "WHERE i.id = ? AND EXISTS ("
                        + "SELECT 1 FROM users u WHERE u.id = ? AND u.verified = TRUE AND u.avatar_image_id = i.id)",
                ROW_MAPPER, imageId, userId).stream().findFirst();
    }
```

## Archivos para seguir el flujo

- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PublicProfileController.java>) · [[PublicProfileController]]
- [services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/main/java/ar/edu/itba/paw/services/PublicProfileServiceImpl.java>) · [[PublicProfileServiceImpl]]
- [services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services-contracts/src/main/java/ar/edu/itba/paw/services/PublicProfileService.java>) · [[PublicProfileService]]
- [models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicProfile.java>) · [[PublicProfile]]
- [models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/PublicUserProfile.java>) · [[PublicUserProfile]]
- [models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/models/src/main/java/ar/edu/itba/paw/models/ReviewStats.java>) · [[ReviewStats]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/UserJdbcDao.java>) · [[UserJdbcDao]]
- [persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/main/java/ar/edu/itba/paw/persistence/ReviewJdbcDao.java>) · [[ReviewJdbcDao]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/ImageController.java>) · [[ImageController]]
- [webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/java/ar/edu/itba/paw/webapp/controller/PostOrigin.java>) · [[PostOrigin]]
- [webapp/src/main/webapp/WEB-INF/views/profile/public.jsp](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/views/profile/public.jsp>)
- [webapp/src/main/webapp/WEB-INF/tags/avatar.tag](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/webapp/src/main/webapp/WEB-INF/tags/avatar.tag>)

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
