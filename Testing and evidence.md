---
title: "Testing and evidence"
categories: ["Testing"]
type: "guide"
module: "cross-cutting"
project: "quieroVinilos"
snapshot: "2026-10-04"
commit: "8929aeaa59b250e6c7119212f96437e153e815ac"
status: "documented"
sources: ["persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java", "persistence/src/test/resources/populator.sql", "persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java", "services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java", "services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java"]
---

# Testing and evidence

> [!summary] En una frase
> Hay 504 casos de test en dos módulos: los DAO se prueban contra una base HSQLDB en memoria con las migraciones reales, y los services con sus dependencias simuladas; nada prueba controllers, vistas, seguridad ni la ruta de PostgreSQL.

## Herramientas

| Herramienta | Para qué |
|---|---|
| JUnit Jupiter 5 | Motor de tests |
| `spring-test` (`SpringExtension`, `@ContextConfiguration`) | Levantar un contexto mínimo para los tests de DAO |
| HSQLDB en memoria con `sql.syntax_pgs=true` | Base de los tests de persistence |
| Flyway | Aplicar al HSQLDB las mismas migraciones que producción |
| `@Transactional` + `@Rollback` | Deshacer lo que cada test escribió |
| `JdbcTestUtils` | Contar filas para verificar el estado persistido |
| Mockito (`MockitoExtension`, `@Mock`, `@InjectMocks`) | Simular DAO y otros services en los tests de services |

## Qué hay

| Módulo | Clases | Casos | Cómo corren |
|---|---|---|---|
| `persistence` | 13 | 235 | Contexto de Spring + HSQLDB + migraciones + `populator.sql` |
| `services` | 12 | 269 | Mockito, sin Spring ni base |
| `webapp`, `models` | 0 | 0 | Regla del proyecto: no llevan tests |

| Tests de persistence | Casos | | Tests de services | Casos |
|---|---|---|---|---|
| [[PostJdbcDaoTest]] | 65 | | [[InquiryServiceImplTest]] | 86 |
| [[InquiryJdbcDaoTest]] | 41 | | [[PostServiceImplTest]] | 52 |
| [[ImageJdbcDaoTest]] | 27 | | [[UserServiceImplTest]] | 44 |
| [[UserJdbcDaoTest]] | 27 | | [[CartServiceImplTest]] | 21 |
| [[ReviewJdbcDaoTest]] | 14 | | [[EmailServiceImplTest]] | 17 |
| [[CartItemJdbcDaoTest]] | 12 | | [[AddressServiceImplTest]] | 10 |
| [[ArtistJdbcDaoTest]] | 11 | | [[ReviewServiceImplTest]] | 8 |
| [[AlbumJdbcDaoTest]] | 10 | | [[PaginationTest]] | 8 |
| [[PasswordResetTokenJdbcDaoTest]] | 9 | | [[ImageServiceImplTest]] | 7 |
| [[AddressJdbcDaoTest]] | 6 | | [[ArtistServiceImplTest]] | 6 |
| [[EmailVerificationTokenJdbcDaoTest]] | 6 | | [[ContactRulesTest]] | 6 |
| [[PostImageJdbcDaoTest]] | 4 | | [[AlbumServiceImplTest]] | 3 |
| [[MessageJdbcDaoTest]] | 3 | | [[PublicProfileServiceImplTest]] | 1 |

Los casos se contaron por ocurrencias de `@Test` en `8929aea`. No se ejecutaron en esta revisión.

## Cómo funciona un test de DAO

1. [[TestConfiguration]] crea un `DataSource` HSQLDB en memoria en modo de compatibilidad con PostgreSQL.
2. Flyway aplica V1 a V11.
3. `populator.sql` carga los datos fijos.
4. Cada test corre dentro de una transacción que se revierte al terminar, así que no se contaminan entre sí.
5. El test llama al DAO y verifica el valor devuelto o cuenta filas con `JdbcTestUtils`.

## Cómo funciona un test de service

1. `@Mock` crea DAO y services falsos; `@InjectMocks` construye el service con ellos.
2. El Arrange define qué devuelve cada dependencia (`Mockito.when(...).thenReturn(...)`).
3. El test llama al método y verifica **lo que devuelve o la excepción que lanza**.

[[InMemoryImageService]] es un doble escrito a mano de `ImageService` para los tests que necesitan que las imágenes guardadas se puedan volver a leer.

## Convenciones

| Regla | Motivo |
|---|---|
| Nombre `test<Método>When<Condición>Returns<Resultado>` | El nombre dice qué caso cubre |
| Tres bloques comentados: `// 1. Arrange`, `// 2. Exercise`, `// 3. Assert` | Estructura uniforme |
| Los datos de los tests de DAO salen solo de `populator.sql` | No insertar en el Arrange: los datos son compartidos y conocidos |
| Prohibido `Mockito.verify` y `Mockito.spy` | Se verifica el resultado o el estado, no que se haya llamado a un método. Un test que verifica llamadas se rompe con cualquier refactor aunque el comportamiento no cambie |
| Un service que solo delega al DAO no se testea | No hay lógica que probar |

En `8929aea` no hay ningún uso de `verify` ni `spy`. Dos tests de DAO hacen un `INSERT` directo: prueban que el `CHECK` de la migración rechaza un valor que el enum de Java impediría mandar.

## Qué prueba y qué no

| Evidencia | Qué establece | Qué no |
|---|---|---|
| Tests de persistence | El SQL de los DAO y las migraciones funcionan en HSQLDB | Que funcionen en PostgreSQL; concurrencia real |
| Tests de services | Las reglas de negocio, dadas ciertas respuestas de los DAO | Transacciones, bloqueos, integración con la base |
| `tools/paw_checks.py` | Paridad de i18n, versiones Flyway, balance de tags | Que la página renderice |
| Lectura estática (este vault) | Qué dice el código | Que se comporte así al ejecutarse |
| Arranque contra PostgreSQL | Que la ruta real funcione | Lo hace quien desarrolla; el vault no lo registra salvo que se indique |

La regla del proyecto lo dice sin vueltas: que los tests pasen no significa que la aplicación ande. Los tests corren con otro motor y ninguno ejercita controllers, JSP, filtros de seguridad, correo real ni la base de producción.

## Límites conocidos

- Sin tests de controllers, de seguridad (reglas de URL, `@PreAuthorize`) ni de vistas.
- Los bloqueos `FOR UPDATE` y las transiciones condicionales no se prueban con concurrencia.
- HSQLDB acepta sintaxis de PostgreSQL pero no es PostgreSQL: diferencias de tipos o de comportamiento pueden pasar inadvertidas.
- El envío de correo se prueba con un `JavaMailSender` simulado: nunca conecta a un SMTP.

## Preguntas de defensa

**¿Qué testean y cómo?**
Los DAO contra HSQLDB en memoria con las migraciones reales y datos de `populator.sql`; los services con Mockito.

**¿Por qué no usan `verify`?**
Porque acopla el test a la implementación. Se verifica el valor devuelto o el estado en la base.

**¿Cómo se aíslan los tests de DAO entre sí?**
Cada uno corre en una transacción que se revierte.

**¿Los tests garantizan que funciona en producción?**
No. Corren en otro motor y no cubren la capa web. Por eso la aplicación se levanta contra PostgreSQL antes de cerrar un cambio.

## Evidencia de código

### Test de DAO

Fuente exacta en `8929aea`: [persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java>), líneas 21–57.

```java
@Rollback
@Transactional
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = TestConfiguration.class)
public class CartItemJdbcDaoTest {

    private static final String CART_ITEMS_TABLE = "cart_items";
    private static final PostStatus POST_STATUS = PostStatus.AVAILABLE;
    private static final List<InquiryStatus> EXCLUDED_INQUIRY_STATUSES = InquiryStatus.OPEN_STATUSES;

    @Autowired
    private CartItemDao cartItemDao;

    @Autowired
    private DataSource dataSource;

    private JdbcTemplate jdbcTemplate;

    @BeforeEach
    public void setUp() {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Test
    public void testAddWhenPostIsNotInCartReturnsTrue() {
        // 1. Arrange
        final long userId = 1;
        final long postId = 2;

        // 2. Exercise
        final boolean result = cartItemDao.add(userId, postId);

        // 3. Assert
        Assertions.assertTrue(result);
        Assertions.assertEquals(1, JdbcTestUtils.countRowsInTableWhere(jdbcTemplate, CART_ITEMS_TABLE,
                "user_id = 1 AND post_id = 2"));
    }
```

### Test de service

Fuente exacta en `8929aea`: [services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java>), líneas 62–92.

```java
    @Test
    public void testAddWhenPostIsContactableReturnsThePost() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(false);
        Mockito.when(cartItemDao.countByUserId(BUYER_ID, CONTACTABLE, BLOCKING)).thenReturn(0);
        Mockito.when(cartItemDao.add(BUYER_ID, POST_ID)).thenReturn(true);

        // 2. Exercise
        final PostSummary result = cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        Assertions.assertEquals(POST_ID, result.getId());
    }

    @Test
    public void testAddWhenPostIsAlreadyInCartReturnsAlreadyInCartRejection() {
        // 1. Arrange
        Mockito.when(postService.findById(POST_ID)).thenReturn(post(POST_ID, SELLER_ID, PostStatus.AVAILABLE));
        Mockito.when(inquiryService.findOpenInquiryId(POST_ID, BUYER_ID)).thenReturn(Optional.empty());
        Mockito.when(cartItemDao.contains(BUYER_ID, POST_ID)).thenReturn(true);

        // 2. Exercise
        final Executable add = () -> cartService.add(BUYER_ID, POST_ID);

        // 3. Assert
        final CartAddRejectedException exception = Assertions.assertThrows(CartAddRejectedException.class, add);
        Assertions.assertEquals(CartAddRejectedException.Reason.ALREADY_IN_CART, exception.getReason());
        Assertions.assertEquals(POST_ID, exception.getPostId());
    }
```

## Archivos para seguir el flujo

- [persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/TestConfiguration.java>) · [[TestConfiguration]]
- [persistence/src/test/resources/populator.sql](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/resources/populator.sql>)
- [persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/persistence/src/test/java/ar/edu/itba/paw/persistence/CartItemJdbcDaoTest.java>) · [[CartItemJdbcDaoTest]]
- [services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/CartServiceImplTest.java>) · [[CartServiceImplTest]]
- [services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java](</Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b/services/src/test/java/ar/edu/itba/paw/services/InMemoryImageService.java>) · [[InMemoryImageService]]

Fuente inspeccionada: `8929aea`, 2026-10-04. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]
